from pydantic_settings import BaseSettings
from typing import List, Union, Any

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "WumengBot"
    app_version: str = "1.0.0"
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
