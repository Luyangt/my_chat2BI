# Chat2BI JSON API 使用指南

## 概述
Chat2BI 现在支持通过JSON API返回查询结果，可以轻松集成到各种前端应用中。

## API 端点

### 1. 健康检查
```bash
GET /
```

### 2. 自然语言查询
```bash
POST /api/query
Content-Type: application/json

{
  "question": "总销售额是多少？"
}
```

### 3. 获取示例查询
```bash
GET /api/sample-queries
```

### 4. 获取数据库信息
```bash
GET /api/database-info
```

## 响应格式

### 成功响应
```json
{
  "success": true,
  "question": "总销售额是多少？",
  "sql": "SELECT SUM(oi.total_price) FROM orders o JOIN order_items oi ON o.order_id = oi.order_id;",
  "data": [
    {
      "SUM(oi.total_price)": 87699.9
    }
  ],
  "count": 1,
  "execution_time": 0.665
}
```

### 错误响应
```json
{
  "success": false,
  "question": "无效查询",
  "error": "SQL验证失败: 无效的表名",
  "execution_time": 0.123
}
```

## 使用示例

### 1. curl 命令示例

```bash
# 查询总销售额
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "总销售额是多少？"}'

# 查询用户信息
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "查询所有用户的信息"}'

# 获取示例查询
curl -X GET "http://localhost:8000/api/sample-queries"
```

### 2. Python 客户端示例

```python
import requests
import json

# API 配置
API_URL = "http://localhost:8000/api/query"

def query_chat2bi(question):
    """发送查询到Chat2BI API"""
    payload = {"question": question}
    response = requests.post(API_URL, json=payload)
    return response.json()

# 使用示例
questions = [
    "总销售额是多少？",
    "各个用户等级的人数分布",
    "哪个商品最受欢迎？"
]

for question in questions:
    result = query_chat2bi(question)
    print(f"问题: {question}")
    print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
    print("-" * 50)
```

### 3. JavaScript 客户端示例

```javascript
// 查询函数
async function queryChat2BI(question) {
    const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question: question
        })
    });
    
    return await response.json();
}

// 使用示例
const questions = [
    "总销售额是多少？",
    "各个用户等级的人数分布",
    "哪个商品最受欢迎？"
];

questions.forEach(async (question) => {
    const result = await queryChat2BI(question);
    console.log('问题:', question);
    console.log('结果:', result);
    console.log('-'.repeat(50));
});
```

## 数据类型处理

API 会自动处理以下数据类型转换：
- **Decimal** → **float**：数值精度保持
- **Date/DateTime** → **ISO格式字符串**：便于前端处理
- **MySQL枚举** → **字符串**：直接可用

## 示例查询列表

API 提供了以下预设查询示例：

1. **总销售额是多少？** - 查询所有已完成订单的总销售额
2. **查询所有用户的信息** - 获取用户基本信息列表
3. **哪个商品最受欢迎？** - 按销量排序找出最受欢迎的商品
4. **各个用户等级的人数分布** - 统计不同用户等级的用户数量
5. **月度销售趋势** - 按月份统计销售金额
6. **库存不足的商品** - 查询库存量低于50的商品

## 错误处理

API 会返回详细的错误信息：

- **SQL生成失败**：AI模型无法理解查询
- **SQL验证失败**：生成的SQL不符合安全规则
- **数据库连接失败**：数据库服务不可用
- **查询执行失败**：SQL语法错误或数据问题

## 性能说明

- **平均响应时间**：0.2-0.7秒
- **最大结果数量**：无限制（建议前端分页）
- **并发支持**：支持多个同时查询
- **缓存机制**：暂未实现（可后续添加）

## 安全特性

-  SQL注入防护
-  危险操作阻止 (DROP, DELETE, UPDATE, INSERT)
-  表名验证
-  CORS支持
-  请求验证

## 集成建议

1. **前端框架**：React、Vue、Angular 都可以直接使用
2. **移动端**：支持 React Native、Flutter 等
3. **后端集成**：可作为微服务集成到现有系统
4. **数据可视化**：结果可直接用于图表库（Chart.js、D3.js等）

## 启动服务

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py

# 服务将在 http://localhost:8000 上运行
```

## 测试验证

```bash
# 运行完整测试
python test_json_api.py

# 预期输出： 所有测试通过！JSON API运行正常
```

---

**注意**：确保已配置好GROQ_API_KEY环境变量和MySQL数据库连接。 