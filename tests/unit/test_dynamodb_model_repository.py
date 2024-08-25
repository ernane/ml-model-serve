from src.core.entities.model import Model

input_schema = (
    '{"type": "object", "properties": {"input": {"type": "string"}}}'
)

output_schema = (
    '{"type": "object", "properties": {"output": {"type": "string"}}}'
)


def test_get_model_success(dynamodb_repository, dynamodb_table):
    # Insere um item de teste na tabela DynamoDB simulada
    dynamodb_table.put_item(
        Item={
            'name': 'test-model',
            'input_schema': input_schema,
            'output_schema': output_schema,
            'status': 'active',
            'type': 'online',
        }
    )

    # Executa o método que deve recuperar o modelo
    result = dynamodb_repository.get_model('test-model')

    # Verifica se o item foi recuperado corretamente
    assert result.name == 'test-model'
    assert result.status == 'active'


def test_get_model_not_found(dynamodb_repository, dynamodb_table):
    # Tenta recuperar um item que não existe
    result = dynamodb_repository.get_model('unknown-model')

    # O resultado deve ser None já que o item não existe
    assert result is None


def test_save_model(dynamodb_repository, dynamodb_table):
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

    # Salva o modelo na tabela
    dynamodb_repository.save_model(model)

    # Verifica se o item foi salvo corretamente
    saved_item = dynamodb_table.get_item(Key={'name': 'test-model'}).get(
        'Item'
    )
    assert saved_item is not None
    assert saved_item['name'] == 'test-model'
    assert saved_item['status'] == 'active'
