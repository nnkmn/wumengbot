from fastapi import APIRouter, HTTPException
from dataclasses import asdict
from maimai_py import PlayerIdentifier
from app.core.maimai_client import maimai_client, divingfish_provider, lxns_provider

router = APIRouter()

@router.get("/player")
async def get_player_scores(username: str = None, friend_code: str = None, provider: str = "divingfish"):
    """
    获取玩家成绩
    
    - username: 用户名（水鱼查分器）
    - friend_code: 好友码（落雪查分器）
    - provider: 数据源，可选值：divingfish, lxns
    """
    try:
        if username:
            identifier = PlayerIdentifier(username=username)
        elif friend_code:
            identifier = PlayerIdentifier(friend_code=friend_code)
        else:
            raise HTTPException(status_code=400, detail="必须提供username或friend_code")
        
        # 选择数据源
        if provider == "divingfish":
            selected_provider = divingfish_provider
        elif provider == "lxns":
            selected_provider = lxns_provider
        else:
            raise HTTPException(status_code=400, detail="不支持的数据源")
        
        # 获取玩家成绩
        scores = await maimai_client.scores(identifier, provider=selected_provider)
        
        # 简单序列化scores_b15
        simple_scores_b15 = []
        for score in scores.scores_b15:
            simple_scores_b15.append({
                "title": getattr(score, "title", None),
                "level": getattr(score, "level", None),
                "score": getattr(score, "score", None),
                "fc": getattr(score, "fc", None),
                "fs": getattr(score, "fs", None)
            })
        
        # 简单序列化scores_all
        simple_scores_all = []
        for score in scores.scores_all[:10]:  # 只返回前10条成绩
            simple_scores_all.append({
                "title": getattr(score, "title", None),
                "level": getattr(score, "level", None),
                "score": getattr(score, "score", None),
                "fc": getattr(score, "fc", None),
                "fs": getattr(score, "fs", None)
            })
        
        return {
            "rating": scores.rating,
            "scores_b15": simple_scores_b15,
            "scores_all": simple_scores_all
        }
    except Exception as e:
        import traceback
        print(f"获取玩家成绩失败: {e}")
        print(traceback.format_exc())
        
        # 处理不同类型的错误
        if "KeyError" in str(type(e)) and "message" in str(e):
            raise HTTPException(status_code=400, detail="玩家不存在或数据源错误")
        else:
            raise HTTPException(status_code=500, detail=f"获取玩家成绩失败: {str(e)}")
