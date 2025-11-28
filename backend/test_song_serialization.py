from maimai_py import MaimaiClient
import os
from dotenv import load_dotenv
import json

# 加载环境变量
load_dotenv()

async def test_song_serialization():
    """测试Song对象的序列化"""
    # 创建客户端
    client = MaimaiClient()
    
    # 获取歌曲列表
    songs = await client.songs()
    all_songs = await songs.get_all()
    
    # 查看第一个歌曲对象的属性和方法
    if all_songs:
        first_song = all_songs[0]
        print(f"Song对象类型: {type(first_song)}")
        print(f"Song对象属性: {dir(first_song)}")
        
        # 查看dataclass字段
        print(f"\nSong对象dataclass字段: {getattr(first_song, '__dataclass_fields__', '没有__dataclass_fields__属性')}")
        
        # 尝试手动构建字典
        print("\n手动构建字典:")
        try:
            # 获取所有dataclass字段
            fields = getattr(first_song, '__dataclass_fields__', {})
            song_dict = {}
            for field_name in fields:
                # 尝试获取字段值
                try:
                    value = getattr(first_song, field_name)
                    # 如果值是枚举类型，转换为字符串
                    if hasattr(value, '__class__') and hasattr(value.__class__, '__bases__') and 'Enum' in str(value.__class__.__bases__):
                        song_dict[field_name] = str(value)
                    # 如果值是列表，递归处理
                    elif isinstance(value, list):
                        song_dict[field_name] = [str(item) if hasattr(item, '__class__') and hasattr(item.__class__, '__bases__') and 'Enum' in str(item.__class__.__bases__) else item for item in value]
                    else:
                        song_dict[field_name] = value
                except Exception as e:
                    print(f"获取字段 {field_name} 失败: {e}")
            
            print("手动构建的字典:")
            print(json.dumps(song_dict, ensure_ascii=False, indent=2))
            
            return song_dict
        except Exception as e:
            print(f"手动构建字典失败: {e}")
    
    return None

# 运行测试
if __name__ == "__main__":
    import asyncio
    asyncio.run(test_song_serialization())