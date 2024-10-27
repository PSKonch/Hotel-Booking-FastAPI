from src.config import settings
from src.connectors.redis_conn import RedisManager

redis_manager = RedisManager(host=settings.REDIS_HOST, port=settings.REDIS_PORT)