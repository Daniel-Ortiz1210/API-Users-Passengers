from fastapi import FastAPI

from src.api.router import router
from src.database.connection import DatabaseConnection
from src.database.models.reservations import ReservationsModel
from src.database.models.passengers import PassengersModel
from src.utils.config import Config

settings = Config()

app: FastAPI = FastAPI(
    title=settings.app_name,
    description='',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc',
    openapi_url='/openapi.json',
)

@app.on_event('startup')
async def startup_event():
    database = DatabaseConnection().get_db()
    database.create_tables([PassengersModel, ReservationsModel], **{"safe": True})

app.include_router(router)
