import os
from dotenv import load_dotenv
from loguru import logger

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 日志配置
logger.add(
    os.path.join(BASE_DIR, "logs", "wumeng_crawler.log"),
    rotation="1 day",
    retention="7 days",
    compression="zip",
    level="INFO"
)

# 数据库配置
DATABASE_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "wumeng_crawler"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres")
}

# Redis配置
REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": int(os.getenv("REDIS_PORT", "6379")),
    "db": int(os.getenv("REDIS_DB", "0")),
    "password": os.getenv("REDIS_PASSWORD", "")
}

# 爬虫配置
SPIDER_CONFIG = {
    # 目标网站配置
    "TARGET_SITES": [
        {
            "ip": "129.28.248.89",
            "domain": "wq.sys-all.cn",
            "name": "wq",
            "enabled": True
        },
        {
            "ip": "81.71.193.236",
            "domain": "ai.sys-all.cn",
            "name": "ai",
            "enabled": True
        },
        {
            "ip": "42.193.74.107",
            "domain": "wi.sys-all.cn",
            "name": "wi",
            "enabled": True
        },
        {
            "ip": "81.70.119.195",
            "domain": "at.sys-all.cn",
            "name": "at",
            "enabled": True
        }
    ],
    
    # 爬取间隔（秒）
    "CRAWL_INTERVAL": int(os.getenv("CRAWL_INTERVAL", "300")),
    
    # 并发请求数
    "CONCURRENT_REQUESTS": int(os.getenv("CONCURRENT_REQUESTS", "16")),
    
    # 请求超时（秒）
    "REQUEST_TIMEOUT": int(os.getenv("REQUEST_TIMEOUT", "30")),
    
    # 重试次数
    "RETRY_TIMES": int(os.getenv("RETRY_TIMES", "3")),
    
    # 重试延迟（秒）
    "RETRY_DELAY": int(os.getenv("RETRY_DELAY", "5")),
    
    # 用户代理池
    "USER_AGENT_POOL": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/119.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ],
    
    # 代理配置
    "PROXY_ENABLED": os.getenv("PROXY_ENABLED", "false").lower() == "true",
    "PROXY_URL": os.getenv("PROXY_URL", "http://localhost:8888"),
    
    # Robots.txt配置
    "ROBOTSTXT_OBEY": os.getenv("ROBOTSTXT_OBEY", "true").lower() == "true",
    
    # 下载延迟（秒）
    "DOWNLOAD_DELAY": float(os.getenv("DOWNLOAD_DELAY", "1.0")),
    
    # 随机下载延迟
    "RANDOMIZE_DOWNLOAD_DELAY": os.getenv("RANDOMIZE_DOWNLOAD_DELAY", "true").lower() == "true"
}

# 调度配置
SCHEDULER_CONFIG = {
    # 任务调度配置
    "TASK_SCHEDULE": {
        "wq_spider": {
            "cron": "*/5 * * * *",  # 每5分钟执行一次
            "enabled": True
        },
        "ai_spider": {
            "cron": "*/10 * * * *",  # 每10分钟执行一次
            "enabled": True
        },
        "wi_spider": {
            "cron": "*/15 * * * *",  # 每15分钟执行一次
            "enabled": True
        },
        "at_spider": {
            "cron": "*/20 * * * *",  # 每20分钟执行一次
            "enabled": True
        }
    },
    
    # 并发任务数
    "CONCURRENT_TASKS": int(os.getenv("CONCURRENT_TASKS", "4")),
    
    # 任务队列名称
    "TASK_QUEUE_NAME": os.getenv("TASK_QUEUE_NAME", "wumeng_crawler_tasks")
}

# API配置
API_CONFIG = {
    "host": os.getenv("API_HOST", "0.0.0.0"),
    "port": int(os.getenv("API_PORT", "8000")),
    "debug": os.getenv("API_DEBUG", "false").lower() == "true"
}

# 数据处理配置
PROCESSOR_CONFIG = {
    # 数据清洗配置
    "CLEANING_CONFIG": {
        "remove_duplicates": True,
        "fill_missing_values": True,
        "validate_data": True,
        "standardize_format": True
    },
    
    # 数据整合配置
    "INTEGRATION_CONFIG": {
        "merge_sources": True,
        "resolve_conflicts": True,
        "create_relationships": True
    },
    
    # 数据格式化配置
    "FORMATTING_CONFIG": {
        "json_format": True,
        "csv_format": True,
        "database_format": True
    }
}

# 监控配置
MONITOR_CONFIG = {
    # 监控指标配置
    "METRICS_CONFIG": {
        "spider_metrics": True,
        "processor_metrics": True,
        "storage_metrics": True,
        "api_metrics": True
    },
    
    # 告警配置
    "ALERT_CONFIG": {
        "enabled": os.getenv("ALERT_ENABLED", "false").lower() == "true",
        "thresholds": {
            "spider_failure_rate": 0.1,  # 爬虫失败率阈值
            "processor_error_rate": 0.05,  # 处理器错误率阈值
            "storage_latency": 1.0  # 存储延迟阈值（秒）
        },
        "notification_channels": ["email", "slack"]
    }
}

# 导出配置
EXPORT_CONFIG = {
    # 导出格式配置
    "FORMATS": ["json", "csv", "excel"],
    
    # 导出路径
    "EXPORT_PATH": os.path.join(BASE_DIR, "exports"),
    
    # 导出频率
    "EXPORT_FREQUENCY": os.getenv("EXPORT_FREQUENCY", "daily"),  # daily, weekly, monthly
    
    # 保留期限
    "RETENTION_PERIOD": int(os.getenv("RETENTION_PERIOD", "30"))  # 30天
}

# 安全配置
SECURITY_CONFIG = {
    # CORS配置
    "CORS_CONFIG": {
        "allow_origins": ["*"],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"]
    },
    
    # API密钥配置
    "API_KEYS": {
        "enabled": os.getenv("API_KEYS_ENABLED", "false").lower() == "true",
        "keys": os.getenv("API_KEYS", "").split(",")
    }
}

# 日志配置
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
    "datefmt": os.getenv("LOG_DATEFMT", "%Y-%m-%d %H:%M:%S")
}

# 版本信息
VERSION = "1.0.0"
AUTHOR = "Wumeng Crawler Team"
DESCRIPTION = "舞萌数据爬取系统"

# 打印配置信息
logger.info(f"项目根目录: {BASE_DIR}")
logger.info(f"数据库配置: {DATABASE_CONFIG}")
logger.info(f"Redis配置: {REDIS_CONFIG}")
logger.info(f"API配置: {API_CONFIG}")
logger.info(f"爬虫配置: {SPIDER_CONFIG}")
logger.info(f"调度配置: {SCHEDULER_CONFIG}")
logger.info(f"监控配置: {MONITOR_CONFIG}")
logger.info(f"版本信息: {VERSION}")
logger.info(f"作者: {AUTHOR}")
logger.info(f"描述: {DESCRIPTION}")

# 导出配置
__all__ = [
    "BASE_DIR",
    "DATABASE_CONFIG",
    "REDIS_CONFIG",
    "SPIDER_CONFIG",
    "SCHEDULER_CONFIG",
    "API_CONFIG",
    "PROCESSOR_CONFIG",
    "MONITOR_CONFIG",
    "EXPORT_CONFIG",
    "SECURITY_CONFIG",
    "LOGGING_CONFIG",
    "VERSION",
    "AUTHOR",
    "DESCRIPTION"
]