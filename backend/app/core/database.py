from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from loguru import logger

# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # 在调试模式下打印SQL语句
    pool_pre_ping=True,  # 连接池预检查
    pool_recycle=3600,  # 连接池回收时间
    pool_size=10,  # 连接池大小
    max_overflow=20  # 连接池最大溢出数量
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

# 获取数据库会话
def get_db():
    """
    获取数据库会话
    
    Yields:
        db: 数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 初始化数据库
def init_db():
    """
    初始化数据库，创建所有表
    """
    logger.info("初始化数据库")
    
    try:
        # 导入所有模型，确保Base.metadata包含所有表的定义
        from app.models import UserSegamaid, CrawledData
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        
        logger.info("数据库初始化完成，所有表已创建")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise e

# 关闭数据库连接
def close_db():
    """
    关闭数据库连接
    """
    logger.info("关闭数据库连接")
    engine.dispose()
    logger.info("数据库连接已关闭")