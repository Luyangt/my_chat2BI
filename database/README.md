# 电商销售数据库设计

## 数据库概述
这是一个为chat2BI项目设计的电商销售数据库，包含完整的用户、商品、订单等业务数据，用于支持自然语言查询转SQL的功能。

## 数据库结构

### 1. 用户表 (users)
- 存储用户基本信息、等级、地理位置等
- 支持用户画像分析和地域销售统计

### 2. 商品分类表 (categories)
- 支持层级分类结构
- 便于商品管理和分类销售统计

### 3. 商品表 (products)
- 完整的商品信息，包含价格、成本、库存等
- 支持利润分析和库存管理

### 4. 订单表 (orders)
- 订单主表，包含支付、物流、状态等信息
- 支持销售趋势和支付方式分析

### 5. 订单详情表 (order_items)
- 订单商品详情，支持多商品订单
- 用于商品销量统计和关联分析

## 数据统计
- 用户数据：15条
- 商品分类：10条
- 商品数据：20条
- 订单数据：15条
- 订单详情：30条
- **总计：90条数据**

## 使用方法

### 1. 创建数据库
```sql
mysql -u root -p < database/schema.sql
```

### 2. 导入样本数据
```sql
mysql -u root -p < database/sample_data.sql
```

### 3. 验证数据
```sql
USE ecommerce_bi;
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM orders;
```

## 支持的查询场景

这个数据库设计支持多种BI查询场景：

### 销售分析
- 总销售额统计
- 月度/季度销售趋势
- 地区销售分布
- 品牌销售排行

### 用户分析
- 用户等级分布
- 用户地域分布
- 用户购买行为分析
- 复购率分析

### 商品分析
- 商品销量排行
- 分类销售统计
- 库存状态分析
- 利润率分析

### 订单分析
- 订单状态统计
- 支付方式分析
- 平均订单金额
- 配送地区分析

## 示例查询

### 1. 销售额统计
```sql
SELECT SUM(final_amount) as total_sales FROM orders WHERE order_status = 'Delivered';
```

### 2. 热销商品TOP 5
```sql
SELECT p.product_name, SUM(oi.quantity) as total_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'Delivered'
GROUP BY p.product_id
ORDER BY total_sold DESC
LIMIT 5;
```

### 3. 用户等级分布
```sql
SELECT user_level, COUNT(*) as user_count
FROM users
GROUP BY user_level
ORDER BY user_count DESC;
```

### 4. 月度销售趋势
```sql
SELECT DATE_FORMAT(order_date, '%Y-%m') as month, 
       SUM(final_amount) as monthly_sales
FROM orders
WHERE order_status = 'Delivered'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
```

这个数据库设计为chat2BI项目提供了丰富的查询场景，可以支持各种复杂的自然语言查询转换为SQL的需求。 