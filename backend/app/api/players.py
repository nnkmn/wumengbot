from fastapi import APIRouter, HTTPException
from maimai_py import PlayerIdentifier
from app.core.maimai_client import maimai_client, divingfish_provider, lxns_provider

router = APIRouter()

@router.get("/search")
async def search_player(username: str = None, friend_code: str = None, provider: str = "divingfish"):
    """
    搜索玩家信息
    
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
        
        # 获取玩家信息
        player = await maimai_client.players(identifier, provider=selected_provider)
        
        # 返回简单的玩家信息
        return {
            "username": getattr(player, "username", None),
            "friend_code": getattr(player, "friend_code", None),
            "rating": getattr(player, "rating", None),
            "title": getattr(player, "title", None)
        }
    except Exception as e:
        import traceback
        print(f"搜索玩家信息失败: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"搜索玩家信息失败: {str(e)}")
