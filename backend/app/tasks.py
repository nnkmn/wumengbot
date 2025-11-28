from app.core.celery import celery_app
from loguru import logger
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入爬虫管理器
from wumeng_crawler.spiders.spider_manager import get_spider_manager
from wumeng_crawler.processors.data_processor import get_data_processor

@celery_app.task(name="app.tasks.run_spider")
def run_spider(spider_name: str):
    """
    运行指定名称的爬虫任务
    
    Args:
        spider_name: 爬虫名称
    
    Returns:
        任务执行结果
    """
    logger.info(f"开始执行爬虫任务: {spider_name}")
    
    try:
        # 初始化爬虫管理器
        spider_manager = get_spider_manager()
        
        # 初始化数据处理器
        data_processor = get_data_processor()
        
        # 运行指定名称的爬虫
        logger.info(f"开始运行爬虫: {spider_name}")
        spider_result = spider_manager.run_spider(spider_name)
        
        if spider_result:
            logger.info(f"爬虫 {spider_name} 运行成功")
            
            # 处理数据，同时保存到数据库
            logger.info(f"开始处理爬虫 {spider_name} 爬取到的数据")
            
            # 使用完整的处理流程，包括保存到数据库
            formatted_data = data_processor.process(
                spider_result, 
                format_type="json", 
                save=True, 
                save_to_db=True
            )
            
            logger.info(f"爬虫 {spider_name} 数据处理完成，已保存到文件和数据库")
            
            return {
                "status": "success",
                "spider_name": spider_name,
                "message": f"爬虫 {spider_name} 运行成功，数据已保存到文件和数据库"
            }
        else:
            logger.warning(f"爬虫 {spider_name} 运行失败或未爬取到任何数据")
            return {
                "status": "warning",
                "spider_name": spider_name,
                "message": f"爬虫 {spider_name} 运行失败或未爬取到任何数据"
            }
    
    except Exception as e:
        logger.error(f"爬虫 {spider_name} 运行异常: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "spider_name": spider_name,
            "message": f"爬虫 {spider_name} 运行异常: {str(e)}"
        }

@celery_app.task(name="app.tasks.run_all_spiders")
def run_all_spiders():
    """
    运行所有爬虫任务
    
    Returns:
        任务执行结果
    """
    logger.info("开始执行所有爬虫任务")
    
    try:
        # 初始化爬虫管理器
        spider_manager = get_spider_manager()
        
        # 初始化数据处理器
        data_processor = get_data_processor()
        
        # 运行所有爬虫
        logger.info("开始运行所有爬虫")
        all_data = spider_manager.run_all_spiders()
        
        if all_data:
            logger.info("所有爬虫运行成功")
            
            # 处理数据，同时保存到数据库
            logger.info("开始处理爬取到的数据")
            
            # 使用完整的处理流程，包括保存到数据库
            formatted_data = data_processor.process(
                all_data, 
                format_type="json", 
                save=True, 
                save_to_db=True
            )
            
            logger.info("所有爬虫数据处理完成，已保存到文件和数据库")
            
            return {
                "status": "success",
                "message": "所有爬虫运行成功，数据已保存到文件和数据库"
            }
        else:
            logger.warning("所有爬虫运行失败或未爬取到任何数据")
            return {
                "status": "warning",
                "message": "所有爬虫运行失败或未爬取到任何数据"
            }
    
    except Exception as e:
        logger.error(f"运行所有爬虫异常: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"运行所有爬虫异常: {str(e)}"
        }

@celery_app.task(name="app.tasks.stop_spider")
def stop_spider(spider_name: str):
    """
    停止指定名称的爬虫任务
    
    Args:
        spider_name: 爬虫名称
    
    Returns:
        任务执行结果
    """
    logger.info(f"开始执行停止爬虫任务: {spider_name}")
    
    try:
        # 初始化爬虫管理器
        spider_manager = get_spider_manager()
        
        # 关闭所有爬虫（目前spider_manager只支持关闭所有爬虫）
        spider_manager.close_all_spiders()
        
        logger.info(f"爬虫 {spider_name} 已停止")
        return {
            "status": "success",
            "spider_name": spider_name,
            "message": f"爬虫 {spider_name} 已停止"
        }
    
    except Exception as e:
        logger.error(f"停止爬虫 {spider_name} 异常: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "spider_name": spider_name,
            "message": f"停止爬虫 {spider_name} 异常: {str(e)}"
        }

@celery_app.task(name="app.tasks.stop_all_spiders")
def stop_all_spiders():
    """
    停止所有爬虫任务
    
    Returns:
        任务执行结果
    """
    logger.info("开始执行停止所有爬虫任务")
    
    try:
        # 初始化爬虫管理器
        spider_manager = get_spider_manager()
        
        # 关闭所有爬虫
        spider_manager.close_all_spiders()
        
        logger.info("所有爬虫已停止")
        return {
            "status": "success",
            "message": "所有爬虫已停止"
        }
    
    except Exception as e:
        logger.error(f"停止所有爬虫异常: {e}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "message": f"停止所有爬虫异常: {str(e)}"
        }