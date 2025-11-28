from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import router as api_router
from app.core.maimai_client import maimai_client
from app.core.database import init_db
from loguru import logger
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入爬虫管理器
from wumeng_crawler.spiders.spider_manager import get_spider_manager

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
init_db()

# 初始化爬虫管理器
logger.info("初始化爬虫管理器")
spider_manager = get_spider_manager()
logger.info(f"爬虫管理器初始化完成，共初始化 {len(spider_manager)} 个爬虫")

# 包含API路由
app.include_router(api_router, prefix="/api")

# 根路径
@app.get("/")
def root():
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "spiders_initialized": len(spider_manager)
    }

# 健康检查
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "wumengbot-backend",
        "spiders_initialized": len(spider_manager)
    }
