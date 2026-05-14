from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import UserCreate
from models import User
from db.database import get_db
import models

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

@router.get("/by-username/{username}")
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    # On nettoie l'entrée (enlève les espaces)
    search_name = username.strip()
    
    # On cherche l'utilisateur
    user = db.query(models.User).filter(models.User.name == search_name).first()
    
    if not user:
        # Si pas trouvé par nom, on tente par email par sécurité
        user = db.query(models.User).filter(models.User.email == search_name).first()

    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    
    # On renvoie l'ID réel pour que Kivy filtre les enfants
    return {
        "id": user.id,
        "name": user.name
    }

@router.get("/by-email/{email}")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    # On utilise la même logique pour la connexion Google
    search_email = email.strip()
    user = db.query(models.User).filter(models.User.email == search_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Email non reconnu")

    return {
        "id": user.id,
        "name": user.name
    }