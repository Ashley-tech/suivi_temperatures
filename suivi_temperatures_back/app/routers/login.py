from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Compte


router = APIRouter(
    prefix="/login",
    tags=["Login"]
)


class LoginRequest(BaseModel):
    email: str
    mdp: str


@router.post("")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    compte = (
        db.query(Compte)
        .filter(
            Compte.email_compte == login_data.email,
            (
                (Compte.mdp_crypted == login_data.mdp)
                | (Compte.mdp == login_data.mdp)
            )
        )
        .first()
    )

    if compte is None:
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect"
        )

    return compte