from sqlalchemy.orm import Session
from loguru import logger
from datetime import datetime
from typing import List, Dict, Any

from app.models.crawled_data import CrawledData

class DBUtils:
    """
    数据库操作工具类，用于处理爬取数据的存储
    """
    
    @staticmethod
    def save_crawled_data(db: Session, crawled_data_list: List[Dict[str, Any]]):
        """
        保存爬取的数据到数据库
        
        Args:
            db: 数据库会话
            crawled_data_list: 爬取的数据列表，每个元素包含spider_name、data_type、data_id、data_content、source等字段
        
        Returns:
            saved_count: 保存成功的数据数量
        """
        logger.info(f"开始保存爬取数据，共 {len(crawled_data_list)} 条数据")
        
        saved_count = 0
        
        try:
            for data_item in crawled_data_list:
                # 验证数据完整性
                if not all(key in data_item for key in ["spider_name", "data_type", "data_content", "source"]):
                    logger.warning(f"爬取数据缺少必要字段，跳过保存: {data_item}")
                    continue
                
                # 创建CrawledData对象
                crawled_data = CrawledData(
                    spider_name=data_item["spider_name"],
                    data_type=data_item["data_type"],
                    data_id=data_item.get("data_id"),
                    data_content=data_item["data_content"],
                    crawl_time=datetime.utcnow(),
                    update_time=datetime.utcnow(),
                    is_valid=True,
                    source=data_item["source"]
                )
                
                # 添加到数据库
                db.add(crawled_data)
                saved_count += 1
            
            # 提交事务
            db.commit()
            
            logger.info(f"爬取数据保存完成，共保存 {saved_count} 条数据")
            
            return saved_count
        
        except Exception as e:
            logger.error(f"保存爬取数据失败: {e}")
            db.rollback()
            raise e
    
    @staticmethod
    def get_crawled_data(db: Session, **filters):
        """
        根据条件查询爬取的数据
        
        Args:
            db: 数据库会话
            **filters: 查询条件，如spider_name、data_type、data_id、is_valid等
        
        Returns:
            crawled_data_list: 查询到的数据列表
        """
        logger.info(f"查询爬取数据，条件: {filters}")
        
        try:
            # 构建查询
            query = db.query(CrawledData)
            
            # 添加过滤条件
            for key, value in filters.items():
                if hasattr(CrawledData, key):
                    query = query.filter(getattr(CrawledData, key) == value)
            
            # 执行查询
            crawled_data_list = query.all()
            
            logger.info(f"查询爬取数据完成，共 {len(crawled_data_list)} 条数据")
            
            return crawled_data_list
        
        except Exception as e:
            logger.error(f"查询爬取数据失败: {e}")
            raise e
    
    @staticmethod
    def update_crawled_data_validity(db: Session, data_id: str, is_valid: bool):
        """
        更新爬取数据的有效性
        
        Args:
            db: 数据库会话
            data_id: 数据ID
            is_valid: 数据是否有效
        
        Returns:
            updated_count: 更新成功的数据数量
        """
        logger.info(f"更新爬取数据有效性，data_id: {data_id}, is_valid: {is_valid}")
        
        try:
            # 执行更新
            result = db.query(CrawledData).filter(
                CrawledData.data_id == data_id
            ).update({
                "is_valid": is_valid,
                "update_time": datetime.utcnow()
            })
            
            # 提交事务
            db.commit()
            
            logger.info(f"更新爬取数据有效性完成，共更新 {result} 条数据")
            
            return result
        
        except Exception as e:
            logger.error(f"更新爬取数据有效性失败: {e}")
            db.rollback()
            raise e
    
    @staticmethod
    def delete_old_crawled_data(db: Session, days: int):
        """
        删除指定天数前的爬取数据
        
        Args:
            db: 数据库会话
            days: 天数，删除days天前的数据
        
        Returns:
            deleted_count: 删除成功的数据数量
        """
        logger.info(f"删除 {days} 天前的爬取数据")
        
        try:
            # 计算删除时间点
            from datetime import timedelta
            delete_time = datetime.utcnow() - timedelta(days=days)
            
            # 执行删除
            result = db.query(CrawledData).filter(
                CrawledData.crawl_time < delete_time
            ).delete()
            
            # 提交事务
            db.commit()
            
            logger.info(f"删除爬取数据完成，共删除 {result} 条数据")
            
            return result
        
        except Exception as e:
            logger.error(f"删除爬取数据失败: {e}")
            db.rollback()
            raise e