from src.core.interfaces.cache_service import CacheService
from src.core.interfaces.model_repository import ModelRepository


class GetModelInfo:
    def __init__(
        self, model_repository: ModelRepository, cache_service: CacheService
    ):
        self.model_repository = model_repository
        self.cache_service = cache_service

    def execute(self, model_name: str):
        # Primeiro tenta buscar no cache
        model = self.cache_service.get(model_name)
        if model:
            return model

        # Se não encontrar no cache, busca no DynamoDB
        model = self.model_repository.get_model(model_name)
        if model:
            # Salva no cache para futuras requisições
            self.cache_service.set(
                model_name, model, ttl=3600
            )  # Cache por 1 hora
        return model
