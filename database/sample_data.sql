-- 电商销售数据库样本数据
USE ecommerce_bi;

-- 插入商品分类数据
INSERT INTO categories (category_name, parent_category_id) VALUES
('Electronics', NULL),
('Clothing', NULL),
('Books', NULL),
('Home & Garden', NULL),
('Sports', NULL),
('Smartphones', 1),
('Laptops', 1),
('Men Clothing', 2),
('Women Clothing', 2),
('Fiction Books', 3);

-- 插入用户数据
INSERT INTO users (username, email, phone, gender, age, city, province, registration_date, last_login_date, user_level) VALUES
('john_doe', 'john.doe@email.com', '13812345678', 'Male', 28, 'Shanghai', 'Shanghai', '2023-01-15', '2024-01-15 10:30:00', 'Gold'),
('jane_smith', 'jane.smith@email.com', '13887654321', 'Female', 32, 'Beijing', 'Beijing', '2023-02-20', '2024-01-14 14:20:00', 'Silver'),
('mike_wang', 'mike.wang@email.com', '13765432109', 'Male', 25, 'Shenzhen', 'Guangdong', '2023-03-10', '2024-01-13 09:15:00', 'Bronze'),
('lisa_chen', 'lisa.chen@email.com', '13654321098', 'Female', 29, 'Hangzhou', 'Zhejiang', '2023-04-05', '2024-01-12 16:45:00', 'Platinum'),
('david_li', 'david.li@email.com', '13543210987', 'Male', 35, 'Guangzhou', 'Guangdong', '2023-05-12', '2024-01-11 11:20:00', 'Gold'),
('sarah_zhang', 'sarah.zhang@email.com', '13432109876', 'Female', 27, 'Chengdu', 'Sichuan', '2023-06-18', '2024-01-10 13:30:00', 'Silver'),
('alex_liu', 'alex.liu@email.com', '13321098765', 'Male', 31, 'Wuhan', 'Hubei', '2023-07-22', '2024-01-09 15:10:00', 'Bronze'),
('emma_wu', 'emma.wu@email.com', '13210987654', 'Female', 26, 'Xian', 'Shaanxi', '2023-08-08', '2024-01-08 10:55:00', 'Gold'),
('tom_huang', 'tom.huang@email.com', '13109876543', 'Male', 33, 'Nanjing', 'Jiangsu', '2023-09-14', '2024-01-07 12:40:00', 'Silver'),
('amy_zhao', 'amy.zhao@email.com', '13098765432', 'Female', 24, 'Tianjin', 'Tianjin', '2023-10-20', '2024-01-06 14:25:00', 'Bronze'),
('kevin_xu', 'kevin.xu@email.com', '13987654321', 'Male', 30, 'Qingdao', 'Shandong', '2023-11-05', '2024-01-05 16:15:00', 'Platinum'),
('lucy_yang', 'lucy.yang@email.com', '13876543210', 'Female', 28, 'Dalian', 'Liaoning', '2023-12-01', '2024-01-04 09:30:00', 'Gold'),
('peter_zhou', 'peter.zhou@email.com', '13765432100', 'Male', 34, 'Suzhou', 'Jiangsu', '2023-12-15', '2024-01-03 11:45:00', 'Silver'),
('helen_gao', 'helen.gao@email.com', '13654321000', 'Female', 29, 'Xiamen', 'Fujian', '2024-01-02', '2024-01-02 13:20:00', 'Bronze'),
('ryan_ma', 'ryan.ma@email.com', '13543210000', 'Male', 27, 'Kunming', 'Yunnan', '2024-01-05', '2024-01-01 15:35:00', 'Gold');

-- 插入商品数据
INSERT INTO products (product_name, category_id, brand, price, cost, stock_quantity, description) VALUES
('iPhone 15 Pro', 6, 'Apple', 7999.00, 6000.00, 50, 'Latest iPhone with Pro features'),
('Samsung Galaxy S24', 6, 'Samsung', 6999.00, 5200.00, 45, 'Flagship Android smartphone'),
('Xiaomi 14', 6, 'Xiaomi', 3999.00, 2800.00, 60, 'High-performance smartphone'),
('MacBook Pro 16"', 7, 'Apple', 18999.00, 14000.00, 25, 'Professional laptop for creators'),
('Dell XPS 13', 7, 'Dell', 8999.00, 6500.00, 30, 'Ultrabook for business'),
('Lenovo ThinkPad X1', 7, 'Lenovo', 12999.00, 9500.00, 20, 'Business laptop'),
('Nike Air Max 270', 8, 'Nike', 899.00, 400.00, 100, 'Comfortable running shoes'),
('Adidas Ultraboost 22', 8, 'Adidas', 1299.00, 600.00, 80, 'Premium running shoes'),
('Uniqlo Cotton T-Shirt', 8, 'Uniqlo', 99.00, 45.00, 200, 'Basic cotton t-shirt'),
('Zara Casual Dress', 9, 'Zara', 299.00, 120.00, 75, 'Elegant casual dress'),
('H&M Jeans', 9, 'H&M', 199.00, 80.00, 150, 'Comfortable denim jeans'),
('The Great Gatsby', 10, 'Classic Books', 29.90, 15.00, 300, 'Classic American novel'),
('Harry Potter Set', 10, 'Bloomsbury', 199.00, 100.00, 120, 'Complete Harry Potter series'),
('Dyson V15 Vacuum', 4, 'Dyson', 3999.00, 2500.00, 35, 'Powerful cordless vacuum'),
('Philips Air Fryer', 4, 'Philips', 899.00, 500.00, 55, 'Healthy cooking appliance'),
('Wilson Tennis Racket', 5, 'Wilson', 799.00, 350.00, 40, 'Professional tennis racket'),
('Nike Football', 5, 'Nike', 199.00, 80.00, 90, 'Official size football'),
('Yoga Mat Premium', 5, 'Lululemon', 399.00, 150.00, 70, 'High-quality yoga mat'),
('AirPods Pro 2', 6, 'Apple', 1899.00, 1200.00, 85, 'Wireless earbuds with ANC'),
('Sony WH-1000XM5', 6, 'Sony', 2399.00, 1500.00, 65, 'Premium noise-canceling headphones');

-- 插入订单数据
INSERT INTO orders (user_id, order_date, total_amount, discount_amount, shipping_fee, final_amount, payment_method, order_status, shipping_address) VALUES
(1, '2024-01-01 10:30:00', 8098.00, 99.00, 0.00, 7999.00, 'Alipay', 'Delivered', 'Shanghai, Pudong New Area, Century Avenue 100'),
(2, '2024-01-02 14:20:00', 1198.00, 99.00, 0.00, 1099.00, 'WeChat Pay', 'Delivered', 'Beijing, Chaoyang District, Guomao Street 200'),
(3, '2024-01-03 09:15:00', 3999.00, 0.00, 15.00, 4014.00, 'Credit Card', 'Delivered', 'Shenzhen, Nanshan District, Keji Road 300'),
(4, '2024-01-04 16:45:00', 18999.00, 0.00, 0.00, 18999.00, 'Credit Card', 'Delivered', 'Hangzhou, Xihu District, Wenyi Road 400'),
(5, '2024-01-05 11:20:00', 898.00, 0.00, 15.00, 913.00, 'PayPal', 'Delivered', 'Guangzhou, Tianhe District, Zhujiang Road 500'),
(6, '2024-01-06 13:30:00', 498.00, 0.00, 15.00, 513.00, 'Alipay', 'Delivered', 'Chengdu, Jinjiang District, Chunxi Road 600'),
(7, '2024-01-07 15:10:00', 8999.00, 0.00, 0.00, 8999.00, 'WeChat Pay', 'Delivered', 'Wuhan, Wuchang District, Zhongnan Road 700'),
(8, '2024-01-08 10:55:00', 1598.00, 0.00, 15.00, 1613.00, 'Credit Card', 'Delivered', 'Xian, Yanta District, Gaoxin Road 800'),
(9, '2024-01-09 12:40:00', 229.90, 0.00, 10.00, 239.90, 'Alipay', 'Delivered', 'Nanjing, Gulou District, Zhongshan Road 900'),
(10, '2024-01-10 14:25:00', 3999.00, 0.00, 0.00, 3999.00, 'Credit Card', 'Delivered', 'Tianjin, Heping District, Binjiang Road 1000'),
(11, '2024-01-11 16:15:00', 799.00, 0.00, 15.00, 814.00, 'PayPal', 'Shipped', 'Qingdao, Shinan District, Xianggang Road 1100'),
(12, '2024-01-12 09:30:00', 6999.00, 0.00, 0.00, 6999.00, 'WeChat Pay', 'Processing', 'Dalian, Zhongshan District, Renmin Road 1200'),
(13, '2024-01-13 11:45:00', 12999.00, 0.00, 0.00, 12999.00, 'Credit Card', 'Processing', 'Suzhou, Gusu District, Guanqian Street 1300'),
(14, '2024-01-14 13:20:00', 898.00, 0.00, 15.00, 913.00, 'Alipay', 'Pending', 'Xiamen, Siming District, Zhongshan Road 1400'),
(15, '2024-01-15 15:35:00', 1899.00, 0.00, 0.00, 1899.00, 'WeChat Pay', 'Pending', 'Kunming, Wuhua District, Dongfeng Road 1500');

-- 插入订单详情数据
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(1, 1, 1, 7999.00, 7999.00),
(1, 9, 1, 99.00, 99.00),
(2, 7, 1, 899.00, 899.00),
(2, 8, 1, 1299.00, 1299.00),
(3, 3, 1, 3999.00, 3999.00),
(4, 4, 1, 18999.00, 18999.00),
(5, 16, 1, 799.00, 799.00),
(5, 9, 1, 99.00, 99.00),
(6, 10, 1, 299.00, 299.00),
(6, 11, 1, 199.00, 199.00),
(7, 5, 1, 8999.00, 8999.00),
(8, 8, 1, 1299.00, 1299.00),
(8, 10, 1, 299.00, 299.00),
(9, 12, 1, 29.90, 29.90),
(9, 13, 1, 199.00, 199.00),
(10, 14, 1, 3999.00, 3999.00),
(11, 16, 1, 799.00, 799.00),
(12, 2, 1, 6999.00, 6999.00),
(13, 6, 1, 12999.00, 12999.00),
(14, 7, 1, 899.00, 899.00),
(15, 19, 1, 1899.00, 1899.00),
(2, 17, 1, 199.00, 199.00),
(3, 18, 1, 399.00, 399.00),
(5, 17, 1, 199.00, 199.00),
(8, 20, 1, 2399.00, 2399.00),
(9, 9, 2, 99.00, 198.00),
(10, 15, 1, 899.00, 899.00),
(11, 18, 1, 399.00, 399.00),
(12, 19, 1, 1899.00, 1899.00),
(13, 1, 1, 7999.00, 7999.00); 