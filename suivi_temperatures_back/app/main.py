from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings

from app.routers import comptes
from app.routers import temperatures
from app.routers import login
from app.routers import email


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:8100",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8100",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.get("/")
def root():
    return {
        "message": "Bienvenue sur mon API FastAPI",
        "db": settings.POSTGRES_DB,
        "host": settings.POSTGRES_HOST,
        "port": settings.POSTGRES_PORT
    }

@app.post("/logout")
def logout():
    response = JSONResponse({"message": "Déconnexion réussie"})
    response.delete_cookie(
        key="access_token",
        samesite="lax",
        secure=False,
        path="/"
    )
    return response

app.include_router(comptes.router)
app.include_router(temperatures.router)
app.include_router(login.router)
app.include_router(email.router)