from fastapi import APIRouter, HTTPException, Query
from loguru import logger
import json
import os
import sys
from typing import List, Dict, Any, Optional

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

router = APIRouter()

# 爬虫数据存储路径
DATA_STORAGE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "wumeng_crawler",
    "data"
)

@router.get("/")
def search_data(
    keyword: Optional[str] = Query(None, description="查询关键词"),
    spider_name: Optional[str] = Query(None, description="爬虫名称"),
    data_type: Optional[str] = Query(None, description="数据类型"),
    limit: int = Query(10, description="返回结果数量"),
    offset: int = Query(0, description="偏移量")
):
    """
    搜索爬虫数据
    
    Args:
        keyword: 查询关键词
        spider_name: 爬虫名称
        data_type: 数据类型
        limit: 返回结果数量
        offset: 偏移量
    
    Returns:
        搜索结果
    """
    logger.info(f"搜索数据: keyword={keyword}, spider_name={spider_name}, data_type={data_type}, limit={limit}, offset={offset}")
    
    try:
        # 检查数据存储目录是否存在
        if not os.path.exists(DATA_STORAGE_PATH):
            return {
                "status": "success",
                "count": 0,
                "results": []
            }
        
        # 获取所有数据文件
        data_files = []
        for root, dirs, files in os.walk(DATA_STORAGE_PATH):
            for file in files:
                if file.endswith(".json"):
                    data_files.append(os.path.join(root, file))
        
        # 按修改时间排序，最新的文件优先
        data_files.sort(key=os.path.getmtime, reverse=True)
        
        # 搜索数据
        all_results = []
        for file_path in data_files:
            try:
                # 读取文件内容
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # 解析文件名，获取爬虫名称
                file_name = os.path.basename(file_path)
                
                # 处理数据
                if isinstance(data, dict):
                    # 单个爬虫的数据
                    all_results.append({
                        "file_path": file_path,
                        "file_name": file_name,
                        "data": data,
                        "timestamp": os.path.getmtime(file_path)
                    })
                elif isinstance(data, list):
                    # 多个爬虫的数据列表
                    for item in data:
                        all_results.append({
                            "file_path": file_path,
                            "file_name": file_name,
                            "data": item,
                            "timestamp": os.path.getmtime(file_path)
                        })
            except Exception as e:
                logger.error(f"读取文件 {file_path} 失败: {e}")
                continue
        
        # 过滤结果
        filtered_results = []
        for result in all_results:
            # 检查爬虫名称
            if spider_name:
                result_spider_name = result["data"].get("spider_name", "")
                if result_spider_name != spider_name:
                    continue
            
            # 检查数据类型
            if data_type:
                result_data_type = result["data"].get("type", "")
                if result_data_type != data_type:
                    continue
            
            # 检查关键词
            if keyword:
                # 将数据转换为字符串，检查是否包含关键词
                data_str = json.dumps(result["data"], ensure_ascii=False)
                if keyword not in data_str:
                    continue
            
            filtered_results.append(result)
        
        # 分页
        total = len(filtered_results)
        paginated_results = filtered_results[offset:offset+limit]
        
        return {
            "status": "success",
            "total": total,
            "count": len(paginated_results),
            "offset": offset,
            "limit": limit,
            "results": paginated_results
        }
    
    except Exception as e:
        logger.error(f"搜索数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"搜索数据失败: {str(e)}")

@router.get("/latest")
def get_latest_data(
    spider_name: Optional[str] = Query(None, description="爬虫名称"),
    limit: int = Query(5, description="返回结果数量")
):
    """
    获取最新的爬虫数据
    
    Args:
        spider_name: 爬虫名称
        limit: 返回结果数量
    
    Returns:
        最新数据列表
    """
    logger.info(f"获取最新数据: spider_name={spider_name}, limit={limit}")
    
    try:
        # 检查数据存储目录是否存在
        if not os.path.exists(DATA_STORAGE_PATH):
            return {
                "status": "success",
                "count": 0,
                "results": []
            }
        
        # 获取所有数据文件
        data_files = []
        for root, dirs, files in os.walk(DATA_STORAGE_PATH):
            for file in files:
                if file.endswith(".json"):
                    data_files.append(os.path.join(root, file))
        
        # 按修改时间排序，最新的文件优先
        data_files.sort(key=os.path.getmtime, reverse=True)
        
        # 获取最新数据
        latest_results = []
        for file_path in data_files:
            try:
                # 读取文件内容
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # 解析文件名，获取爬虫名称
                file_name = os.path.basename(file_path)
                
                # 处理数据
                if isinstance(data, dict):
                    # 单个爬虫的数据
                    if not spider_name or data.get("spider_name", "") == spider_name:
                        latest_results.append({
                            "file_path": file_path,
                            "file_name": file_name,
                            "data": data,
                            "timestamp": os.path.getmtime(file_path)
                        })
                elif isinstance(data, list):
                    # 多个爬虫的数据列表
                    for item in data:
                        if not spider_name or item.get("spider_name", "") == spider_name:
                            latest_results.append({
                                "file_path": file_path,
                                "file_name": file_name,
                                "data": item,
                                "timestamp": os.path.getmtime(file_path)
                            })
            except Exception as e:
                logger.error(f"读取文件 {file_path} 失败: {e}")
                continue
            
            # 检查是否达到限制
            if len(latest_results) >= limit:
                break
        
        return {
            "status": "success",
            "count": len(latest_results),
            "results": latest_results
        }
    
    except Exception as e:
        logger.error(f"获取最新数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取最新数据失败: {str(e)}")

@router.get("/stats")
def get_data_stats():
    """
    获取数据统计信息
    
    Returns:
        数据统计信息
    """
    logger.info("获取数据统计信息")
    
    try:
        # 检查数据存储目录是否存在
        if not os.path.exists(DATA_STORAGE_PATH):
            return {
                "status": "success",
                "total_files": 0,
                "total_records": 0,
                "spider_stats": {},
                "data_type_stats": {}
            }
        
        # 统计数据
        total_files = 0
        total_records = 0
        spider_stats = {}
        data_type_stats = {}
        
        # 获取所有数据文件
        data_files = []
        for root, dirs, files in os.walk(DATA_STORAGE_PATH):
            for file in files:
                if file.endswith(".json"):
                    data_files.append(os.path.join(root, file))
        
        total_files = len(data_files)
        
        # 统计每个文件的数据
        for file_path in data_files:
            try:
                # 读取文件内容
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # 处理数据
                if isinstance(data, dict):
                    # 单个爬虫的数据
                    total_records += 1
                    
                    # 统计爬虫
                    spider_name = data.get("spider_name", "unknown")
                    spider_stats[spider_name] = spider_stats.get(spider_name, 0) + 1
                    
                    # 统计数据类型
                    data_type = data.get("type", "unknown")
                    data_type_stats[data_type] = data_type_stats.get(data_type, 0) + 1
                elif isinstance(data, list):
                    # 多个爬虫的数据列表
                    total_records += len(data)
                    
                    for item in data:
                        # 统计爬虫
                        spider_name = item.get("spider_name", "unknown")
                        spider_stats[spider_name] = spider_stats.get(spider_name, 0) + 1
                        
                        # 统计数据类型
                        data_type = item.get("type", "unknown")
                        data_type_stats[data_type] = data_type_stats.get(data_type, 0) + 1
            except Exception as e:
                logger.error(f"读取文件 {file_path} 失败: {e}")
                continue
        
        return {
            "status": "success",
            "total_files": total_files,
            "total_records": total_records,
            "spider_stats": spider_stats,
            "data_type_stats": data_type_stats
        }
    
    except Exception as e:
        logger.error(f"获取数据统计信息失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取数据统计信息失败: {str(e)}")