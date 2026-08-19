from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Compte
from app.security import create_access_token, verify_password


router = APIRouter(
    prefix="/login",
    tags=["Login"]
)


class LoginRequest(BaseModel):
    email: EmailStr
    mdp: str = Field(..., min_length=8)


@router.post("")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    compte = db.query(Compte).filter(Compte.email_compte == login_data.email).first()

    if compte is None:
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect"
        )

    password_valid = False
    if compte.mdp_crypted:
        password_valid = verify_password(login_data.mdp, compte.mdp_crypted)
    if not password_valid and compte.mdp:
        password_valid = verify_password(login_data.mdp, compte.mdp)

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect"
        )

    token = create_access_token(compte.email_compte)
    response = JSONResponse({
        "message": "Connexion réussie",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": compte.id,
            "email_compte": compte.email_compte,
            "nom_compte": compte.nom_compte,
            "prenom_compte": compte.prenom_compte,
        }
    })

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=3600,
        path="/"
    )

    return response
