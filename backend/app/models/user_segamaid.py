from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.core.database import Base
from datetime import datetime

class UserSegamaid(Base):
    __tablename__ = "user_segamaid"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(String(50), unique=True, index=True, nullable=False, comment="玩家ID")
    segamaid_id = Column(String(100), unique=True, index=True, nullable=False, comment="Segamaid ID")
    segamaid_token = Column(String(255), nullable=False, comment="Segamaid Token")
    status = Column(String(20), default="bound", nullable=False, comment="绑定状态: bound/unbound")
    bind_time = Column(DateTime, default=datetime.utcnow, nullable=False, comment="绑定时间")
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    is_active = Column(Boolean, default=True, nullable=False, comment="是否活跃")
    
    def __repr__(self):
        return f"<UserSegamaid(player_id='{self.player_id}', segamaid_id='{self.segamaid_id}', status='{self.status}')>"