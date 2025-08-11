"""
时空信箱API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.schemas import (
    TimeCapsule, 
    TimeCapsuleCreate, 
    TimeCapsuleUpdate,
    MessageResponse
)
from app.core.auth import get_current_user_id
from app.core.database import get_supabase_client

router = APIRouter(prefix="/time-capsules", tags=["时空信箱"])


@router.post("/", response_model=TimeCapsule)
async def create_time_capsule(
    capsule: TimeCapsuleCreate,
    user_id: UUID = Depends(get_current_user_id)
):
    """创建新的时空信箱"""
    supabase = get_supabase_client()
    
    # 准备数据
    capsule_data = capsule.dict()
    # 将datetime对象转换为ISO格式字符串
    if capsule_data.get("unlock_date"):
        capsule_data["unlock_date"] = capsule_data["unlock_date"].isoformat()
    
    data = {
        **capsule_data,
        "user_id": str(user_id),
        "status": "locked"
    }
    
    try:
        response = supabase.table("time_capsules").insert(data).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"创建时空信箱失败: {str(e)}"
        )


@router.get("/", response_model=List[TimeCapsule])
async def get_my_capsules(
    user_id: UUID = Depends(get_current_user_id),
    status: Optional[str] = None
):
    """获取我的时空信箱列表"""
    supabase = get_supabase_client()
    
    try:
        query = supabase.table("time_capsules").select("*").eq("user_id", str(user_id))
        if status:
            query = query.eq("status", status)
        response = query.order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"获取时空信箱失败: {str(e)}"
        )


@router.get("/public", response_model=List[TimeCapsule])
async def get_public_capsules():
    """获取公开的时空信箱（回音廊）"""
    supabase = get_supabase_client()
    
    try:
        response = (
            supabase.table("time_capsules")
            .select("*")
            .eq("is_public", True)
            .eq("status", "public")
            .order("updated_at", desc=True)
            .limit(50)
            .execute()
        )
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"获取公开信箱失败: {str(e)}"
        )


@router.get("/{capsule_id}", response_model=TimeCapsule)
async def get_capsule(
    capsule_id: UUID,
    user_id: UUID = Depends(get_current_user_id)
):
    """获取特定的时空信箱"""
    supabase = get_supabase_client()
    
    try:
        response = (
            supabase.table("time_capsules")
            .select("*")
            .eq("id", str(capsule_id))
            .single()
            .execute()
        )
        
        capsule = response.data
        
        # 检查权限：只能查看自己的信箱或公开的信箱
        if str(capsule["user_id"]) != str(user_id) and not (
            capsule["is_public"] and capsule["status"] == "public"
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权访问此时空信箱"
            )
        
        return capsule
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"时空信箱不存在: {str(e)}"
        )


@router.put("/{capsule_id}", response_model=TimeCapsule)
async def update_capsule(
    capsule_id: UUID,
    capsule_update: TimeCapsuleUpdate,
    user_id: UUID = Depends(get_current_user_id)
):
    """更新时空信箱"""
    supabase = get_supabase_client()
    
    # 检查信箱是否存在且属于当前用户
    try:
        existing = (
            supabase.table("time_capsules")
            .select("*")
            .eq("id", str(capsule_id))
            .eq("user_id", str(user_id))
            .single()
            .execute()
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="时空信箱不存在或无权修改"
        )
    
    # 更新数据
    update_data = capsule_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    try:
        response = (
            supabase.table("time_capsules")
            .update(update_data)
            .eq("id", str(capsule_id))
            .execute()
        )
        return response.data[0]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"更新时空信箱失败: {str(e)}"
        )


@router.post("/{capsule_id}/unlock", response_model=MessageResponse)
async def unlock_capsule(
    capsule_id: UUID,
    user_id: UUID = Depends(get_current_user_id)
):
    """解锁时空信箱"""
    supabase = get_supabase_client()
    
    # 获取信箱信息
    try:
        response = (
            supabase.table("time_capsules")
            .select("*")
            .eq("id", str(capsule_id))
            .eq("user_id", str(user_id))
            .single()
            .execute()
        )
        capsule = response.data
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="时空信箱不存在或无权操作"
        )
    
    # 检查解锁条件
    if capsule["status"] != "locked":
        return MessageResponse(message="时空信箱已经解锁")
    
    can_unlock = False
    unlock_message = ""
    
    # 检查时间条件
    if capsule["unlock_date"]:
        unlock_date = datetime.fromisoformat(capsule["unlock_date"].replace("Z", "+00:00"))
        if datetime.utcnow() >= unlock_date:
            can_unlock = True
            unlock_message = "时间已到，信箱解锁成功"
        else:
            unlock_message = f"时间未到，请等到 {unlock_date.strftime('%Y-%m-%d %H:%M')} 后再试"
    
    # 如果有特殊条件，这里可以添加更多逻辑
    if capsule["unlock_condition"] and not can_unlock:
        # 这里可以根据具体条件判断
        # 暂时只做示例
        unlock_message = f"解锁条件：{capsule['unlock_condition']}"
    
    if can_unlock:
        # 更新状态为解锁
        try:
            supabase.table("time_capsules").update({
                "status": "unlocked",
                "updated_at": datetime.utcnow().isoformat()
            }).eq("id", str(capsule_id)).execute()
            
            return MessageResponse(
                message=unlock_message,
                success=True,
                data={"capsule_id": str(capsule_id)}
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"解锁失败: {str(e)}"
            )
    else:
        return MessageResponse(
            message=unlock_message,
            success=False
        )


@router.post("/{capsule_id}/publish", response_model=MessageResponse)
async def publish_capsule(
    capsule_id: UUID,
    user_id: UUID = Depends(get_current_user_id)
):
    """将时空信箱发布到公共回音廊"""
    supabase = get_supabase_client()
    
    # 检查信箱是否存在且属于当前用户
    try:
        response = (
            supabase.table("time_capsules")
            .select("*")
            .eq("id", str(capsule_id))
            .eq("user_id", str(user_id))
            .single()
            .execute()
        )
        capsule = response.data
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="时空信箱不存在或无权操作"
        )
    
    # 只有解锁的信箱才能发布
    if capsule["status"] != "unlocked":
        return MessageResponse(
            message="只有解锁的信箱才能发布到公共回音廊",
            success=False
        )
    
    # 更新为公开状态
    try:
        supabase.table("time_capsules").update({
            "status": "public",
            "is_public": True,
            "updated_at": datetime.utcnow().isoformat()
        }).eq("id", str(capsule_id)).execute()
        
        return MessageResponse(
            message="成功发布到公共回音廊",
            success=True,
            data={"capsule_id": str(capsule_id)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"发布失败: {str(e)}"
        )


@router.delete("/{capsule_id}", response_model=MessageResponse)
async def delete_capsule(
    capsule_id: UUID,
    user_id: UUID = Depends(get_current_user_id)
):
    """删除时空信箱"""
    supabase = get_supabase_client()
    
    try:
        # 只能删除自己的信箱
        response = (
            supabase.table("time_capsules")
            .delete()
            .eq("id", str(capsule_id))
            .eq("user_id", str(user_id))
            .execute()
        )
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="时空信箱不存在或无权删除"
            )
        
        return MessageResponse(
            message="时空信箱已删除",
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"删除失败: {str(e)}"
        )