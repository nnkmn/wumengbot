from fastapi import APIRouter, HTTPException
from loguru import logger
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# 导入爬虫管理器和数据处理器
from wumeng_crawler.spiders.spider_manager import get_spider_manager
from wumeng_crawler.processors.data_processor import get_data_processor

router = APIRouter()

@router.get("/")
def get_all_spiders():
    """
    获取所有爬虫的状态
    
    Returns:
        所有爬虫的状态信息
    """
    logger.info("获取所有爬虫状态")
    
    try:
        # 初始化爬虫管理器
        spider_manager = get_spider_manager()
        
        # 获取所有爬虫的状态
        spiders_status = spider_manager.get_spider_status()
        
        return {
            "status": "success",
            "count": len(spiders_status),
            "spiders": spiders_status
        }
    
    except Exception as e:
        logger.error(f"获取爬虫状态失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取爬虫状态失败: {str(e)}")

@router.post("/{spider_name}/run")
def run_spider_task(spider_name: str):
    """
    运行指定名称的爬虫
    
    Args:
        spider_name: 爬虫名称
    
    Returns:
        任务执行结果
    """
    logger.info(f"运行爬虫任务: {spider_name}")
    
    try:
        # 初始化爬虫管理器
        spider_manager = get_spider_manager()
        
        # 初始化数据处理器
        data_processor = get_data_processor()
        
        # 直接运行爬虫，不使用Celery
        spider_result = spider_manager.run_spider(spider_name)
        
        if spider_result:
            # 处理数据，同时保存到数据库
            _ = data_processor.process(
                spider_result, 
                format_type="json", 
                save=True, 
                save_to_db=True
            )
            
            return {
                "status": "success",
                "message": f"爬虫 {spider_name} 运行成功，数据已保存到文件和数据库",
                "result": "success"
            }
        else:
            return {
                "status": "warning",
                "message": f"爬虫 {spider_name} 运行失败或未爬取到任何数据",
                "result": "warning"
            }
    
    except Exception as e:
        logger.error(f"启动爬虫任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"启动爬虫任务失败: {str(e)}")

@router.post("/run-all")
def run_all_spiders_task():
    """
    运行所有爬虫
    
    Returns:
        任务执行结果
    """
    logger.info("运行所有爬虫任务")
    
    try:
        # 初始化爬虫管理器
        spider_manager = get_spider_manager()
        
        # 初始化数据处理器
        data_processor = get_data_processor()
        
        # 直接运行所有爬虫，不使用Celery
        all_data = spider_manager.run_all_spiders()
        
        if all_data:
            # 处理数据，同时保存到数据库
            _ = data_processor.process(
                all_data, 
                format_type="json", 
                save=True, 
                save_to_db=True
            )
            
            return {
                "status": "success",
                "message": "所有爬虫运行成功，数据已保存到文件和数据库",
                "result": "success"
            }
        else:
            return {
                "status": "warning",
                "message": "所有爬虫运行失败或未爬取到任何数据",
                "result": "warning"
            }
    
    except Exception as e:
        logger.error(f"启动所有爬虫任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"启动所有爬虫任务失败: {str(e)}")

@router.post("/{spider_name}/stop")
def stop_spider_task(spider_name: str):
    """
    停止指定名称的爬虫
    
    Args:
        spider_name: 爬虫名称
    
    Returns:
        任务执行结果
    """
    logger.info(f"停止爬虫任务: {spider_name}")
    
    try:
        # 初始化爬虫管理器
        spider_manager = get_spider_manager()
        
        # 关闭所有爬虫（目前spider_manager只支持关闭所有爬虫）
        spider_manager.close_all_spiders()
        
        return {
            "status": "success",
            "message": f"爬虫 {spider_name} 已停止",
            "result": "success"
        }
    
    except Exception as e:
        logger.error(f"启动停止爬虫任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"启动停止爬虫任务失败: {str(e)}")

@router.post("/stop-all")
def stop_all_spiders_task():
    """
    停止所有爬虫
    
    Returns:
        任务执行结果
    """
    logger.info("停止所有爬虫任务")
    
    try:
        # 初始化爬虫管理器
        spider_manager = get_spider_manager()
        
        # 关闭所有爬虫
        spider_manager.close_all_spiders()
        
        return {
            "status": "success",
            "message": "所有爬虫已停止",
            "result": "success"
        }
    
    except Exception as e:
        logger.error(f"启动停止所有爬虫任务失败: {e}")
        raise HTTPException(status_code=500, detail=f"启动停止所有爬虫任务失败: {str(e)}")
