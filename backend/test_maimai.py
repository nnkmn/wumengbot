from maimai_py import MaimaiClient, DivingFishProvider
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_song_serialization():
    """测试Song对象的序列化"""
    # 创建客户端
    client = MaimaiClient()
    
    # 创建数据源
    divingfish_token = os.getenv("DIVINGFISH_TOKEN")
    divingfish_provider = DivingFishProvider(developer_token=divingfish_token)
    
    # 获取歌曲列表
    import asyncio
    
    async def main():
        songs = await client.songs()
        all_songs = await songs.get_all()
        
        # 查看第一个歌曲对象的属性和方法
        if all_songs:
            first_song = all_songs[0]
            print(f"Song对象类型: {type(first_song)}")
            print(f"Song对象属性: {dir(first_song)}")
            
            # 尝试不同的序列化方式
            print("\n尝试直接转换为字典:")
            try:
                song_dict = dict(first_song)
                print(song_dict)
            except Exception as e:
                print(f"直接转换失败: {e}")
            
            print("\n尝试获取属性:")
            try:
                song_info = {
                    "id": getattr(first_song, "id", None),
                    "title": getattr(first_song, "title", None),
                    "artist": getattr(first_song, "artist", None),
                    "genre": getattr(first_song, "genre", None),
                    "bpm": getattr(first_song, "bpm", None),
                    "level": getattr(first_song, "level", None),
                    "version": getattr(first_song, "version", None)
                }
                print(song_info)
            except Exception as e:
                print(f"获取属性失败: {e}")
    
    asyncio.run(main())

if __name__ == "__main__":
    test_song_serialization()