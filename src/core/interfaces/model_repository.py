from abc import ABC, abstractmethod
from typing import Optional

from src.core.entities.model import Model


class ModelRepository(ABC):
    @abstractmethod
    def get_model(self, name: str) -> Optional[Model]:
        raise NotImplementedError

    @abstractmethod
    def save_model(self, model: Model) -> None:
        raise NotImplementedError
