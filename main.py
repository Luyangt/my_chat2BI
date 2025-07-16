from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.query import router as query_router
import os

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

# 包含API路由
app.include_router(query_router, prefix="/api", tags=["query"])

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

def check_environment():
    """检查环境配置"""
    print("[INFO] 检查环境配置...")
    
    # 检查GROQ_API_KEY
    if not os.environ.get("GROQ_API_KEY"):
        print("[ERROR] 请设置GROQ_API_KEY环境变量")
        print("   获取API密钥：https://console.groq.com/")
        return False
    
    # 检查数据库连接
    try:
        from app.utils.database import get_db
        db = get_db()
        if db.connect():
            print("[SUCCESS] 数据库连接正常")
            db.disconnect()
        else:
            print("[ERROR] 数据库连接失败")
            return False
    except Exception as e:
        print(f"[ERROR] 数据库检查失败: {e}")
        return False
    
    print("[SUCCESS] 环境检查通过")
    return True

if __name__ == "__main__":
    import uvicorn
    
    print("[INFO] Chat2BI API 启动中...")
    
    # 检查环境
    if not check_environment():
        print("[ERROR] 环境检查失败，请修复后重试")
        exit(1)
    
    print("[INFO] 启动服务器...")
    print("[INFO] API地址: http://localhost:8000")
    print("[INFO] API文档: http://localhost:8000/docs")
    print("[INFO] 按 Ctrl+C 停止服务器")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("\n[INFO] 服务器已停止") 