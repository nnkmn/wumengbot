#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的测试脚本，只初始化爬虫管理器，不实际运行爬虫
"""

import os
import sys
from loguru import logger

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wumeng_crawler.spiders.spider_manager import get_spider_manager
from wumeng_crawler.config.config import SPIDER_CONFIG

def main():
    """
    主函数
    """
    logger.info("启动测试脚本")
    
    try:
        # 初始化爬虫管理器
        logger.info("初始化爬虫管理器")
        spider_manager = get_spider_manager()
        
        # 获取爬虫状态
        logger.info("获取爬虫状态")
        status = spider_manager.get_spider_status()
        logger.info(f"爬虫状态: {status}")
        
        logger.info(f"共初始化 {len(spider_manager)} 个爬虫")
        
        # 打印爬虫信息
        for spider in spider_manager:
            logger.info(f"爬虫: {spider.name}，域名: {spider.domain}，IP: {spider.ip}")
            
    except Exception as e:
        logger.error(f"测试脚本运行异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        logger.info("关闭测试脚本")

if __name__ == "__main__":
    main()