from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import ProductCreate, ProductRead
from models import  Product, Child
from db.database import get_db


router = APIRouter(prefix='/products',  tags=["Products"])



@router.post("/",response_model = ProductRead)
def add_products(id_child : int, product : ProductCreate ,db : Session = Depends(get_db)):
    child = db.query(Child).filter(id_child == Child.id).first()

    if not child:
        raise HTTPException(
            status_code=404,
            detail="Child not found"
        )

    new_product = Product(
        barcode = product.barcode,
        type = product.type,
        name = product.name,
        brand = product.brand,
        calories = product.calories,
        calcium = product.calcium,
        proteins = product.proteins,
        lipids = product.lipids,
        salt = product.salt,
        id_child = child.id)
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
