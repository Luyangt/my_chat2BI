# Chat2BI - 自然语言查询商业智能系统

Chat2BI是一个基于自然语言处理的商业智能查询系统，用户可以通过中文自然语言提问，系统会自动将问题转换为SQL查询并返回结果。

## 项目特性

- **自然语言查询**：支持中文自然语言输入，无需掌握SQL语法
- **智能SQL转换**：使用Groq/Llama3模型将自然语言转换为SQL查询
- **Web界面**：基于React和Ant Design的现代化Web界面
- **实时响应**：快速的查询响应和结果展示
- **多种查询类型**：支持销售统计、用户分析、产品查询等多种业务场景
- **结果可视化**：表格形式展示查询结果，支持分页和排序

## 技术栈

### 后端
- **FastAPI**：高性能Python Web框架
- **MySQL**：关系型数据库
- **Groq/Llama3**：自然语言处理模型
- **Uvicorn**：ASGI服务器

### 前端
- **React 19.1.0**：用户界面框架
- **TypeScript**：类型安全的JavaScript
- **Ant Design**：企业级UI组件库
- **Axios**：HTTP客户端

## 系统架构

```
Frontend (React)  →  Backend (FastAPI)  →  Database (MySQL)
     ↓                      ↓                    ↓
  用户界面              API接口              数据存储
  自然语言输入          SQL转换              查询执行
  结果展示              结果返回              数据管理
```

## 数据库结构

系统包含5个核心数据表：
- `users`：用户信息表
- `categories`：产品分类表
- `products`：产品信息表
- `orders`：订单信息表
- `order_items`：订单详情表

## 安装和配置

### 环境要求

- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### 1. 克隆项目
```bash
git clone <repository-url>
cd chat2BI
```

### 2. 后端配置

```bash
# 安装Python依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，设置数据库连接和API密钥
```

### 3. 数据库配置

```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE chat2BI"

# 导入数据
mysql -u root -p chat2BI < database/schema.sql
mysql -u root -p chat2BI < database/data.sql
```

### 4. 前端配置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 返回项目根目录
cd ..
```

## 使用方法

### 快速启动

使用便利脚本一键启动所有服务：

```bash
# 启动所有服务
./start_services.sh

# 停止所有服务
./stop_services.sh
```

### 手动启动

如果需要分别启动服务：

```bash
# 启动后端服务
uvicorn main:app --reload --port 8000

# 启动前端服务（新终端）
cd frontend
npm start
```

### 访问应用

- **Web界面**：http://localhost:3000
- **API文档**：http://localhost:8000/docs
- **后端API**：http://localhost:8000

## 使用示例

### 支持的查询类型

1. **销售统计**
   - "总销售额是多少？"
   - "今年的销售情况如何？"

2. **用户分析**
   - "有多少用户？"
   - "用户等级分布情况？"

3. **产品查询**
   - "最受欢迎的产品是什么？"
   - "库存不足的产品有哪些？"

4. **趋势分析**
   - "每月销售趋势如何？"
   - "季度增长率？"

### Web界面使用

1. 打开 http://localhost:3000
2. 在输入框中输入自然语言查询
3. 点击"查询"按钮或使用快捷键
4. 查看结果表格和对应的SQL语句
5. 可以复制SQL语句用于其他用途

### API使用

#### 查询API

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "总销售额是多少？"}'
```

#### 获取示例查询

```bash
curl "http://localhost:8000/api/sample-queries"
```

#### 获取数据库信息

```bash
curl "http://localhost:8000/api/database-info"
```

## API文档

### POST /api/query

执行自然语言查询

**请求体**：
```json
{
  "question": "总销售额是多少？"
}
```

**响应**：
```json
{
  "success": true,
  "question": "总销售额是多少？",
  "sql": "SELECT SUM(oi.quantity * oi.price) as total_sales FROM order_items oi",
  "data": [{"total_sales": 87699.9}],
  "count": 1,
  "execution_time": 0.05
}
```

### GET /api/sample-queries

获取示例查询列表

### GET /api/database-info

获取数据库表结构信息

## 项目结构

```
chat2BI/
├── app/
│   ├── api/          # API路由
│   ├── config/       # 配置文件
│   ├── models/       # 数据模型
│   └── services/     # 业务逻辑
├── database/         # 数据库文件
├── frontend/         # React前端应用
├── static/           # 静态文件
├── main.py           # 应用入口
├── requirements.txt  # Python依赖
├── start_services.sh # 启动脚本
├── stop_services.sh  # 停止脚本
└── README.md         # 项目说明
```

## 开发指南

### 添加新的查询类型

1. 在`app/services/query_service.py`中添加新的查询逻辑
2. 更新示例查询列表
3. 测试新的查询类型

### 修改数据库结构

1. 更新`database/schema.sql`
2. 重新导入数据库
3. 更新相关查询逻辑

### 前端开发

```bash
cd frontend
npm run dev    # 开发模式
npm run build  # 构建生产版本
npm test       # 运行测试
```

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查MySQL服务是否运行
   - 验证`.env`文件中的数据库配置

2. **前端无法连接后端**
   - 确认后端服务在8000端口运行
   - 检查防火墙设置

3. **查询结果为空**
   - 验证数据库中是否有数据
   - 检查查询语句是否正确

### 日志查看

- 后端日志：终端输出
- 前端日志：浏览器开发者工具
- 数据库日志：MySQL日志文件

## 许可证

本项目采用MIT许可证。详情请参阅LICENSE文件。

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 联系方式

如有问题或建议，请通过以下方式联系：

- 创建Issue
- 发送邮件至项目维护者
- 在讨论区发起讨论

---

感谢使用Chat2BI系统！