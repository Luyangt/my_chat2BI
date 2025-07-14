import os
from groq import Groq
import json
import sys
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 添加database目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../../database'))

# 导入database配置
import importlib.util
spec = importlib.util.spec_from_file_location("db_config", os.path.join(os.path.dirname(__file__), '../../database/config.py'))
db_config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db_config)

get_table_schema = db_config.get_table_schema
get_field_mapping = db_config.get_field_mapping
get_table_relationships = db_config.get_table_relationships
get_enum_values = db_config.get_enum_values

class NL2SQLService:
    def __init__(self):
        # 初始化Groq客户端
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY", "")
        )
        
        # 获取数据库元数据
        self.table_schema = get_table_schema()
        self.field_mapping = get_field_mapping()
        self.table_relationships = get_table_relationships()
        self.enum_values = get_enum_values()
        
    def _build_database_context(self):
        """构建数据库上下文信息"""
        context = """
### Database Schema Information

This is the complete structure of the e-commerce sales database:

**Table Structures:**
"""
        
        # 添加表结构信息
        for table_name, table_info in self.table_schema.items():
            context += f"\n**{table_name} table** ({table_info['description']}):\n"
            context += f"- Primary key: {table_info['primary_key']}\n"
            context += "- Columns:\n"
            for column in table_info['columns']:
                chinese_name = self.field_mapping.get(column, column)
                context += f"  - {column} ({chinese_name})\n"
        
        # 添加表关系信息
        context += "\n**Table Relationships:**\n"
        for table, relations in self.table_relationships.items():
            for related_table, join_condition in relations.items():
                context += f"- {table} -> {related_table}: {join_condition}\n"
        
        # 添加枚举值信息
        context += "\n**Enum Values:**\n"
        for field, values in self.enum_values.items():
            context += f"- {field}: {', '.join(values)}\n"
        
        return context
    
    def _build_prompt(self, user_question):
        """构建完整的提示词"""
        database_context = self._build_database_context()
        
        prompt = f"""
You are a professional SQL query generation expert. Please generate accurate MySQL queries based on user's natural language questions.

{database_context}

### Important Rules:
1. Return ONLY the SQL query statement, nothing else
2. Do NOT include any explanations, descriptions, or comments
3. Use MySQL syntax
4. Field names and table names must exactly match the database structure
5. Use appropriate JOINs to connect tables
6. For time queries, use appropriate DATE functions
7. For fuzzy queries, use LIKE operator
8. For statistical queries, use COUNT, SUM, AVG and other aggregate functions
9. For sorting queries, use ORDER BY
10. For pagination queries, use LIMIT

### Example:
Question: How many users are there?
Answer: SELECT COUNT(*) FROM users;

### User Question:
{user_question}

### SQL Query (return only the SQL statement):
"""
        return prompt
    
    def generate_sql(self, user_question):
        """生成SQL查询"""
        try:
            # 构建提示词
            prompt = self._build_prompt(user_question)
            
            # 调用Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",  # 使用Llama3-8B模型
                temperature=0.1,  # 降低随机性，提高准确性
                max_tokens=500,
                top_p=0.9,
            )
            
            # 提取生成的SQL
            sql_query = chat_completion.choices[0].message.content.strip()
            
            # 清理SQL查询（移除代码块标记等）
            sql_query = self._clean_sql(sql_query)
            
            return {
                "success": True,
                "sql": sql_query,
                "user_question": user_question
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "user_question": user_question
            }
    
    def _clean_sql(self, sql_query):
        """清理SQL查询"""
        # 移除代码块标记
        sql_query = sql_query.replace("```sql", "").replace("```", "")
        
        # 寻找SQL语句（通常以SELECT开头）
        lines = sql_query.split('\n')
        sql_lines = []
        
        for line in lines:
            line = line.strip()
            # 跳过空行和非SQL内容
            if line and (line.upper().startswith('SELECT') or 
                        line.upper().startswith('FROM') or 
                        line.upper().startswith('WHERE') or 
                        line.upper().startswith('JOIN') or 
                        line.upper().startswith('GROUP BY') or 
                        line.upper().startswith('ORDER BY') or 
                        line.upper().startswith('LIMIT') or 
                        line.upper().startswith('HAVING') or 
                        (sql_lines and not line.lower().startswith('here is')) or
                        (sql_lines and not line.lower().startswith('answer:'))):
                sql_lines.append(line)
        
        # 如果找到SQL行，使用它们；否则使用原始清理后的查询
        if sql_lines:
            sql_query = ' '.join(sql_lines)
        else:
            sql_query = sql_query.strip()
        
        # 移除多余的空白
        sql_query = ' '.join(sql_query.split())
        
        # 确保以分号结尾
        if not sql_query.endswith(';'):
            sql_query += ';'
        
        return sql_query
    
    def validate_sql(self, sql_query):
        """验证SQL查询的基本语法"""
        # 基本的SQL关键字检查
        sql_upper = sql_query.upper()
        
        # 检查是否包含基本的SELECT语句
        if not sql_upper.startswith('SELECT'):
            return False, "Query must start with SELECT"
        
        # 检查是否包含危险操作
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'CREATE', 'TRUNCATE']
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                return False, f"Operation {keyword} is not allowed"
        
        # 检查表名是否存在
        table_names = list(self.table_schema.keys())
        found_table = False
        for table_name in table_names:
            if table_name.upper() in sql_upper:
                found_table = True
                break
        
        if not found_table:
            return False, "No valid table name found in query"
        
        return True, "SQL query validation passed"

# 创建全局服务实例
nl2sql_service = NL2SQLService()

def get_nl2sql_service():
    """获取自然语言转SQL服务实例"""
    return nl2sql_service 