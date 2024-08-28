from fastapi import FastAPI

from src.controllers.health_controller import router as health_router
from src.controllers.model_controller import router as model_router

app = FastAPI()


# Registrando o controller com as dependências configuradas
app.include_router(health_router)
app.include_router(model_router, prefix='/api/v1')
