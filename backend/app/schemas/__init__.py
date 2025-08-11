"""
Pydantic数据模型定义
"""
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, Literal
from uuid import UUID
import re

# Optional EmailStr: fall back to str with regex validation if email-validator isn't installed
try:
    import email_validator  # type: ignore  # noqa: F401
    from pydantic import EmailStr as PydanticEmailStr
    EmailType = PydanticEmailStr
    _USE_REGEX_EMAIL_VALIDATION = False
except Exception:
    EmailType = str
    _USE_REGEX_EMAIL_VALIDATION = True


# ============ 用户相关模型 ============
class UserBase(BaseModel):
    """用户基础模型"""
    email: EmailType

    # When email-validator isn't available, validate with a conservative regex
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str):
        if not _USE_REGEX_EMAIL_VALIDATION:
            return v
        # Simple RFC5322-ish regex; not perfect, but reasonable fallback
        pattern = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
        if not isinstance(v, str) or not pattern.match(v):
            raise ValueError("Invalid email format")
        return v


class UserCreate(UserBase):
    """用户创建模型"""
    password: str


class UserLogin(UserBase):
    """用户登录模型"""
    password: str


class User(UserBase):
    """用户响应模型"""
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """认证令牌模型"""
    access_token: str
    token_type: str = "bearer"
    user: User


# ============ 时空信箱相关模型 ============
class TimeCapsuleBase(BaseModel):
    """时空信箱基础模型"""
    title: str
    content: str
    unlock_date: Optional[datetime] = None
    unlock_condition: Optional[str] = None
    is_public: bool = False


class TimeCapsuleCreate(TimeCapsuleBase):
    """创建时空信箱模型"""
    pass


class TimeCapsuleUpdate(BaseModel):
    """更新时空信箱模型"""
    title: Optional[str] = None
    content: Optional[str] = None
    unlock_date: Optional[datetime] = None
    unlock_condition: Optional[str] = None
    is_public: Optional[bool] = None
    status: Optional[Literal["locked", "unlocked", "public"]] = None


class TimeCapsule(TimeCapsuleBase):
    """时空信箱响应模型"""
    id: UUID
    user_id: UUID
    status: Literal["locked", "unlocked", "public"]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ============ 回音壁相关模型 ============
class EchoWallBase(BaseModel):
    """回音壁基础模型"""
    content: str
    emotion_tag: Optional[str] = None


class EchoWallCreate(EchoWallBase):
    """创建回音壁消息模型"""
    pass


class EchoWall(EchoWallBase):
    """回音壁响应模型"""
    id: UUID
    user_id: UUID
    is_matched: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ 情感匹配相关模型 ============
class EchoMatchBase(BaseModel):
    """情感匹配基础模型"""
    echo_id: UUID
    matched_echo_id: UUID


class EchoMatchCreate(EchoMatchBase):
    """创建匹配模型"""
    pass


class EchoMatch(EchoMatchBase):
    """匹配响应模型"""
    id: UUID
    matched_at: datetime
    echo: Optional[EchoWall] = None
    matched_echo: Optional[EchoWall] = None
    
    class Config:
        from_attributes = True


# ============ 通用响应模型 ============
class MessageResponse(BaseModel):
    """通用消息响应"""
    message: str
    success: bool = True
    data: Optional[dict] = None