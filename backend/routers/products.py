from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas import ProductCreate, ProductRead
from models import Product, Child
from db.database import get_db

router = APIRouter(prefix='/products', tags=["Products"])

# --- ROUTE POUR ENREGISTRER ---
@router.post("/", response_model=ProductRead)
def add_products(id_child: int, product: ProductCreate, db: Session = Depends(get_db)):
    # 1. Vérification si l'enfant existe
    child = db.query(Child).filter(Child.id == id_child).first()

    if not child:
        raise HTTPException(
            status_code=404,
            detail="Child not found"
        )

    # 2. Création du nouveau produit (AVEC GLUCIDES)
    new_product = Product(
        barcode=product.barcode,
        type=product.type,
        name=product.name,
        brand=product.brand,
        calories=product.calories,
        glucides=product.glucides,  # <--- IL MANQUAIT CETTE LIGNE ICI !
        calcium=product.calcium,
        proteins=product.proteins,
        lipids=product.lipids,
        salt=product.salt,
        id_child=child.id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# --- VOIR TOUS LES PRODUITS ---
@router.get("/", response_model=List[ProductRead])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# --- VOIR LES PRODUITS D'UN ENFANT PRÉCIS ---
@router.get("/child/{id_child}", response_model=List[ProductRead])
def get_products_by_child(id_child: int, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.id_child == id_child).all()
    return products