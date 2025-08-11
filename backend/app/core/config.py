"""
配置文件 - 从环境变量加载应用配置
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置设置"""
    # Supabase配置
    supabase_url: str
    supabase_anon_key: str
    
    # JWT配置
    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 应用配置
    app_name: str = "Echo"
    app_version: str = "1.0.0"
    debug: bool = True
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """获取应用配置单例"""
    return Settings()