from abc import ABC, abstractmethod
from typing import Optional

from src.core.entities.model import Model


class CacheService(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Model]:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: Model, ttl: int) -> None:
        raise NotImplementedError
