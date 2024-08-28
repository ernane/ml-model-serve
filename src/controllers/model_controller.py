from fastapi import APIRouter, HTTPException

from src.core.use_cases.get_model_info import GetModelInfo
from src.infrastructure.cache.redis_cache_service import RedisCacheService
from src.infrastructure.db.dynamodb_model_repository import (
    DynamoDBModelRepository,
)

router = APIRouter()

# Configurações e injeção de dependências
dynamo_repo = DynamoDBModelRepository(table_name='models_table')
redis_cache = RedisCacheService(host='172.17.0.3', port=6379)
get_model_info_use_case = GetModelInfo(
    model_repository=dynamo_repo, cache_service=redis_cache
)


@router.get('/models/{model_name}')
async def get_model(model_name: str):
    model = get_model_info_use_case.execute(model_name)
    if model:
        return model
    raise HTTPException(status_code=404, detail='Model not found')
