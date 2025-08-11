"""
回音壁API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
import random
from datetime import datetime, timedelta
from app.schemas import (
    EchoWall,
    EchoWallCreate,
    EchoMatch,
    MessageResponse
)
from app.core.auth import get_current_user_id
from app.core.database import get_supabase_client

router = APIRouter(prefix="/echo-wall", tags=["回音壁"])


# 情感标签及其相关/对应标签
EMOTION_MATCHES = {
    "lonely": ["understanding", "companionship", "warm"],
    "sad": ["comfort", "hope", "encouragement"],
    "anxious": ["calm", "peace", "reassurance"],
    "happy": ["joy", "celebration", "gratitude"],
    "nostalgic": ["memories", "understanding", "shared"],
    "confused": ["clarity", "guidance", "support"],
    "hopeful": ["inspiration", "dreams", "possibility"],
    "grateful": ["appreciation", "kindness", "blessing"],
    "love": ["affection", "care", "connection"],
    "regret": ["forgiveness", "acceptance", "growth"]
}


def analyze_emotion(content: str) -> str:
    """简单的情感分析，返回情感标签"""
    # 定义关键词映射
    emotion_keywords = {
        "lonely": ["孤独", "寂寞", "一个人", "孤单", "无人"],
        "sad": ["难过", "伤心", "悲伤", "哭", "痛苦"],
        "anxious": ["焦虑", "紧张", "不安", "担心", "害怕"],
        "happy": ["开心", "快乐", "幸福", "高兴", "愉快"],
        "nostalgic": ["怀念", "想念", "回忆", "从前", "过去"],
        "confused": ["迷茫", "困惑", "不知道", "疑惑", "不明白"],
        "hopeful": ["希望", "期待", "愿望", "梦想", "未来"],
        "grateful": ["感谢", "感恩", "谢谢", "感激", "珍惜"],
        "love": ["爱", "喜欢", "心动", "情", "恋"],
        "regret": ["后悔", "遗憾", "错过", "可惜", "懊悔"]
    }
    
    # 计算每个情感的匹配度
    emotion_scores = {}
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for keyword in keywords if keyword in content)
        if score > 0:
            emotion_scores[emotion] = score
    
    # 返回得分最高的情感，如果没有匹配则返回"neutral"
    if emotion_scores:
        return max(emotion_scores, key=emotion_scores.get)
    return "neutral"


def find_matching_emotion(emotion_tag: str) -> List[str]:
    """找到匹配的情感标签"""
    if emotion_tag in EMOTION_MATCHES:
        return EMOTION_MATCHES[emotion_tag]
    
    # 反向查找
    for key, values in EMOTION_MATCHES.items():
        if emotion_tag in values:
            return [key] + [v for v in values if v != emotion_tag]
    
    # 如果没有特定匹配，返回所有可能的标签
    return list(EMOTION_MATCHES.keys())


@router.post("/", response_model=EchoWall)
async def create_echo(
    echo: EchoWallCreate,
    user_id: UUID = Depends(get_current_user_id)
):
    """发送一个呼喊到回音壁"""
    supabase = get_supabase_client()
    
    # 如果没有提供情感标签，进行简单的情感分析
    emotion_tag = echo.emotion_tag
    if not emotion_tag:
        emotion_tag = analyze_emotion(echo.content)
    
    # 准备数据
    data = {
        "content": echo.content,
        "emotion_tag": emotion_tag,
        "user_id": str(user_id),
        "is_matched": False
    }
    
    try:
        response = supabase.table("echo_wall").insert(data).execute()
        created_echo = response.data[0]
        
        # 异步尝试匹配（这里简化处理，实际可以用后台任务）
        await try_match_echo(created_echo["id"], emotion_tag, str(user_id))
        
        return created_echo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"发送呼喊失败: {str(e)}"
        )


async def try_match_echo(echo_id: str, emotion_tag: str, user_id: str):
    """尝试为新的呼喊找到匹配"""
    supabase = get_supabase_client()
    
    try:
        # 找到可以匹配的情感标签
        matching_emotions = find_matching_emotion(emotion_tag)
        
        # 查找可匹配的回音（不是自己的，未被匹配的）
        potential_matches = []
        for emotion in matching_emotions:
            response = (
                supabase.table("echo_wall")
                .select("*")
                .eq("emotion_tag", emotion)
                .eq("is_matched", False)
                .neq("user_id", user_id)
                .neq("id", echo_id)
                .limit(10)
                .execute()
            )
            potential_matches.extend(response.data)
        
        if potential_matches:
            # 随机选择一个进行匹配
            matched_echo = random.choice(potential_matches)
            
            # 创建匹配记录
            match_data = {
                "echo_id": echo_id,
                "matched_echo_id": matched_echo["id"]
            }
            supabase.table("echo_matches").insert(match_data).execute()
            
            # 更新两个回音的匹配状态
            supabase.table("echo_wall").update({"is_matched": True}).eq("id", echo_id).execute()
            supabase.table("echo_wall").update({"is_matched": True}).eq("id", matched_echo["id"]).execute()
            
    except Exception as e:
        # 匹配失败不影响主流程
        print(f"匹配失败: {str(e)}")


@router.get("/my-echoes", response_model=List[EchoWall])
async def get_my_echoes(
    user_id: UUID = Depends(get_current_user_id)
):
    """获取我的所有呼喊"""
    supabase = get_supabase_client()
    
    try:
        response = (
            supabase.table("echo_wall")
            .select("*")
            .eq("user_id", str(user_id))
            .order("created_at", desc=True)
            .execute()
        )
        return response.data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"获取呼喊失败: {str(e)}"
        )


@router.get("/my-matches", response_model=List[EchoMatch])
async def get_my_matches(
    user_id: UUID = Depends(get_current_user_id)
):
    """获取我的回音匹配"""
    supabase = get_supabase_client()
    
    try:
        # 先获取用户的所有呼喊
        echo_response = (
            supabase.table("echo_wall")
            .select("id")
            .eq("user_id", str(user_id))
            .execute()
        )
        
        if not echo_response.data:
            return []
        
        echo_ids = [echo["id"] for echo in echo_response.data]
        
        # 获取所有相关的匹配
        matches = []
        
        # 作为echo_id的匹配
        for echo_id in echo_ids:
            response = (
                supabase.table("echo_matches")
                .select("*, echo_wall!echo_matches_echo_id_fkey(*), echo_wall!echo_matches_matched_echo_id_fkey(*)")
                .eq("echo_id", echo_id)
                .execute()
            )
            matches.extend(response.data)
        
        # 作为matched_echo_id的匹配
        for echo_id in echo_ids:
            response = (
                supabase.table("echo_matches")
                .select("*, echo_wall!echo_matches_echo_id_fkey(*), echo_wall!echo_matches_matched_echo_id_fkey(*)")
                .eq("matched_echo_id", echo_id)
                .execute()
            )
            matches.extend(response.data)
        
        # 去重并格式化
        seen = set()
        unique_matches = []
        for match in matches:
            if match["id"] not in seen:
                seen.add(match["id"])
                # 格式化响应
                formatted_match = {
                    "id": match["id"],
                    "echo_id": match["echo_id"],
                    "matched_echo_id": match["matched_echo_id"],
                    "matched_at": match["matched_at"]
                }
                unique_matches.append(formatted_match)
        
        return unique_matches
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"获取匹配失败: {str(e)}"
        )


@router.get("/recent", response_model=List[EchoWall])
async def get_recent_echoes(limit: int = 20):
    """获取最近的回音（公共展示）"""
    supabase = get_supabase_client()
    
    try:
        # 获取最近24小时内的回音
        time_threshold = (datetime.utcnow() - timedelta(hours=24)).isoformat()
        
        response = (
            supabase.table("echo_wall")
            .select("*")
            .gte("created_at", time_threshold)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        
        # 匿名化处理 - 移除user_id
        echoes = response.data
        for echo in echoes:
            echo["user_id"] = None  # 匿名化
        
        return echoes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"获取最近回音失败: {str(e)}"
        )


@router.get("/emotions", response_model=List[dict])
async def get_emotion_tags():
    """获取所有可用的情感标签"""
    tags = []
    
    # 主要情感
    for emotion in EMOTION_MATCHES.keys():
        tags.append({
            "value": emotion,
            "label": emotion.title(),
            "type": "primary"
        })
    
    # 相关情感
    all_related = set()
    for related_list in EMOTION_MATCHES.values():
        all_related.update(related_list)
    
    for emotion in all_related:
        if emotion not in EMOTION_MATCHES:
            tags.append({
                "value": emotion,
                "label": emotion.title(),
                "type": "secondary"
            })
    
    # 中性
    tags.append({
        "value": "neutral",
        "label": "Neutral",
        "type": "default"
    })
    
    return tags


@router.post("/manual-match", response_model=MessageResponse)
async def create_manual_match(
    echo_id: UUID,
    matched_echo_id: UUID,
    user_id: UUID = Depends(get_current_user_id)
):
    """手动创建一个匹配（用于测试或特殊情况）"""
    supabase = get_supabase_client()
    
    # 验证两个回音都存在且至少有一个属于当前用户
    try:
        echo1 = supabase.table("echo_wall").select("*").eq("id", str(echo_id)).single().execute()
        echo2 = supabase.table("echo_wall").select("*").eq("id", str(matched_echo_id)).single().execute()
        
        if str(echo1.data["user_id"]) != str(user_id) and str(echo2.data["user_id"]) != str(user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权创建此匹配"
            )
        
        # 创建匹配
        match_data = {
            "echo_id": str(echo_id),
            "matched_echo_id": str(matched_echo_id)
        }
        supabase.table("echo_matches").insert(match_data).execute()
        
        # 更新匹配状态
        supabase.table("echo_wall").update({"is_matched": True}).eq("id", str(echo_id)).execute()
        supabase.table("echo_wall").update({"is_matched": True}).eq("id", str(matched_echo_id)).execute()
        
        return MessageResponse(
            message="匹配创建成功",
            success=True,
            data={"echo_id": str(echo_id), "matched_echo_id": str(matched_echo_id)}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"创建匹配失败: {str(e)}"
        )