"""
Supabase客户端初始化
"""
from supabase import create_client, Client
from app.core.config import get_settings

settings = get_settings()


def get_supabase_client() -> Client:
    """获取Supabase客户端实例

    优先使用服务角色密钥（如果提供），以确保服务端在RLS开启的环境下
    拥有必要的读写权限。否则退回到anon key。
    """
    key = settings.supabase_service_role_key or settings.supabase_anon_key
    return create_client(
        settings.supabase_url,
        key
    )