import pickle
from typing import Optional

import redis

from src.core.entities.model import Model
from src.core.interfaces.cache_service import CacheService


class RedisCacheService(CacheService):
    def __init__(self, host: str = '127.0.0.1', port: int = 6379, db: int = 0):
        self.client = redis.Redis(host=host, port=port, db=db)

    def get(self, key: str) -> Optional[Model]:
        data = self.client.get(key)
        if data:
            return pickle.loads(data)
        return None

    def set(self, key: str, value: Model, ttl: int = 3600) -> None:
        self.client.setex(key, ttl, pickle.dumps(value))
