from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

# 导入服务
from app.services.nl2sql_service import get_nl2sql_service
from app.utils.database import get_db

# 创建API路由
router = APIRouter()

# 请求模型
class QueryRequest(BaseModel):
    question: str
    
class QueryResponse(BaseModel):
    success: bool
    question: str
    sql: Optional[str] = None
    data: Optional[List[Dict[str, Any]]] = None
    count: Optional[int] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None

@router.post("/query", response_model=QueryResponse)
async def natural_language_query(request: QueryRequest):
    """
    自然语言查询接口
    
    接收自然语言问题，转换为SQL查询，执行并返回JSON结果
    """
    import time
    
    start_time = time.time()
    
    try:
        # 1. 获取服务实例
        nl2sql = get_nl2sql_service()
        db = get_db()
        
        # 2. 生成SQL查询
        sql_result = nl2sql.generate_sql(request.question)
        
        if not sql_result["success"]:
            return QueryResponse(
                success=False,
                question=request.question,
                error=f"SQL生成失败: {sql_result['error']}",
                execution_time=time.time() - start_time
            )
        
        sql_query = sql_result["sql"]
        
        # 3. 验证SQL查询
        is_valid, validation_message = nl2sql.validate_sql(sql_query)
        if not is_valid:
            return QueryResponse(
                success=False,
                question=request.question,
                sql=sql_query,
                error=f"SQL验证失败: {validation_message}",
                execution_time=time.time() - start_time
            )
        
        # 4. 执行SQL查询
        if not db.connect():
            return QueryResponse(
                success=False,
                question=request.question,
                sql=sql_query,
                error="数据库连接失败",
                execution_time=time.time() - start_time
            )
        
        try:
            query_result = db.execute_query(sql_query)
            
            if query_result is None:
                return QueryResponse(
                    success=False,
                    question=request.question,
                    sql=sql_query,
                    error="查询执行失败",
                    execution_time=time.time() - start_time
                )
            
            # 5. 处理查询结果
            result_data = []
            if isinstance(query_result, list):
                # 处理字典列表结果
                for row in query_result:
                    if isinstance(row, dict):
                        # 转换Decimal类型为float，处理日期时间格式
                        processed_row = {}
                        for key, value in row.items():
                            if hasattr(value, 'isoformat'):  # 日期时间对象
                                processed_row[key] = value.isoformat()
                            elif hasattr(value, '__float__'):  # Decimal对象
                                processed_row[key] = float(value)
                            else:
                                processed_row[key] = value
                        result_data.append(processed_row)
                    else:
                        result_data.append(row)
            else:
                # 单个值结果
                result_data = [{"result": query_result}]
            
            return QueryResponse(
                success=True,
                question=request.question,
                sql=sql_query,
                data=result_data,
                count=len(result_data),
                execution_time=time.time() - start_time
            )
            
        finally:
            db.disconnect()
            
    except Exception as e:
        return QueryResponse(
            success=False,
            question=request.question,
            error=f"系统错误: {str(e)}",
            execution_time=time.time() - start_time
        )

@router.get("/sample-queries")
async def get_sample_queries():
    """
    获取示例查询列表
    """
    return {
        "sample_queries": [
            {
                "question": "总销售额是多少？",
                "description": "查询所有已完成订单的总销售额"
            },
            {
                "question": "查询所有用户的信息",
                "description": "获取用户基本信息列表"
            },
            {
                "question": "哪个商品最受欢迎？",
                "description": "按销量排序找出最受欢迎的商品"
            },
            {
                "question": "各个用户等级的人数分布",
                "description": "统计不同用户等级的用户数量"
            },
            {
                "question": "月度销售趋势",
                "description": "按月份统计销售金额"
            },
            {
                "question": "库存不足的商品",
                "description": "查询库存量低于50的商品"
            }
        ]
    }

@router.get("/database-info")
async def get_database_info():
    """
    获取数据库结构信息
    """
    try:
        from app.services.nl2sql_service import get_nl2sql_service
        nl2sql = get_nl2sql_service()
        
        return {
            "tables": nl2sql.table_schema,
            "field_mapping": nl2sql.field_mapping,
            "relationships": nl2sql.table_relationships,
            "enum_values": nl2sql.enum_values
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据库信息失败: {str(e)}") 