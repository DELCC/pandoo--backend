from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import UserCreate
from models import User
from db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    """Test"""
    return db.query(User).all()


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Créer un compte utilisateur
    """

    # Création de l'objet SQLAlchemy
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    # Sauvegarde en base
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Utilisateur créé avec succès",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }