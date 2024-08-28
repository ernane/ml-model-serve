from fastapi import status
from fastapi.testclient import TestClient

from src.fastapi_app import app


def test_root_ok_and_health():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'health': 'ok'}
