from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    Integer,
    Numeric,
    String,
    Time,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.database import Base


class Compte(Base):
    __tablename__ = "compte"

    id = Column(Integer, primary_key=True, index=True)
    nom_compte = Column(String)
    prenom_compte = Column(String)
    email_compte = Column(String)
    mdp = Column(String)
    mdp_crypted = Column(String)
    tel = Column(String)
    adresse = Column(String)
    adresse_comp = Column(String)
    cp = Column(String)
    ville = Column(String)
    pays = Column(String)
    fonction = Column(String)

    temperatures = relationship(
        "Temperature",
        back_populates="compte_relation"
    )


class Temperature(Base):
    __tablename__ = "temperature"

    id = Column(BigInteger, primary_key=True, index=True)
    degre = Column(Numeric(3, 2))
    localisation = Column(String)
    date_temperature = Column(Date, nullable=False)
    heure = Column(Time)

    compte_id = Column(
        "compte",
        Integer,
        ForeignKey("compte.id"),
        nullable=False
    )

    compte_relation = relationship(
        "Compte",
        back_populates="temperatures"
    )