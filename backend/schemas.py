from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

# --- SCHÉMAS UTILISATEUR ---
class UserCreate(BaseModel):
    username: str = Field(min_length=2, max_length=50) # Ajout du champ username
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password : str

class UserRead(BaseModel):
    id: int
    username: str # Ajout pour la lecture
    name: str
    email: EmailStr
    
    class Config:
        from_attributes = True

# --- SCHÉMAS ENFANT ---
class ChildCreate(BaseModel):
    name : str
    age : int
    id_parent : int

class ChildRead(BaseModel):
    id : int
    name : str
    age : int
    id_parent : int
    
    class Config:
        from_attributes = True

# --- SCHÉMAS PRODUIT ---
class ProductCreate(BaseModel):
    barcode: int
    type: str
    name: str
    brand: str
    calories: float
    glucides: float
    calcium: float
    proteins: float
    lipids: float
    salt: float

class ProductRead(BaseModel):
    id : int
    barcode : int
    type : str
    name : str
    brand : str
    calories: float
    glucides: float
    calcium: float
    proteins : float
    lipids : float
    salt : float
    id_child : int
    
    class Config:
        from_attributes = True

# --- SCHÉMAS STORY (Options) ---
class StoryCreate(BaseModel):
    pass

class StoryRead(BaseModel):
    pass