import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Groq API配置
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama3-8b-8192"

# 数据库配置（从database/config.py导入）
import sys
sys.path.append('database')
from database.config import get_database_config

DATABASE_CONFIG = get_database_config()

# API配置
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True 