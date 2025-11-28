from pydantic_settings import BaseSettings
from typing import List, Union, Any, Dict

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "WumengBot"
    app_version: str = "1.5.0"
    debug: bool = True
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000
    
    # 数据库配置
    database_url: str = "sqlite:///./wumengbot.db"
    
    # Redis配置
    redis_url: str = "redis://localhost:6379/0"
    
    # maimai.py配置
    divingfish_token: str = ""
    lxns_token: str = ""
    
    # CORS配置
    cors_origins: Union[str, List[str]] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # 爬虫配置
    # 基本配置
    spider_enabled: bool = True
    spider_concurrent_requests: int = 4
    spider_request_timeout: int = 30
    spider_retry_times: int = 3
    spider_retry_delay: int = 5
    spider_download_delay: float = 1.0
    spider_randomize_download_delay: bool = True
    spider_robotstxt_obey: bool = True
    
    # 代理配置
    spider_proxy_enabled: bool = False
    spider_proxy_url: str = "http://localhost:8888"
    
    # 目标网站配置
    spider_target_sites: List[Dict[str, Any]] = [
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
    ]
    
    # 调度配置
    spider_schedule: Dict[str, Dict[str, Any]] = {
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
    }
    
    # 数据处理配置
    spider_data_processing: Dict[str, Any] = {
        "remove_duplicates": True,
        "fill_missing_values": True,
        "validate_data": True,
        "standardize_format": True,
        "merge_sources": True,
        "resolve_conflicts": True,
        "create_relationships": True
    }
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "cors_origins":
                # 处理逗号分隔的字符串
                if isinstance(raw_val, str):
                    return [origin.strip() for origin in raw_val.split(",") if origin.strip()]
            return raw_val

# 确保cors_origins是列表类型
settings = Settings()
if isinstance(settings.cors_origins, str):
    settings.cors_origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
