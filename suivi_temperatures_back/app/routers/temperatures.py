from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Temperature


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"]
)


@router.get("")
def get_temperatures(db: Session = Depends(get_db)):
    temperatures = db.query(Temperature).all()
    return temperatures