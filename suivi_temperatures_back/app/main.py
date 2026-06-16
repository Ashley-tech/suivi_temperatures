from fastapi import FastAPI
from app.config import settings

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Bienvenue sur mon API FastAPI",
        "db": settings.POSTGRES_DB,
        "host": settings.POSTGRES_HOST,
        "port": settings.POSTGRES_PORT
    }