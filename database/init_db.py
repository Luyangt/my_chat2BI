#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建数据库表结构和导入示例数据
"""

import mysql.connector
import os
from config import get_database_config

def read_sql_file(file_path):
    """读取SQL文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def execute_sql_file(cursor, sql_content):
    """执行SQL文件内容"""
    # 按分号分割SQL语句
    statements = sql_content.split(';')
    
    for statement in statements:
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
                print(f"[SUCCESS] 执行成功: {statement[:50]}...")
            except mysql.connector.Error as err:
                print(f"[ERROR] 执行失败: {err}")
                print(f"  语句: {statement[:100]}...")

def init_database():
    """初始化数据库"""
    config = get_database_config()
    
    try:
        # 连接MySQL服务器（不指定数据库）
        conn = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            charset=config['charset']
        )
        
        cursor = conn.cursor()
        
        print("开始初始化数据库...")
        
        # 1. 创建数据库结构
        print("\n[SCHEMA] 创建数据库表结构...")
        schema_sql = read_sql_file('schema.sql')
        execute_sql_file(cursor, schema_sql)
        
        # 2. 插入示例数据
        print("\n[DATA] 插入示例数据...")
        data_sql = read_sql_file('sample_data.sql')
        execute_sql_file(cursor, data_sql)
        
        # 3. 验证数据
        print("\n[VERIFY] 验证数据...")
        cursor.execute("USE ecommerce_bi")
        
        tables = ['users', 'categories', 'products', 'orders', 'order_items']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"[OK] {table}: {count} 条记录")
        
        conn.commit()
        print("\n[COMPLETE] 数据库初始化完成！")
        
    except mysql.connector.Error as err:
        print(f"[ERROR] 数据库连接错误: {err}")
        return False
    except FileNotFoundError as err:
        print(f"[ERROR] 文件不存在: {err}")
        return False
    except Exception as err:
        print(f"[ERROR] 未知错误: {err}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
    
    return True

def test_connection():
    """测试数据库连接"""
    config = get_database_config()
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # 测试查询
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM orders WHERE order_status = 'Delivered'")
        delivered_orders = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(final_amount) FROM orders WHERE order_status = 'Delivered'")
        total_sales = cursor.fetchone()[0]
        
        print(f"[SUCCESS] 数据库连接成功！")
        print(f"[INFO] 用户总数: {user_count}")
        print(f"[INFO] 已完成订单: {delivered_orders}")
        print(f"[INFO] 总销售额: ¥{total_sales:,.2f}")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"[ERROR] 数据库连接失败: {err}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='数据库初始化工具')
    parser.add_argument('--init', action='store_true', help='初始化数据库')
    parser.add_argument('--test', action='store_true', help='测试数据库连接')
    
    args = parser.parse_args()
    
    if args.init:
        init_database()
    elif args.test:
        test_connection()
    else:
        print("请使用 --init 初始化数据库或 --test 测试连接")
        print("例如: python init_db.py --init") 