from celery import Celery
from app.core.config import settings
import os

# 创建Celery应用实例
celery_app = Celery(
    "wumengbot",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks"]
)

# 配置Celery应用
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
    beat_schedule={},
    task_ignore_result=True,
    task_store_errors_even_if_ignored=True,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=3
)

# 自动发现任务
celery_app.autodiscover_tasks()

if __name__ == "__main__":
    celery_app.start()