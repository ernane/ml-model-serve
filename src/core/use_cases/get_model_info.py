from src.core.interfaces.cache_service import CacheService
from src.core.interfaces.model_repository import ModelRepository


class GetModelInfo:
    """
    Caso de uso para obter informações de um modelo a partir de um repositório
    de modelos e de um serviço de cache.

    Attributes:
        model_repository (ModelRepository): O repositório onde os modelos são
        armazenados e recuperados.
        cache_service (CacheService): O serviço de cache usado para armazenar
        e recuperar modelos em cache.

    Methods:
        execute(model_name: str) -> Optional[Model]: Recupera um modelo pelo
        nome, buscando primeiro no cache e depois no repositório.
    """

    def __init__(
        self, model_repository: ModelRepository, cache_service: CacheService
    ):
        """
        Inicializa o caso de uso com um repositório de modelos
        e um serviço de cache.

        Args:
            model_repository (ModelRepository): O repositório onde os modelos
            são armazenados e recuperados.
            cache_service (CacheService): O serviço de cache usado para
            armazenar e recuperar modelos em cache.
        """
        self.model_repository = model_repository
        self.cache_service = cache_service

    def execute(self, model_name: str):
        """
        Recupera um modelo pelo nome.

        Primeiro tenta buscar o modelo no cache. Se o modelo não for
        encontrado no cache, tenta buscar no repositório de modelos.
        Se o modelo for encontrado no repositório, ele é armazenado no cache
        para futuras requisições. O modelo fica armazenado em cache por 1 hora.

        Args:
            model_name (str): Nome do modelo a ser recuperado.

        Returns:
            Optional[Model]: O modelo recuperado, ou None se o modelo não
            for encontrado em nenhum dos locais.
        """
        model = self.cache_service.get(model_name)
        if model:
            return model

        model = self.model_repository.get_model(model_name)
        if model:
            self.cache_service.set(model_name, model, ttl=3600)
        return model
