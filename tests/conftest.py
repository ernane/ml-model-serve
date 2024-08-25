import os

import boto3
import pytest
from moto import mock_aws

from src.core.entities.model import Model
from src.infrastructure.db.dynamodb_model_repository import (
    DynamoDBModelRepository,
)


@pytest.fixture
def sample_model():
    return Model(
        name='churn-model',
        input_schema={
            'type': 'object',
            'properties': {
                'input': {
                    'type': 'string',
                }
            },
        },
        output_schema={
            'type': 'object',
            'properties': {
                'output': {
                    'type': 'string',
                }
            },
        },
        status='active',
        type='online',
    )


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'


@pytest.fixture
def aws_client(aws_credentials):
    with mock_aws():
        yield boto3.resource('dynamodb', region_name='us-east-1')


@pytest.fixture
def dynamodb_table(aws_client):
    with mock_aws(config={'dynamodb': {'use_docker': False}}):
        dynamodb = aws_client
        table = dynamodb.create_table(
            TableName='models_table',
            KeySchema=[{'AttributeName': 'name', 'KeyType': 'HASH'}],
            AttributeDefinitions=[
                {'AttributeName': 'name', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            },
        )
        # Espera a tabela ser criada
        table.meta.client.get_waiter('table_exists').wait(
            TableName='models_table'
        )
        yield table


@pytest.fixture
def dynamodb_repository(dynamodb_table):
    return DynamoDBModelRepository(table_name='models_table')
