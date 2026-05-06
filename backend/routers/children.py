from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import ChildCreate, ChildRead
from models import Child, User
from db.database import get_db

router = APIRouter(
    prefix="/children",
    tags=["Children"]
)


@router.post("/{parent_id}", response_model=ChildRead)
def create_child(
    parent_id: int,
    child: ChildCreate,
    db: Session = Depends(get_db)
):
    """
    Créer un enfant lié à un parent
    """

    # Vérifie que le parent existe
    parent = db.query(User).filter(User.id == parent_id).first()
    

    if not parent:
        raise HTTPException(
            status_code=404,
            detail="Parent introuvable"
        )

    # Création enfant
    new_child = Child(
        name=child.name,
        age=child.age,
        id_parent=parent.id
    )

    db.add(new_child)
    db.commit()
    db.refresh(new_child)

    return new_child

@router.get("/")
def list_all_children(db : Session = Depends(get_db)):
    return db.query(Child).all()

@router.get("/{parent_id}")
def list_parent_children(parent_id : int, db : Session = Depends(get_db)):
    return db.query(Child).filter(Child.id_parent == parent_id).all()