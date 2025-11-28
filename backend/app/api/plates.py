from fastapi import APIRouter, HTTPException
from maimai_py import PlayerIdentifier
from app.core.maimai_client import maimai_client, divingfish_provider, lxns_provider
router = APIRouter()

@router.get("/player")
async def get_player_plates(username: str = None, friend_code: str = None, plate_type: str = "舞将", provider: str = "divingfish"):
    """
    获取玩家牌子进度
    
    - username: 用户名（水鱼查分器）
    - friend_code: 好友码（落雪查分器）
    - plate_type: 牌子类型，如"舞将"、"舞霸"等
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
        
        # 获取牌子进度
        plates = await maimai_client.plates(identifier, plate_type, provider=selected_provider)
        
        # 获取完成数量和总数量
        cleared_count = await plates.count_cleared()
        total_count = await plates.count_all()
        
        # 获取所有牌子
        all_plates = await plates.get_all()
        
        # 简单序列化牌子
        simple_plates = []
        for plate in all_plates:
            simple_plates.append({
                "title": getattr(plate, "title", None),
                "cleared": getattr(plate, "cleared", None)
            })
        
        return {
            "plate_type": plate_type,
            "cleared_count": cleared_count,
            "total_count": total_count,
            "completion_rate": f"{cleared_count/total_count:.2%}",
            "plates": simple_plates
        }
    except Exception as e:
        import traceback
        print(f"获取玩家牌子进度失败: {e}")
        print(traceback.format_exc())
        
        # 处理不同类型的错误
        if "KeyError" in str(type(e)) and "message" in str(e):
            raise HTTPException(status_code=400, detail="玩家不存在或数据源错误")
        else:
            raise HTTPException(status_code=500, detail=f"获取玩家牌子进度失败: {str(e)}")
