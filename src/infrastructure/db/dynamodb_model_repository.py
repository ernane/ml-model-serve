from typing import Optional

import boto3

from src.core.entities.model import Model
from src.core.interfaces.model_repository import ModelRepository


class DynamoDBModelRepository(ModelRepository):
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_model(self, name: str) -> Optional[Model]:
        response = self.table.get_item(Key={'name': name})
        item = response.get('Item')
        if item:
            return Model(
                name=item['name'],
                input_schema=item['input_schema'],
                output_schema=item['output_schema'],
                status=item['status'],
                type=item['type'],
            )
        return None

    def save_model(self, model: Model) -> None:
        self.table.put_item(
            Item={
                'name': model.name,
                'input_schema': model.input_schema,
                'output_schema': model.output_schema,
                'status': model.status,
                'type': model.type,
            }
        )
