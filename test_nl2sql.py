#!/usr/bin/env python3
"""
测试自然语言转SQL功能
"""

import os
from app.services.nl2sql_service import get_nl2sql_service
from app.utils.database import get_db

def test_nl2sql_service():
    """测试自然语言转SQL服务"""
    
    # 检查API密钥
    if not os.environ.get("GROQ_API_KEY"):
        print("[ERROR] 请设置GROQ_API_KEY环境变量")
        print("获取API密钥：")
        print("1. 访问 https://console.groq.com/")
        print("2. 注册账户并获取API密钥")
        print("3. 设置环境变量: export GROQ_API_KEY=your_api_key")
        return False
    
    # 获取服务实例
    nl2sql = get_nl2sql_service()
    db = get_db()
    
    print("开始测试自然语言转SQL功能...")
    
    # 测试问题列表
    test_questions = [
        "总销售额是多少？",
        "查询所有用户的信息",
        "哪个商品最受欢迎？",
        "上海用户有多少个？",
        "苹果品牌的商品有哪些？",
        "已完成的订单数量是多少？"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n[TEST {i}] 问题: {question}")
        
        # 生成SQL
        result = nl2sql.generate_sql(question)
        
        if result["success"]:
            sql_query = result["sql"]
            print(f"[SUCCESS] 生成的SQL: {sql_query}")
            
            # 验证SQL
            is_valid, validation_message = nl2sql.validate_sql(sql_query)
            if is_valid:
                print(f"[VALID] {validation_message}")
                
                # 执行查询
                if db.connect():
                    query_result = db.execute_query(sql_query)
                    if query_result is not None:
                        print(f"[RESULT] 查询结果: {len(query_result)} 行数据")
                        if len(query_result) > 0:
                            print(f"[SAMPLE] 样本数据: {query_result[0] if len(query_result) > 0 else 'No data'}")
                    else:
                        print("[ERROR] 查询执行失败")
                    db.disconnect()
                else:
                    print("[ERROR] 数据库连接失败")
            else:
                print(f"[INVALID] {validation_message}")
        else:
            print(f"[ERROR] SQL生成失败: {result['error']}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_nl2sql_service() 