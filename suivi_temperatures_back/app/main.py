from fastapi import FastAPI

from app.config import settings

from app.routers import comptes
from app.routers import temperatures
from app.routers import login


app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Bienvenue sur mon API FastAPI",
        "db": settings.POSTGRES_DB,
        "host": settings.POSTGRES_HOST,
        "port": settings.POSTGRES_PORT
    }


app.include_router(comptes.router)
app.include_router(temperatures.router)
app.include_router(login.router)