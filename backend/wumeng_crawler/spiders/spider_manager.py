from wumeng_crawler.spiders.wq_spider import WQSpider
from wumeng_crawler.spiders.ai_spider import AISpider
from wumeng_crawler.spiders.wi_spider import WISpider
from wumeng_crawler.spiders.at_spider import ATSpider
from wumeng_crawler.config.config import SPIDER_CONFIG
from loguru import logger
from typing import Dict, List, Optional, Any
import concurrent.futures

class SpiderManager:
    """
    爬虫管理器，用于管理和调度所有爬虫
    """
    
    def __init__(self):
        """
        初始化爬虫管理器
        """
        self.spiders = []
        self._init_spiders()
        logger.info("初始化爬虫管理器完成")
    
    def _init_spiders(self):
        """
        初始化所有爬虫
        """
        logger.info("开始初始化所有爬虫")
        
        # 获取目标网站配置
        target_sites = SPIDER_CONFIG.get("TARGET_SITES", [])
        
        for site_config in target_sites:
            if site_config.get("enabled", True):
                # 根据网站名称创建对应的爬虫实例
                spider_name = site_config.get("name", "")
                
                if spider_name == "wq":
                    spider = WQSpider(site_config)
                elif spider_name == "ai":
                    spider = AISpider(site_config)
                elif spider_name == "wi":
                    spider = WISpider(site_config)
                elif spider_name == "at":
                    spider = ATSpider(site_config)
                else:
                    logger.warning(f"未知的爬虫名称: {spider_name}，跳过初始化")
                    continue
                
                self.spiders.append(spider)
                logger.info(f"初始化爬虫成功: {spider_name}")
            else:
                logger.info(f"爬虫 {site_config.get('name')} 已禁用，跳过初始化")
        
        logger.info(f"初始化爬虫完成，共初始化 {len(self.spiders)} 个爬虫")
    
    def run_all_spiders(self) -> List[Dict[str, Any]]:
        """
        运行所有爬虫
        
        Returns:
            所有爬虫爬取到的数据列表
        """
        logger.info("开始运行所有爬虫")
        
        all_data = []
        
        # 使用线程池并行运行爬虫
        with concurrent.futures.ThreadPoolExecutor(max_workers=SPIDER_CONFIG.get("CONCURRENT_REQUESTS", 4)) as executor:
            # 提交所有爬虫任务
            future_to_spider = {
                executor.submit(spider.run): spider
                for spider in self.spiders
            }
            
            # 获取任务结果
            for future in concurrent.futures.as_completed(future_to_spider):
                spider = future_to_spider[future]
                try:
                    result = future.result()
                    if result:
                        logger.info(f"爬虫 {spider.name} 运行成功")
                    else:
                        logger.warning(f"爬虫 {spider.name} 运行失败")
                except Exception as e:
                    logger.error(f"爬虫 {spider.name} 运行异常: {e}")
        
        logger.info("所有爬虫运行完成")
        return all_data
    
    def run_spider(self, spider_name: str) -> bool:
        """
        运行指定名称的爬虫
        
        Args:
            spider_name: 爬虫名称
            
        Returns:
            运行结果，成功返回True，失败返回False
        """
        logger.info(f"开始运行爬虫: {spider_name}")
        
        # 查找指定名称的爬虫
        for spider in self.spiders:
            if spider.name == spider_name:
                try:
                    result = spider.run()
                    if result:
                        logger.info(f"爬虫 {spider_name} 运行成功")
                    else:
                        logger.warning(f"爬虫 {spider_name} 运行失败")
                    return result
                except Exception as e:
                    logger.error(f"爬虫 {spider_name} 运行异常: {e}")
                    return False
        
        logger.error(f"未找到名称为 {spider_name} 的爬虫")
        return False
    
    def get_spider_status(self) -> List[Dict[str, Any]]:
        """
        获取所有爬虫的状态
        
        Returns:
            爬虫状态列表
        """
        logger.info("获取所有爬虫状态")
        
        status_list = []
        
        for spider in self.spiders:
            status = {
                "name": spider.name,
                "domain": spider.domain,
                "ip": spider.ip,
                "enabled": spider.enabled
            }
            status_list.append(status)
        
        logger.info(f"获取爬虫状态完成，共 {len(status_list)} 个爬虫")
        return status_list
    
    def close_all_spiders(self) -> None:
        """
        关闭所有爬虫
        """
        logger.info("开始关闭所有爬虫")
        
        for spider in self.spiders:
            try:
                spider.close()
            except Exception as e:
                logger.error(f"关闭爬虫 {spider.name} 失败: {e}")
        
        logger.info("关闭所有爬虫完成")
    
    def __enter__(self):
        """
        进入上下文管理器
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出上下文管理器，关闭所有爬虫
        """
        self.close_all_spiders()
    
    def __len__(self):
        """
        获取爬虫数量
        
        Returns:
            爬虫数量
        """
        return len(self.spiders)
    
    def __getitem__(self, index):
        """
        根据索引获取爬虫
        
        Args:
            index: 爬虫索引
            
        Returns:
            爬虫实例
        """
        return self.spiders[index]
    
    def __iter__(self):
        """
        迭代爬虫列表
        """
        return iter(self.spiders)

# 单例模式
_spider_manager_instance = None

def get_spider_manager() -> SpiderManager:
    """
    获取爬虫管理器实例
    
    Returns:
        爬虫管理器实例
    """
    global _spider_manager_instance
    if _spider_manager_instance is None:
        _spider_manager_instance = SpiderManager()
    return _spider_manager_instance