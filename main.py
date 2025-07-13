from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用实例
app = FastAPI(
    title="Chat2BI API",
    description="将自然语言转换为SQL查询的API服务",
    version="1.0.0"
)

# 配置CORS中间件（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 基础健康检查接口
@app.get("/")
async def root():
    return {"message": "Chat2BI API is running", "status": "healthy"}

# 获取API信息
@app.get("/api/info")
async def get_api_info():
    return {
        "name": "Chat2BI",
        "version": "1.0.0",
        "description": "自然语言转SQL查询API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 