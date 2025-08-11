"""
Supabase客户端初始化
"""
from supabase import create_client, Client
from app.core.config import get_settings

settings = get_settings()


def get_supabase_client() -> Client:
    """获取Supabase客户端实例"""
    return create_client(
        settings.supabase_url,
        settings.supabase_anon_key
    )