#!/usr/bin/env python3
"""
测试数据库连接
"""

from app.utils.database import get_db

def test_database_connection():
    print("开始测试数据库连接...")
    
    # 获取数据库实例
    db = get_db()
    
    # 测试连接
    success = db.test_connection()
    
    if success:
        print("[SUCCESS] 数据库连接测试通过")
        
        # 测试一些基本查询
        print("\n测试基本查询...")
        
        # 重新连接进行查询测试
        if db.connect():
            # 查询用户信息
            users = db.execute_query("SELECT username, city, user_level FROM users LIMIT 3")
            if users:
                print("[INFO] 用户样本数据:")
                for user in users:
                    print(f"  - {user['username']} ({user['city']}, {user['user_level']})")
            
            # 查询商品信息
            products = db.execute_query("SELECT product_name, brand, price FROM products LIMIT 3")
            if products:
                print("[INFO] 商品样本数据:")
                for product in products:
                    print(f"  - {product['product_name']} ({product['brand']}, ¥{product['price']})")
            
            # 查询订单统计
            orders = db.execute_query("""
                SELECT COUNT(*) as total_orders, 
                       SUM(final_amount) as total_sales 
                FROM orders 
                WHERE order_status = 'Delivered'
            """)
            if orders:
                order_info = orders[0]
                print(f"[INFO] 订单统计: {order_info['total_orders']} 个已完成订单, 总销售额: ¥{order_info['total_sales']}")
            
            db.disconnect()
        
        return True
    else:
        print("[ERROR] 数据库连接测试失败")
        return False

if __name__ == "__main__":
    test_database_connection() 