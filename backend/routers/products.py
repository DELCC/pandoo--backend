from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import json

from schemas import ProductCreate, ProductRead
from models import Product, Child
from db.database import get_db

router = APIRouter(prefix='/products', tags=["Products"])

# --- ROUTE POUR ENREGISTRER UN PRODUIT ---
@router.post("/", response_model=ProductRead)
def add_products(id_child: int, product: ProductCreate, db: Session = Depends(get_db)):
    # 1. Vérification si l'enfant existe
    child = db.query(Child).filter(Child.id == id_child).first()

    if not child:
        raise HTTPException(
            status_code=404,
            detail="Enfant non trouvé"
        )

    # 2. LOGIQUE ANTI-DOUBLON (Évite d'enregistrer 2 fois le même scan pour le même enfant)
    existing_product = db.query(Product).filter(
        Product.barcode == product.barcode,
        Product.id_child == id_child
    ).first()

    if existing_product:
        print(f"⚠️ Produit déjà existant : {product.name}")
        return existing_product

    # 3. Création du nouveau produit
    # On s'assure de bien mapper tous les champs reçus du frontend
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
        id_child=id_child
    )
    
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        print(f"✅ Produit enregistré avec succès : {new_product.name}")
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur BDD : {str(e)}")

# --- VOIR TOUS LES PRODUITS (CORRECTIF ACCENTS) ---
@router.get("/", response_model=List[ProductRead])
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    
    # Pour forcer les accents dans le navigateur, on transforme en dictionnaire 
    # et on renvoie via JSONResponse avec le charset UTF-8
    products_list = []
    for p in products:
        products_list.append({
            "id": p.id,
            "barcode": p.barcode,
            "name": p.name,
            "type": p.type,
            "brand": p.brand,
            "calories": p.calories,
            "glucides": p.glucides,
            "proteins": p.proteins,
            "lipids": p.lipids,
            "salt": p.salt,
            "calcium": p.calcium,
            "id_child": p.id_child
        })
    
    return JSONResponse(
        content=products_list,
        media_type="application/json; charset=utf-8"
    )

# --- VOIR LES PRODUITS D'UN ENFANT PRÉCIS ---
@router.get("/child/{id_child}", response_model=List[ProductRead])
def get_products_by_child(id_child: int, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.id_child == id_child).all()
    
    products_data = [
        {
            "id": p.id, "barcode": p.barcode, "name": p.name, 
            "type": p.type, "brand": p.brand, "calories": p.calories,
            "glucides": p.glucides, "proteins": p.proteins, "salt": p.salt,
            "id_child": p.id_child
        } for p in products
    ]
    
    return JSONResponse(
        content=products_data,
        media_type="application/json; charset=utf-8"
    )