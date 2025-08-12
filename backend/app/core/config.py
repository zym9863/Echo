"""
配置文件 - 从环境变量加载应用配置
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置设置"""
    # Supabase配置
    supabase_url: str
    supabase_anon_key: str
    # 可选：服务角色密钥（用于后端服务端访问，绕过RLS）
    supabase_service_role_key: str | None = None

    # JWT配置
    secret_key: str = "change-this-secret-key-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # 应用配置
    app_name: str = "Echo"
    app_version: str = "1.0.0"
    debug: bool = True

    # Pydantic Settings v2 配置
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings() -> "Settings":
    """获取应用配置单例"""
    return Settings()
