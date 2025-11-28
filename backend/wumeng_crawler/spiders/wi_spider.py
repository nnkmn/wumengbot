from wumeng_crawler.spiders.base_spider import BaseSpider
from loguru import logger
from typing import Dict, List, Optional, Any

class WISpider(BaseSpider):
    name = "wi_spider"
    allowed_domains = ["wi.sys-all.cn"]
    start_urls = ["https://wi.sys-all.cn/"]
    
    爬取wi.sys-all.cn域名的数据
    """
    
    def __init__(self, site_config: Dict[str, Any]):
        """
        初始化WI爬虫
        
        Args:
            site_config: 网站配置，包含ip、domain、name等信息
        """
        super().__init__(site_config)
        logger.info(f"初始化WI爬虫: {self.name}")
    
    def crawl(self) -> List[Dict[str, Any]]:
        """
        爬取wi.sys-all.cn的数据
        
        Returns:
            爬取到的数据列表
        """
        logger.info(f"开始爬取 {self.domain} 的数据")
        
        # 爬取数据的具体逻辑
        data = []
        
        try:
            # 示例：爬取首页数据
            url = self.get_url()
            response = self.get(url)
            
            if response:
                # 解析HTML
                soup = self.parse_html(response)
                
                # 示例：提取页面标题
                title = soup.title.string if soup.title else ""
                
                # 示例：提取所有链接
                links = []
                for a in soup.find_all("a", href=True):
                    links.append({
                        "text": a.get_text(strip=True),
                        "href": a["href"]
                    })
                
                # 构建数据
                data.append({
                    "site": self.name,
                    "domain": self.domain,
                    "title": title,
                    "links": links,
                    "crawl_time": self._get_current_time()
                })
                
                # 示例：爬取其他页面数据
                # 这里可以根据实际情况添加更多的爬取逻辑
                
        except Exception as e:
            logger.error(f"爬取 {self.domain} 数据失败: {e}")
        
        logger.info(f"爬取 {self.domain} 完成，共获取 {len(data)} 条数据")
        return data
    
    def process_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        处理爬取到的数据
        
        Args:
            data: 爬取到的数据列表
            
        Returns:
            处理后的数据列表
        """
        logger.info(f"开始处理 {self.domain} 的数据")
        
        processed_data = []
        
        for item in data:
            # 数据清洗和整合
            processed_item = {
                "site": item.get("site", self.name),
                "domain": item.get("domain", self.domain),
                "title": item.get("title", "").strip(),
                "links": [
                    {
                        "text": link.get("text", "").strip(),
                        "href": self._normalize_url(link.get("href", ""))
                    }
                    for link in item.get("links", [])
                    if link.get("href", "").strip()
                ],
                "crawl_time": item.get("crawl_time", self._get_current_time())
            }
            
            processed_data.append(processed_item)
        
        logger.info(f"处理 {self.domain} 数据完成，共处理 {len(processed_data)} 条数据")
        return processed_data
    
    def save_data(self, data: List[Dict[str, Any]]) -> bool:
        """
        保存处理后的数据
        
        Args:
            data: 处理后的数据列表
            
        Returns:
            保存结果，成功返回True，失败返回False
        """
        logger.info(f"开始保存 {self.domain} 的数据")
        
        try:
            # 示例：保存到文件
            import json
            import os
            from wumeng_crawler.config.config import BASE_DIR
            
            # 创建数据目录
            data_dir = os.path.join(BASE_DIR, "data", self.name)
            os.makedirs(data_dir, exist_ok=True)
            
            # 保存数据到JSON文件
            file_path = os.path.join(data_dir, f"{self._get_current_time().replace(':', '-')}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"保存 {self.domain} 数据成功，保存路径: {file_path}")
            return True
        except Exception as e:
            logger.error(f"保存 {self.domain} 数据失败: {e}")
            return False
    
    def _normalize_url(self, url: str) -> str:
        """
        标准化URL
        
        Args:
            url: 原始URL
            
        Returns:
            标准化后的URL
        """
        if not url:
            return ""
        
        # 处理相对URL
        if url.startswith("/"):
            return self.get_url(url)
        elif not url.startswith("http"):
            return self.get_url(url)
        
        return url
    
    def _get_current_time(self) -> str:
        """
        获取当前时间
        
        Returns:
            当前时间字符串，格式为YYYY-MM-DD HH:MM:SS
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")