# 数据库配置
import os
from typing import Dict, Any

# 数据库连接配置
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'ecommerce_bi'),
    'charset': 'utf8mb4',
    'autocommit': True
}

# 数据库表信息（用于自然语言转SQL）
TABLE_SCHEMA = {
    'users': {
        'columns': [
            'user_id', 'username', 'email', 'phone', 'gender', 'age', 
            'city', 'province', 'registration_date', 'last_login_date', 
            'user_level', 'created_at'
        ],
        'description': '用户表，包含用户基本信息和等级',
        'primary_key': 'user_id'
    },
    'categories': {
        'columns': [
            'category_id', 'category_name', 'parent_category_id', 'created_at'
        ],
        'description': '商品分类表，支持层级分类',
        'primary_key': 'category_id'
    },
    'products': {
        'columns': [
            'product_id', 'product_name', 'category_id', 'brand', 'price', 
            'cost', 'stock_quantity', 'description', 'is_active', 'created_at'
        ],
        'description': '商品表，包含商品信息、价格和库存',
        'primary_key': 'product_id'
    },
    'orders': {
        'columns': [
            'order_id', 'user_id', 'order_date', 'total_amount', 'discount_amount', 
            'shipping_fee', 'final_amount', 'payment_method', 'order_status', 
            'shipping_address', 'created_at'
        ],
        'description': '订单表，包含订单信息和状态',
        'primary_key': 'order_id'
    },
    'order_items': {
        'columns': [
            'order_item_id', 'order_id', 'product_id', 'quantity', 
            'unit_price', 'total_price', 'created_at'
        ],
        'description': '订单详情表，包含订单中的商品信息',
        'primary_key': 'order_item_id'
    }
}

# 字段中文含义映射（用于自然语言理解）
FIELD_MAPPING = {
    # 用户表
    'user_id': '用户ID',
    'username': '用户名',
    'email': '邮箱',
    'phone': '手机号',
    'gender': '性别',
    'age': '年龄',
    'city': '城市',
    'province': '省份',
    'registration_date': '注册日期',
    'last_login_date': '最后登录时间',
    'user_level': '用户等级',
    
    # 商品表
    'product_id': '商品ID',
    'product_name': '商品名称',
    'category_id': '分类ID',
    'brand': '品牌',
    'price': '价格',
    'cost': '成本',
    'stock_quantity': '库存数量',
    'description': '描述',
    'is_active': '是否有效',
    
    # 订单表
    'order_id': '订单ID',
    'order_date': '订单日期',
    'total_amount': '订单总金额',
    'discount_amount': '优惠金额',
    'shipping_fee': '运费',
    'final_amount': '实付金额',
    'payment_method': '支付方式',
    'order_status': '订单状态',
    'shipping_address': '收货地址',
    
    # 订单详情表
    'order_item_id': '订单项ID',
    'quantity': '数量',
    'unit_price': '单价',
    'total_price': '总价',
    
    # 分类表
    'category_name': '分类名称',
    'parent_category_id': '父分类ID',
    
    # 通用字段
    'created_at': '创建时间'
}

# 表关系定义
TABLE_RELATIONSHIPS = {
    'users': {
        'orders': 'users.user_id = orders.user_id'
    },
    'categories': {
        'products': 'categories.category_id = products.category_id',
        'categories': 'categories.category_id = categories.parent_category_id'
    },
    'products': {
        'order_items': 'products.product_id = order_items.product_id',
        'categories': 'products.category_id = categories.category_id'
    },
    'orders': {
        'order_items': 'orders.order_id = order_items.order_id',
        'users': 'orders.user_id = users.user_id'
    },
    'order_items': {
        'orders': 'order_items.order_id = orders.order_id',
        'products': 'order_items.product_id = products.product_id'
    }
}

# 枚举值定义
ENUM_VALUES = {
    'gender': ['Male', 'Female', 'Other'],
    'user_level': ['Bronze', 'Silver', 'Gold', 'Platinum'],
    'payment_method': ['Credit Card', 'Debit Card', 'PayPal', 'Alipay', 'WeChat Pay'],
    'order_status': ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
}

def get_database_config() -> Dict[str, Any]:
    """获取数据库配置"""
    return DATABASE_CONFIG.copy()

def get_table_schema() -> Dict[str, Dict[str, Any]]:
    """获取表结构信息"""
    return TABLE_SCHEMA.copy()

def get_field_mapping() -> Dict[str, str]:
    """获取字段中文映射"""
    return FIELD_MAPPING.copy()

def get_table_relationships() -> Dict[str, Dict[str, str]]:
    """获取表关系定义"""
    return TABLE_RELATIONSHIPS.copy()

def get_enum_values() -> Dict[str, list]:
    """获取枚举值定义"""
    return ENUM_VALUES.copy() 