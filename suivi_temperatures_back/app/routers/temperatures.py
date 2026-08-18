from datetime import date, time
from enum import Enum

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Compte, Temperature
from app.security import get_current_user


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"]
)


class LocalisationEnum(str, Enum):
    NO = "NO"
    N = "N"
    NE = "NE"
    SO = "SO"
    S = "S"
    SE = "SE"


@router.get("")
def get_temperatures(
    db: Session = Depends(get_db),
    current_user: Compte = Depends(get_current_user)
):
    _ = current_user
    temperatures = db.query(Temperature).all()
    return temperatures


class TemperatureCreate(BaseModel):
    degre: float = Field(..., ge=-100, le=100)
    localisation: str | LocalisationEnum
    date_temperature: date
    heure: time | None = None
    compte_id: int


@router.post("")
def create_temperature(
    temperature_data: TemperatureCreate,
    db: Session = Depends(get_db),
    current_user: Compte = Depends(get_current_user)
):
    _ = current_user
    compte = db.query(Compte).filter(Compte.id == temperature_data.compte_id).first()
    if compte is None:
        raise HTTPException(
            status_code=404,
            detail="Compte introuvable"
        )

    nouvelle_temperature = Temperature(
        degre=temperature_data.degre,
        localisation=temperature_data.localisation,
        date_temperature=temperature_data.date_temperature,
        heure=temperature_data.heure,
        compte_id=temperature_data.compte_id
    )

    db.add(nouvelle_temperature)
    db.commit()
    db.refresh(nouvelle_temperature)

    return nouvelle_temperature


class TemperatureUpdate(BaseModel):
    degre: float | None = Field(default=None, ge=-100, le=100)
    localisation: str | None | LocalisationEnum = None
    date_temperature: date | None = None
    heure: time | None = None
    compte_id: int | None = None
    id: int | None = None


@router.put("/{id}")
@router.patch("/{id}")
def update_temperature(
    id: int,
    temperature_data: TemperatureUpdate,
    db: Session = Depends(get_db),
    current_user: Compte = Depends(get_current_user)
):
    _ = current_user
    temperature = db.query(Temperature).filter(Temperature.id == id).first()
    if temperature is None:
        raise HTTPException(
            status_code=404,
            detail="Température introuvable"
        )

    if temperature_data.id is not None and temperature_data.id != id:
        raise HTTPException(
            status_code=400,
            detail="L'ID de la température ne peut pas être modifié"
        )

    if temperature_data.compte_id is not None:
        compte = db.query(Compte).filter(Compte.id == temperature_data.compte_id).first()
        if compte is None:
            raise HTTPException(
                status_code=404,
                detail="Compte introuvable"
            )
        temperature.compte_id = temperature_data.compte_id

    if temperature_data.degre is not None:
        temperature.degre = temperature_data.degre
    if temperature_data.localisation is not None:
        temperature.localisation = temperature_data.localisation
    if temperature_data.date_temperature is not None:
        temperature.date_temperature = temperature_data.date_temperature
    if "heure" in temperature_data.model_fields_set:
        temperature.heure = temperature_data.heure

    db.commit()
    db.refresh(temperature)

    return temperature


@router.delete("/{id}")
def delete_temperature(
    id: int,
    db: Session = Depends(get_db),
    current_user: Compte = Depends(get_current_user)
):
    _ = current_user
    temperature = db.query(Temperature).filter(Temperature.id == id).first()
    if temperature is None:
        raise HTTPException(
            status_code=404,
            detail="Température introuvable"
        )

    db.delete(temperature)
    db.commit()

    return {"message": "Température supprimée avec succès"}


@router.get("/compte/{compte_id}")
def get_temperatures_by_compte(
    compte_id: int,
    db: Session = Depends(get_db),
    current_user: Compte = Depends(get_current_user)
):
    _ = current_user
    compte = db.query(Compte).filter(Compte.id == compte_id).first()
    if compte is None:
        raise HTTPException(
            status_code=404,
            detail="Compte introuvable"
        )

    temperatures = db.query(Temperature).filter(Temperature.compte_id == compte_id).order_by(Temperature.date_temperature.desc(), Temperature.heure.desc()).all()
    return temperatures