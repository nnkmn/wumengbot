from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from app.core.database import Base
from datetime import datetime

class CrawledData(Base):
    __tablename__ = "crawled_data"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    spider_name = Column(String(50), index=True, nullable=False, comment="爬虫名称")
    data_type = Column(String(50), index=True, nullable=False, comment="数据类型: player/score/song/plate")
    data_id = Column(String(100), index=True, nullable=True, comment="数据ID，如玩家ID、歌曲ID等")
    data_content = Column(JSON, nullable=False, comment="数据内容，JSON格式")
    crawl_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment="爬取时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    is_valid = Column(Boolean, default=True, nullable=False, comment="数据是否有效")
    source = Column(String(100), nullable=False, comment="数据来源，如wq/ai/wi/at")
    
    def __repr__(self):
        return f"<CrawledData(spider_name='{self.spider_name}', data_type='{self.data_type}', data_id='{self.data_id}', crawl_time='{self.crawl_time}')>"