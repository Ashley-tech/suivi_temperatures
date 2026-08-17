from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models import Compte
from app.security import hash_password

router = APIRouter(
    prefix="/comptes",
    tags=["Comptes"]
)

@router.get("")
def get_comptes(db: Session = Depends(get_db)):
    comptes = db.query(Compte).all()
    return comptes

@router.get("/{id}")
def get_compte(id: int, db: Session = Depends(get_db)):
    compte = db.query(Compte).filter(Compte.id == id).first()
    if compte is None:
        raise HTTPException(
            status_code=404,
            detail="Compte introuvable"
        )
    return compte


class CompteCreate(BaseModel):
    nom_compte: str
    prenom_compte: str
    email_compte: str
    mdp: str
    tel: str | None = None
    adresse: str | None = None
    adresse_comp: str | None = None
    cp: str | None = None
    ville: str | None = None
    pays: str | None = None
    fonction: str | None = None


@router.post("")
def create_compte(
    compte_data: CompteCreate,
    db: Session = Depends(get_db)
):
    compte_existant = (
        db.query(Compte)
        .filter(Compte.email_compte == compte_data.email_compte)
        .first()
    )

    if compte_existant:
        raise HTTPException(
            status_code=409,
            detail="Cette adresse email est déjà utilisée"
        )

    nouveau_compte = Compte(
        nom_compte=compte_data.nom_compte,
        prenom_compte=compte_data.prenom_compte,
        email_compte=compte_data.email_compte,

        # Mot de passe en clair
        mdp=compte_data.mdp,

        # Mot de passe hashé
        mdp_crypted=hash_password(compte_data.mdp),

        tel=compte_data.tel,
        adresse=compte_data.adresse,
        adresse_comp=compte_data.adresse_comp,
        cp=compte_data.cp,
        ville=compte_data.ville,
        pays=compte_data.pays,
        fonction=compte_data.fonction
    )

    db.add(nouveau_compte)
    db.commit()
    db.refresh(nouveau_compte)

    return nouveau_compte