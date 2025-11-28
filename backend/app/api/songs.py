from fastapi import APIRouter, HTTPException
import logging
from app.core.maimai_client import maimai_client

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 自定义序列化函数
def serialize_song(song):
    """
    自定义序列化Song对象，处理复杂类型
    """
    song_dict = {
        "id": song.id,
        "title": song.title,
        "artist": song.artist,
        "genre": str(song.genre),
        "bpm": song.bpm,
        "map": song.map,
        "version": song.version,
        "rights": song.rights,
        "aliases": song.aliases,
        "disabled": song.disabled
    }
    
    # 处理difficulties字段
    if hasattr(song, "difficulties") and song.difficulties:
        difficulties = song.difficulties
        song_dict["difficulties"] = {
            "basic": getattr(difficulties, "basic", None),
            "advanced": getattr(difficulties, "advanced", None),
            "expert": getattr(difficulties, "expert", None),
            "master": getattr(difficulties, "master", None),
            "remaster": getattr(difficulties, "remaster", None)
        }
    
    return song_dict

router = APIRouter()

@router.get("/")
async def get_all_songs():
    """
    获取所有歌曲信息
    """
    try:
        logger.info("开始获取所有歌曲信息")
        songs = await maimai_client.songs()
        logger.info("成功获取歌曲对象")
        all_songs = await songs.get_all()
        logger.info(f"成功获取 {len(all_songs)} 首歌曲")
        
        # 直接返回简单的歌曲列表，不使用复杂的序列化
        simple_songs = []
        for song in all_songs:
            simple_songs.append({
                "id": song.id,
                "title": song.title,
                "artist": song.artist
            })
        
        return simple_songs
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        logger.error(f"获取歌曲信息失败: {e}\n{error_detail}")
        raise HTTPException(status_code=500, detail=f"获取歌曲信息失败: {str(e)}")

@router.get("/id/{song_id}")
async def get_song_by_id(song_id: int):
    """
    根据ID获取歌曲信息
    """
    try:
        songs = await maimai_client.songs()
        song = await songs.by_id(song_id)
        if not song:
            raise HTTPException(status_code=404, detail="歌曲不存在")
        
        # 返回简单的歌曲信息
        return {
            "id": song.id,
            "title": song.title,
            "artist": song.artist
        }
    except Exception as e:
        import traceback
        logger.error(f"根据ID获取歌曲信息失败: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"根据ID获取歌曲信息失败: {str(e)}")

@router.get("/search")
async def search_songs(title: str = None, artist: str = None):
    """
    搜索歌曲
    
    - title: 歌曲标题
    - artist: 艺术家
    """
    try:
        songs = await maimai_client.songs()
        all_songs = await songs.get_all()
        
        # 过滤歌曲
        filtered_songs = []
        for song in all_songs:
            match = True
            if title and title.lower() not in song.title.lower():
                match = False
            if artist and artist.lower() not in song.artist.lower():
                match = False
            if match:
                # 使用简单的序列化
                filtered_songs.append({
                    "id": song.id,
                    "title": song.title,
                    "artist": song.artist
                })
        
        return filtered_songs
    except Exception as e:
        import traceback
        logger.error(f"搜索歌曲失败: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"搜索歌曲失败: {str(e)}")
