#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
舞萌数据爬取系统主程序
"""

import os
import sys
from loguru import logger
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wumeng_crawler.spiders.spider_manager import get_spider_manager
from wumeng_crawler.processors.data_processor import get_data_processor
from wumeng_crawler.config.config import BASE_DIR

def main():
    """
    主程序入口
    """
    logger.info("启动舞萌数据爬取系统")
    
    # 创建日志目录
    logs_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # 初始化爬虫管理器
    spider_manager = get_spider_manager()
    
    # 初始化数据处理器
    data_processor = get_data_processor()
    
    try:
        # 运行所有爬虫
        logger.info("开始运行所有爬虫")
        all_data = spider_manager.run_all_spiders()
        
        # 处理数据
        if all_data:
            logger.info("开始处理爬取到的数据")
            
            # 清洗数据
            cleaned_data = data_processor.clean_data(all_data)
            
            # 整合数据
            integrated_data = data_processor.integrate_data(cleaned_data)
            
            # 格式化数据为JSON
            formatted_data = data_processor.format_data(integrated_data, format_type="json")
            
            # 保存数据
            file_path = data_processor.save_processed_data(formatted_data, format_type="json")
            logger.info(f"数据保存成功，保存路径: {file_path}")
        else:
            logger.warning("未爬取到任何数据")
            
    except KeyboardInterrupt:
        logger.info("用户中断程序")
    except Exception as e:
        logger.error(f"程序运行异常: {e}")
        import traceback
        traceback.print_exc()
    finally:
        logger.info("关闭舞萌数据爬取系统")

if __name__ == "__main__":
    main()