import os
import pickle
from unittest.mock import MagicMock, patch

import pytest
from pytest_redis import factories

from src.core.entities.model import Model
from src.infrastructure.cache.redis_cache_service import RedisCacheService

redis_nooproc = factories.redis_noproc(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=6379,
    startup_timeout=5,
)

redis_external = factories.redisdb('redis_nooproc')


@pytest.fixture
def redis_cache_service(redis_external):
    redis_cache_service = RedisCacheService()
    redis_cache_service.client = redis_external
    return redis_cache_service


def test_get_model_from_cache(redis_cache_service, redis_external):
    # Criando um modelo de teste
    model = Model(
        name='test-model',
        input_schema={
            'type': 'object',
            'properties': {'input': {'type': 'string'}},
        },
        output_schema={
            'type': 'object',
            'properties': {'output': {'type': 'string'}},
        },
        status='active',
        type='online',
    )

    redis_external.setex('test-model', 3600, pickle.dumps(model))

    # Recuperando o modelo através do serviço de cache
    result = redis_cache_service.get('test-model')

    # Verificando se o modelo retornado é igual ao esperado
    assert result == model


def test_get_model_not_in_cache(redis_cache_service, redis_external):
    # Certifique-se de que a chave 'test-model' não exista no cache
    redis_external.delete('test-model')

    # Chama o método get, que deve retornar None
    result = redis_cache_service.get('test-model')

    # Verifica se o resultado é None, indicando que o modelo não está no cache
    assert result is None


@patch('redis.client.Redis.setex', new_callable=MagicMock)
def test_set_model_in_cache(mock_setex, redis_cache_service):
    model = Model(
        name='test-model',
        input_schema={
            'type': 'object',
            'properties': {'input': {'type': 'string'}},
        },
        output_schema={
            'type': 'object',
            'properties': {'output': {'type': 'string'}},
        },
        status='active',
        type='online',
    )

    redis_cache_service.set('test-model', model, ttl=3600)

    # Verifica se o método setex foi chamado corretamente
    mock_setex.assert_called_once_with('test-model', 3600, pickle.dumps(model))
