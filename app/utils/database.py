import mysql.connector
from mysql.connector import Error
import sys
import os

# 添加database目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../../database'))

from config import get_database_config

class DatabaseManager:
    def __init__(self):
        self.config = get_database_config()
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """连接到数据库"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
            print("[SUCCESS] 数据库连接成功")
            return True
        except Error as e:
            print(f"[ERROR] 数据库连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("[INFO] 数据库连接已断开")
    
    def execute_query(self, query, params=None):
        """执行查询语句"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return None
        
        try:
            self.cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                result = self.cursor.fetchall()
                return result
            else:
                self.connection.commit()
                return self.cursor.rowcount
        except Error as e:
            print(f"[ERROR] 查询执行失败: {e}")
            return None
    
    def test_connection(self):
        """测试数据库连接和基本查询"""
        if not self.connect():
            return False
        
        try:
            # 测试基本查询
            result = self.execute_query("SELECT COUNT(*) as count FROM users")
            if result:
                user_count = result[0]['count']
                print(f"[INFO] 用户总数: {user_count}")
                
                # 测试更多表
                tables = ['categories', 'products', 'orders', 'order_items']
                for table in tables:
                    result = self.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                    if result:
                        count = result[0]['count']
                        print(f"[INFO] {table}: {count} 条记录")
                
                return True
            else:
                return False
        except Exception as e:
            print(f"[ERROR] 连接测试失败: {e}")
            return False
        finally:
            self.disconnect()

# 创建全局数据库实例
db_manager = DatabaseManager()

def get_db():
    """获取数据库连接实例"""
    return db_manager 