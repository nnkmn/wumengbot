from maimai_py import MaimaiClient, DivingFishProvider, LXNSProvider
from app.core.config import settings

# 全局创建MaimaiClient实例（单例模式）
maimai_client = MaimaiClient()

# 初始化数据源
divingfish_provider = DivingFishProvider(developer_token=settings.divingfish_token)
lxns_provider = LXNSProvider(developer_token=settings.lxns_token)
