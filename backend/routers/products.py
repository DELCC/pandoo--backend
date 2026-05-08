from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas import ProductCreate, ProductRead
from models import Product, Child
from db.database import get_db

router = APIRouter(prefix='/products', tags=["Products"])

# --- ROUTE POUR ENREGISTRER UN PRODUIT (AVEC ANTI-DOUBLON) ---
@router.post("/", response_model=ProductRead)
def add_products(id_child: int, product: ProductCreate, db: Session = Depends(get_db)):
    # 1. Vérification si l'enfant existe
    child = db.query(Child).filter(Child.id == id_child).first()

    if not child:
        raise HTTPException(
            status_code=404,
            detail="Enfant non trouvé"
        )

    # 2. LOGIQUE ANTI-DOUBLON
    existing_product = db.query(Product).filter(
        Product.barcode == product.barcode,
        Product.id_child == id_child
    ).first()

    if existing_product:
        # On affiche un message bien visible dans le terminal de l'API
        print("\n" + "="*50)
        print(f"   INFO : L'article '{product.name}' (BC: {product.barcode})")
        print(f"   est DÉJÀ enregistré pour l'enfant ID: {id_child}")
        print("="*50 + "\n")
        return existing_product

    # 3. Création du nouveau produit si c'est un nouveau scan pour cet enfant
    new_product = Product(
        barcode=product.barcode,
        type=product.type,
        name=product.name,
        brand=product.brand,
        calories=product.calories,
        glucides=product.glucides, 
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

# --- VOIR TOUS LES PRODUITS ENREGISTRÉS ---
@router.get("/", response_model=List[ProductRead])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# --- VOIR LES PRODUITS D'UN ENFANT PRÉCIS ---
@router.get("/child/{id_child}", response_model=List[ProductRead])
def get_products_by_child(id_child: int, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.id_child == id_child).all()
    return products