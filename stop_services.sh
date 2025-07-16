#!/bin/bash

echo "停止 Chat2BI 服务..."

# 检查PID文件是否存在
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo "[INFO] 后端服务已停止 (PID: $BACKEND_PID)"
    else
        echo "[INFO] 后端服务未运行"
    fi
    rm -f logs/backend.pid
else
    echo "[INFO] 未找到后端服务PID文件"
fi

if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo "[INFO] 前端服务已停止 (PID: $FRONTEND_PID)"
    else
        echo "[INFO] 前端服务未运行"
    fi
    rm -f logs/frontend.pid
else
    echo "[INFO] 未找到前端服务PID文件"
fi

# 强制停止可能残留的进程
pkill -f "python main.py" 2>/dev/null
pkill -f "npm start" 2>/dev/null

echo "[SUCCESS] 所有服务已停止" 