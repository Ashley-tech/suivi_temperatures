from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field, constr
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Compte, Temperature
from app.security import get_current_user, hash_password

router = APIRouter(
    prefix="/comptes",
    tags=["Comptes"]
)


@router.get("")
def get_comptes(
    db: Session = Depends(get_db),
    current_user: Compte = Depends(get_current_user)
):
    _ = current_user
    comptes = db.query(Compte).all()
    return comptes


@router.get("/{id}")
def get_compte(
    id: int,
    db: Session = Depends(get_db),
    current_user: Compte = Depends(get_current_user)
):
    _ = current_user
    compte = db.query(Compte).filter(Compte.id == id).first()
    if compte is None:
        raise HTTPException(
            status_code=404,
            detail="Compte introuvable"
        )
    return compte


class RequestFindEmail(BaseModel):
    email: EmailStr


@router.post("/find")
def get_compte(
    request_find: RequestFindEmail,
    db: Session = Depends(get_db)
):
    compte = db.query(Compte).filter(Compte.email_compte == request_find.email).first()
    if compte is None:
        raise HTTPException(
            status_code=404,
            detail="Compte introuvable"
        )
    return compte


class CompteCreate(BaseModel):
    nom_compte: constr(min_length=1, max_length=100)
    prenom_compte: constr(min_length=1, max_length=100)
    email_compte: EmailStr
    mdp: str = Field(..., min_length=8)
    tel: str | None = Field(default=None, max_length=20)
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

    hashed_password = hash_password(compte_data.mdp)
    nouveau_compte = Compte(
        nom_compte=compte_data.nom_compte,
        prenom_compte=compte_data.prenom_compte,
        email_compte=compte_data.email_compte,
        mdp=compte_data.mdp,
        mdp_crypted=hashed_password,
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


class CompteUpdate(BaseModel):
    nom_compte: constr(min_length=2, max_length=100) | None = None
    prenom_compte: constr(min_length=2, max_length=100) | None = None
    email_compte: EmailStr | None = None
    mdp: str | None = Field(default=None, min_length=8)
    tel: str | None = Field(default=None, min_length=8, max_length=20)
    adresse: str | None = None
    adresse_comp: str | None = None
    cp: str | None = None
    ville: str | None = None
    pays: str | None = None
    fonction: str | None = None
    id: int | None = None


@router.put("/{id}")
@router.patch("/{id}")
def update_compte(
    id: int,
    compte_data: CompteUpdate,
    db: Session = Depends(get_db),
    current_user: Compte = Depends(get_current_user)
):
    _ = current_user
    compte = db.query(Compte).filter(Compte.id == id).first()
    if compte is None:
        raise HTTPException(
            status_code=404,
            detail="Compte introuvable"
        )

    if compte_data.id is not None and compte_data.id != id:
        raise HTTPException(
            status_code=400,
            detail="L'ID du compte ne peut pas être modifié"
        )

    if compte_data.email_compte is not None and compte_data.email_compte != compte.email_compte:
        compte_existant = (
            db.query(Compte)
            .filter(Compte.email_compte == compte_data.email_compte, Compte.id != id)
            .first()
        )
        if compte_existant:
            raise HTTPException(
                status_code=409,
                detail="Cette adresse email est déjà utilisée"
            )

    if compte_data.nom_compte is not None:
        compte.nom_compte = compte_data.nom_compte
    if compte_data.prenom_compte is not None:
        compte.prenom_compte = compte_data.prenom_compte
    if compte_data.email_compte is not None:
        compte.email_compte = compte_data.email_compte
    if compte_data.mdp is not None:
        hashed_password_value = hash_password(compte_data.mdp)
        compte.mdp = hashed_password_value
        compte.mdp_crypted = hashed_password_value
    if compte_data.tel is not None:
        compte.tel = compte_data.tel
    if compte_data.adresse is not None:
        compte.adresse = compte_data.adresse
    if compte_data.adresse_comp is not None:
        compte.adresse_comp = compte_data.adresse_comp
    if compte_data.cp is not None:
        compte.cp = compte_data.cp
    if compte_data.ville is not None:
        compte.ville = compte_data.ville
    if compte_data.pays is not None:
        compte.pays = compte_data.pays
    if compte_data.fonction is not None:
        compte.fonction = compte_data.fonction

    db.commit()
    db.refresh(compte)

    return compte


@router.delete("/{id}")
def delete_compte(
    id: int,
    db: Session = Depends(get_db),
    current_user: Compte = Depends(get_current_user)
):
    _ = current_user
    compte = db.query(Compte).filter(Compte.id == id).first()
    if compte is None:
        raise HTTPException(
            status_code=404,
            detail="Compte introuvable"
        )

    db.query(Temperature).filter(Temperature.compte_id == id).delete()
    db.delete(compte)
    db.commit()

    return {"message": "Compte et toutes ses températures supprimés avec succès"}