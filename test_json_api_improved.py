#!/usr/bin/env python3
"""
改进的JSON API测试脚本
自动等待服务器启动
"""

import requests
import json
import time
import sys

# API配置
API_BASE_URL = "http://localhost:8000"
MAX_RETRY = 30  # 最大重试次数
RETRY_DELAY = 1  # 重试间隔(秒)

def wait_for_server():
    """等待服务器启动"""
    print("[INFO] 等待服务器启动...")
    
    for attempt in range(MAX_RETRY):
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=2)
            if response.status_code == 200:
                print(f"[SUCCESS] 服务器已启动 (尝试 {attempt + 1}/{MAX_RETRY})")
                return True
        except requests.exceptions.ConnectionError:
            print(f"[INFO] 等待服务器启动... ({attempt + 1}/{MAX_RETRY})")
            time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"[ERROR] 连接错误: {e}")
            time.sleep(RETRY_DELAY)
    
    print("[ERROR] 服务器启动超时，请检查:")
    print("   1. 是否运行了 python main.py")
    print("   2. 是否设置了GROQ_API_KEY环境变量")
    print("   3. 数据库是否可访问")
    return False

def test_api_health():
    """测试API健康检查"""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"[健康检查] 状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"[健康检查] 响应: {data['message']}")
        return response.status_code == 200
    except Exception as e:
        print(f"[错误] 健康检查失败: {e}")
        return False

def test_sample_queries():
    """测试示例查询接口"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/sample-queries")
        print(f"[示例查询] 状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"[示例查询] 可用示例: {len(data['sample_queries'])} 个")
            for i, query in enumerate(data['sample_queries'][:3], 1):
                print(f"  {i}. {query['question']}")
        return response.status_code == 200
    except Exception as e:
        print(f"[错误] 示例查询失败: {e}")
        return False

def test_database_info():
    """测试数据库信息接口"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/database-info")
        print(f"[数据库信息] 状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"[数据库信息] 表数量: {len(data['tables'])}")
            print(f"[数据库信息] 可用表: {', '.join(data['tables'].keys())}")
        return response.status_code == 200
    except Exception as e:
        print(f"[错误] 数据库信息失败: {e}")
        return False

def test_query_api(question):
    """测试查询API接口"""
    try:
        payload = {"question": question}
        response = requests.post(
            f"{API_BASE_URL}/api/query",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\n[查询] 问题: {question}")
        print(f"[查询] 状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"[查询] 成功: {data['success']}")
            print(f"[查询] 执行时间: {data['execution_time']:.3f}秒")
            
            if data['success']:
                print(f"[查询] 生成SQL: {data['sql']}")
                print(f"[查询] 结果数量: {data['count']} 条")
                
                if data['data'] and len(data['data']) > 0:
                    print(f"[查询] 结果示例:")
                    # 显示前2条结果
                    for i, row in enumerate(data['data'][:2], 1):
                        print(f"  {i}. {json.dumps(row, ensure_ascii=False, indent=2)}")
                    
                    if len(data['data']) > 2:
                        print(f"  ... 还有 {len(data['data']) - 2} 条结果")
                else:
                    print("[查询] 无结果数据")
            else:
                print(f"[查询] 错误: {data['error']}")
        else:
            print(f"[错误] API请求失败: {response.text}")
            
        return response.status_code == 200
        
    except Exception as e:
        print(f"[错误] 查询失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("Chat2BI JSON API 测试器")
    print("=" * 60)
    
    # 等待服务器启动
    if not wait_for_server():
        print("\n[ERROR] 无法连接到服务器")
        print("请先运行: python main.py")
        sys.exit(1)
    
    # 测试基础功能
    print("\n=== 基础功能测试 ===")
    basic_tests = [
        ("健康检查", test_api_health),
        ("示例查询", test_sample_queries),
        ("数据库信息", test_database_info)
    ]
    
    basic_success = 0
    for name, test_func in basic_tests:
        if test_func():
            basic_success += 1
            print(f"[SUCCESS] {name} 通过")
        else:
            print(f"[FAILED] {name} 失败")
    
    # 测试查询功能
    print("\n=== 查询功能测试 ===")
    test_questions = [
        "总销售额是多少？",
        "各个用户等级的人数分布",
        "哪个商品最受欢迎？",
        "已完成的订单数量是多少？"
    ]
    
    query_success = 0
    for question in test_questions:
        if test_query_api(question):
            query_success += 1
            print(f"[SUCCESS] 查询测试通过")
        else:
            print(f"[FAILED] 查询测试失败")
        time.sleep(0.5)  # 避免请求过快
    
    # 测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"基础功能: {basic_success}/{len(basic_tests)} 通过")
    print(f"查询功能: {query_success}/{len(test_questions)} 通过")
    print(f"总体成功率: {(basic_success + query_success)}/{len(basic_tests) + len(test_questions)} 通过")
    
    if basic_success == len(basic_tests) and query_success == len(test_questions):
        print("\n[SUCCESS] 所有测试通过！API运行正常")
        print("API地址: http://localhost:8000")
        print("API文档: http://localhost:8000/docs")
    else:
        print("\n[WARNING] 部分测试失败，请检查:")
        print("   1. 服务器是否正常运行")
        print("   2. 数据库连接是否正常")
        print("   3. GROQ_API_KEY是否设置")

if __name__ == "__main__":
    main() 