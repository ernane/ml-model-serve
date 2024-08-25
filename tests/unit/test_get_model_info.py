from unittest.mock import Mock

from src.core.use_cases.get_model_info import GetModelInfo


def test_get_model_info_found_in_cache(sample_model):
    # Mock the repository and cache service
    model_repository = Mock()
    cache_service = Mock()

    # Cache returns the model directly
    cache_service.get.return_value = sample_model

    # Create the use case with mocked dependencies
    use_case = GetModelInfo(model_repository, cache_service)

    # Execute the use case
    result = use_case.execute('fraud-detection')

    # Assertions
    cache_service.get.assert_called_once_with('fraud-detection')
    model_repository.get_model.assert_not_called()
    assert result == sample_model


def test_get_model_info_not_in_cache_but_in_repository(sample_model):
    # Mock the repository and cache service
    model_repository = Mock()
    cache_service = Mock()

    # Cache misses, repository returns the model
    cache_service.get.return_value = None
    model_repository.get_model.return_value = sample_model

    # Create the use case with mocked dependencies
    use_case = GetModelInfo(model_repository, cache_service)

    # Execute the use case
    result = use_case.execute('fraud-detection')

    # Assertions
    cache_service.get.assert_called_once_with('fraud-detection')
    model_repository.get_model.assert_called_once_with('fraud-detection')
    cache_service.set.assert_called_once_with(
        'fraud-detection', sample_model, ttl=3600
    )
    assert result == sample_model


def test_get_model_info_not_found(sample_model):
    # Mock the repository and cache service
    model_repository = Mock()
    cache_service = Mock()

    # Cache misses, repository also misses
    cache_service.get.return_value = None
    model_repository.get_model.return_value = None

    # Create the use case with mocked dependencies
    use_case = GetModelInfo(model_repository, cache_service)

    # Execute the use case
    result = use_case.execute('unknown-model')

    # Assertions
    cache_service.get.assert_called_once_with('unknown-model')
    model_repository.get_model.assert_called_once_with('unknown-model')
    cache_service.set.assert_not_called()
    assert result is None
