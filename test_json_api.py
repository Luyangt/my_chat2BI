#!/usr/bin/env python3
"""
测试JSON API接口功能
"""

import requests
import json
import time

# API配置
API_BASE_URL = "http://localhost:8000"

def test_api_health():
    """测试API健康检查"""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"[HEALTH CHECK] Status: {response.status_code}")
        print(f"[HEALTH CHECK] Response: {response.json()}")
        return True
    except Exception as e:
        print(f"[ERROR] 健康检查失败: {e}")
        return False

def test_sample_queries():
    """测试示例查询接口"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/sample-queries")
        print(f"[SAMPLE QUERIES] Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"[SAMPLE QUERIES] 可用示例查询: {len(data['sample_queries'])} 个")
            for i, query in enumerate(data['sample_queries'][:3], 1):
                print(f"  {i}. {query['question']} - {query['description']}")
        return True
    except Exception as e:
        print(f"[ERROR] 示例查询获取失败: {e}")
        return False

def test_database_info():
    """测试数据库信息接口"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/database-info")
        print(f"[DATABASE INFO] Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"[DATABASE INFO] 数据库表数量: {len(data['tables'])}")
            print(f"[DATABASE INFO] 可用表: {', '.join(data['tables'].keys())}")
        return True
    except Exception as e:
        print(f"[ERROR] 数据库信息获取失败: {e}")
        return False

def test_query_api(question):
    """测试查询API接口"""
    try:
        payload = {"question": question}
        response = requests.post(
            f"{API_BASE_URL}/api/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n[QUERY] 问题: {question}")
        print(f"[QUERY] Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[QUERY] 成功: {data['success']}")
            print(f"[QUERY] 执行时间: {data['execution_time']:.3f}s")
            
            if data['success']:
                print(f"[QUERY] 生成的SQL: {data['sql']}")
                print(f"[QUERY] 结果数量: {data['count']} 条")
                
                if data['data'] and len(data['data']) > 0:
                    print(f"[QUERY] 查询结果示例:")
                    # 显示前3条结果
                    for i, row in enumerate(data['data'][:3], 1):
                        print(f"  {i}. {json.dumps(row, ensure_ascii=False, indent=2)}")
                    
                    if len(data['data']) > 3:
                        print(f"  ... 还有 {len(data['data']) - 3} 条结果")
                else:
                    print("[QUERY] 无结果数据")
            else:
                print(f"[QUERY] 错误: {data['error']}")
        else:
            print(f"[ERROR] API请求失败: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"[ERROR] 查询API测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试Chat2BI JSON API...")
    
    # 测试基础功能
    print("\n=== 基础功能测试 ===")
    if not test_api_health():
        print("[ERROR] API服务未运行，请先启动服务器")
        return
    
    test_sample_queries()
    test_database_info()
    
    # 测试查询功能
    print("\n=== 查询功能测试 ===")
    test_questions = [
        "总销售额是多少？",
        "查询所有用户的信息",
        "哪个商品最受欢迎？",
        "各个用户等级的人数分布",
        "已完成的订单数量是多少？"
    ]
    
    success_count = 0
    for question in test_questions:
        if test_query_api(question):
            success_count += 1
        time.sleep(1)  # 避免请求过快
    
    print(f"\n=== 测试总结 ===")
    print(f"查询测试成功: {success_count}/{len(test_questions)}")
    
    if success_count == len(test_questions):
        print("🎉 所有测试通过！JSON API运行正常")
    else:
        print("⚠️  部分测试失败，请检查API服务")

if __name__ == "__main__":
    main() 