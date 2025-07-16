#!/bin/bash

echo "启动 Chat2BI 服务..."

# 检查是否设置了GROQ_API_KEY
if [ -z "$GROQ_API_KEY" ]; then
    echo "[ERROR] 请设置GROQ_API_KEY环境变量"
    echo "export GROQ_API_KEY=\"your_api_key_here\""
    exit 1
fi

# 创建日志目录
mkdir -p logs

# 启动后端服务
echo "[INFO] 启动后端服务..."
python main.py > logs/backend.log 2>&1 &
BACKEND_PID=$!

# 等待后端服务启动
sleep 5

# 检查后端服务是否启动成功
if curl -s http://localhost:8000/ > /dev/null; then
    echo "[SUCCESS] 后端服务启动成功 (PID: $BACKEND_PID)"
else
    echo "[ERROR] 后端服务启动失败"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# 启动前端服务
echo "[INFO] 启动前端服务..."
cd frontend
npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "[SUCCESS] 服务启动完成"
echo "后端服务: http://localhost:8000 (PID: $BACKEND_PID)"
echo "前端服务: http://localhost:3000 (PID: $FRONTEND_PID)"
echo "API文档: http://localhost:8000/docs"

# 保存PID到文件
echo $BACKEND_PID > logs/backend.pid
echo $FRONTEND_PID > logs/frontend.pid

echo ""
echo "按 Ctrl+C 停止所有服务"

# 等待用户中断
trap "echo ''; echo '[INFO] 停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '[INFO] 服务已停止'; exit 0" INT

# 保持脚本运行
wait 