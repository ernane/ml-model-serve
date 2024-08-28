from fastapi import APIRouter, status
from pydantic import BaseModel


class Health(BaseModel):
    health: str


router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=Health)
async def root():
    return {'health': 'ok'}
