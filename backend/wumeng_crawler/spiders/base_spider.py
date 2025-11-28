import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger
from typing import Dict, List, Optional, Any
import time
import random

from wumeng_crawler.config.config import SPIDER_CONFIG

class BaseSpider:
    """
    爬虫基类，包含通用的爬取逻辑和配置
    """
    
    def __init__(self, site_config: Dict[str, Any]):
        """
        初始化爬虫
        
        Args:
            site_config: 网站配置，包含ip、domain、name等信息
        """
        self.site_config = site_config
        self.ip = site_config.get("ip")
        self.domain = site_config.get("domain")
        self.name = site_config.get("name")
        self.enabled = site_config.get("enabled", True)
        
        # 初始化请求会话
        self.session = requests.Session()
        
        # 配置请求头
        self.user_agent = UserAgent()
        self.session.headers.update({
            "User-Agent": self.user_agent.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        })
        
        # 配置代理
        if SPIDER_CONFIG.get("PROXY_ENABLED"):
            proxy_url = SPIDER_CONFIG.get("PROXY_URL")
            self.session.proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
        
        # 配置超时
        self.timeout = SPIDER_CONFIG.get("REQUEST_TIMEOUT", 30)
        
        # 配置重试次数
        self.retry_times = SPIDER_CONFIG.get("RETRY_TIMES", 3)
        
        # 配置重试延迟
        self.retry_delay = SPIDER_CONFIG.get("RETRY_DELAY", 5)
        
        # 配置下载延迟
        self.download_delay = SPIDER_CONFIG.get("DOWNLOAD_DELAY", 1.0)
        
        # 配置随机下载延迟
        self.randomize_download_delay = SPIDER_CONFIG.get("RANDOMIZE_DOWNLOAD_DELAY", True)
        
        logger.info(f"初始化爬虫: {self.name}，目标域名: {self.domain}，IP地址: {self.ip}")
    
    def get_url(self, path: str = "") -> str:
        """
        构建完整的URL
        
        Args:
            path: 路径
            
        Returns:
            完整的URL
        """
        return f"http://{self.domain}/{path.lstrip('/')}"
    
    def get_url_by_ip(self, path: str = "") -> str:
        """
        使用IP地址构建完整的URL
        
        Args:
            path: 路径
            
        Returns:
            完整的URL
        """
        return f"http://{self.ip}/{path.lstrip('/')}"
    
    def add_headers(self, headers: Dict[str, str]) -> None:
        """
        添加请求头
        
        Args:
            headers: 请求头字典
        """
        self.session.headers.update(headers)
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        """
        发送GET请求
        
        Args:
            url: URL地址
            params: 请求参数
            headers: 请求头
            
        Returns:
            请求响应，失败返回None
        """
        for retry in range(self.retry_times):
            try:
                # 随机下载延迟
                if self.randomize_download_delay:
                    delay = random.uniform(0.5 * self.download_delay, 1.5 * self.download_delay)
                else:
                    delay = self.download_delay
                
                time.sleep(delay)
                
                logger.info(f"发送GET请求: {url}，重试次数: {retry + 1}")
                response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                
                logger.info(f"GET请求成功: {url}，状态码: {response.status_code}")
                return response
            except requests.exceptions.RequestException as e:
                logger.error(f"GET请求失败: {url}，错误: {e}，重试次数: {retry + 1}")
                
                if retry < self.retry_times - 1:
                    logger.info(f"等待 {self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"GET请求最终失败: {url}，已达到最大重试次数")
                    return None
    
    def post(self, url: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Optional[requests.Response]:
        """
        发送POST请求
        
        Args:
            url: URL地址
            data: 表单数据
            json: JSON数据
            headers: 请求头
            
        Returns:
            请求响应，失败返回None
        """
        for retry in range(self.retry_times):
            try:
                # 随机下载延迟
                if self.randomize_download_delay:
                    delay = random.uniform(0.5 * self.download_delay, 1.5 * self.download_delay)
                else:
                    delay = self.download_delay
                
                time.sleep(delay)
                
                logger.info(f"发送POST请求: {url}，重试次数: {retry + 1}")
                response = self.session.post(url, data=data, json=json, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                
                logger.info(f"POST请求成功: {url}，状态码: {response.status_code}")
                return response
            except requests.exceptions.RequestException as e:
                logger.error(f"POST请求失败: {url}，错误: {e}，重试次数: {retry + 1}")
                
                if retry < self.retry_times - 1:
                    logger.info(f"等待 {self.retry_delay} 秒后重试...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"POST请求最终失败: {url}，已达到最大重试次数")
                    return None
    
    def parse_html(self, response: requests.Response) -> BeautifulSoup:
        """
        解析HTML响应
        
        Args:
            response: 请求响应
            
        Returns:
            BeautifulSoup对象
        """
        return BeautifulSoup(response.text, "lxml")
    
    def parse_json(self, response: requests.Response) -> Optional[Dict[str, Any]]:
        """
        解析JSON响应
        
        Args:
            response: 请求响应
            
        Returns:
            JSON字典，失败返回None
        """
        try:
            return response.json()
        except ValueError as e:
            logger.error(f"解析JSON失败: {e}")
            return None
    
    def crawl(self) -> List[Dict[str, Any]]:
        """
        爬取数据的主方法，需要在子类中实现
        
        Returns:
            爬取到的数据列表
        """
        raise NotImplementedError("子类必须实现crawl方法")
    
    def close(self) -> None:
        """
        关闭爬虫会话
        """
        self.session.close()
        logger.info(f"关闭爬虫: {self.name}")
    
    def __enter__(self):
        """
        进入上下文管理器
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出上下文管理器，关闭爬虫会话
        """
        self.close()
    
    def save_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        保存数据的方法，需要在子类中实现
        
        Args:
            data: 爬取到的数据列表
            
        Returns:
            保存结果，成功返回True，失败返回False
        """
        raise NotImplementedError("子类必须实现save_data方法")
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        处理数据的方法，需要在子类中实现
        
        Args:
            data: 爬取到的数据列表
            
        Returns:
            处理后的数据列表
        """
        raise NotImplementedError("子类必须实现process_data方法")
    
    def run(self) -> bool:
        """
        运行爬虫的完整流程
        
        Returns:
            运行结果，成功返回True，失败返回False
        """
        if not self.enabled:
            logger.info(f"爬虫 {self.name} 已禁用，跳过运行")
            return False
        
        try:
            logger.info(f"开始运行爬虫: {self.name}")
            
            # 爬取数据
            raw_data = self.crawl()
            
            if not raw_data:
                logger.warning(f"爬虫 {self.name} 未爬取到数据")
                return False
            
            logger.info(f"爬虫 {self.name} 爬取到 {len(raw_data)} 条数据")
            
            # 处理数据
            processed_data = self.process_data(raw_data)
            
            if not processed_data:
                logger.warning(f"爬虫 {self.name} 处理数据后为空")
                return False
            
            logger.info(f"爬虫 {self.name} 处理后的数据数量: {len(processed_data)}")
            
            # 保存数据
            save_result = self.save_data(processed_data)
            
            if save_result:
                logger.info(f"爬虫 {self.name} 数据保存成功")
                return True
            else:
                logger.error(f"爬虫 {self.name} 数据保存失败")
                return False
        
        except Exception as e:
            logger.error(f"爬虫 {self.name} 运行失败: {e}")
            return False
        finally:
            self.close()
