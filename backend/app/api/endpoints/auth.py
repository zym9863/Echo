"""
用户认证API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.schemas import UserCreate, UserLogin, User, Token, MessageResponse
from app.core.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from app.core.config import get_settings
from app.core.database import get_supabase_client

router = APIRouter(prefix="/auth", tags=["认证"])
settings = get_settings()


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """用户注册"""
    supabase = get_supabase_client()
    
    try:
        # 使用Supabase Auth创建用户
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })
        
        if response.user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="注册失败，可能邮箱已被使用"
            )
        
        # 创建访问令牌
        access_token = create_access_token(
            data={"sub": str(response.user.id)},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        # 返回用户信息和令牌
        user = User(
            id=response.user.id,
            email=response.user.email,
            created_at=response.user.created_at
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"注册失败: {str(e)}"
        )


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录"""
    supabase = get_supabase_client()
    
    try:
        # 使用Supabase Auth登录
        response = supabase.auth.sign_in_with_password({
            "email": form_data.username,  # OAuth2PasswordRequestForm使用username字段
            "password": form_data.password
        })
        
        if response.user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # 创建访问令牌
        access_token = create_access_token(
            data={"sub": str(response.user.id)},
            expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
        )
        
        # 返回用户信息和令牌
        user = User(
            id=response.user.id,
            email=response.user.email,
            created_at=response.user.created_at
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="登录失败，请检查邮箱和密码",
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/logout", response_model=MessageResponse)
async def logout(current_user=Depends(get_current_user)):
    """用户登出"""
    supabase = get_supabase_client()
    
    try:
        # Supabase登出
        supabase.auth.sign_out()
        
        return MessageResponse(
            message="登出成功",
            success=True
        )
    except Exception as e:
        # 即使登出失败也返回成功（前端会清除令牌）
        return MessageResponse(
            message="登出成功",
            success=True
        )


@router.get("/me", response_model=User)
async def get_me(current_user=Depends(get_current_user)):
    """获取当前用户信息"""
    return User(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user=Depends(get_current_user)):
    """刷新访问令牌"""
    # 创建新的访问令牌
    access_token = create_access_token(
        data={"sub": str(current_user.id)},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    user = User(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    old_password: str,
    new_password: str,
    current_user=Depends(get_current_user)
):
    """修改密码"""
    supabase = get_supabase_client()
    
    # 验证旧密码
    try:
        # 尝试用旧密码登录来验证
        supabase.auth.sign_in_with_password({
            "email": current_user.email,
            "password": old_password
        })
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="原密码错误"
        )
    
    # 更新密码
    try:
        response = supabase.auth.update_user({
            "password": new_password
        })
        
        if response.user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="密码修改失败"
            )
        
        return MessageResponse(
            message="密码修改成功",
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"密码修改失败: {str(e)}"
        )


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(email: str):
    """发送密码重置邮件"""
    supabase = get_supabase_client()
    
    try:
        # 发送密码重置邮件
        supabase.auth.reset_password_email(email)
        
        return MessageResponse(
            message="密码重置邮件已发送，请查收",
            success=True
        )
    except Exception as e:
        # 为了安全，不暴露邮箱是否存在
        return MessageResponse(
            message="如果该邮箱已注册，密码重置邮件将会发送",
            success=True
        )