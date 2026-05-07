from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password : str

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr


class ChildCreate(BaseModel):
    name : str
    age : int
    id_parent : int

class ChildRead(BaseModel):
    id : int
    name : str
    age : int
    id_parent : int

class ProductCreate(BaseModel):
    barcode : int
    type : str
    name : str
    brand : str
    calories: float
    calcium: float
    proteins : float
    lipids : float
    salt : float


class ProductRead(BaseModel):
    id : int
    barcode : int
    type : str
    name : str
    brand : str
    calories: float
    calcium: float
    proteins : float
    lipids : float
    salt : float
    id_child : int


class StoryCreate(BaseModel):
    pass

class StoryRead(BaseModel):
    pass

model_config = {"from_attributes": True} # Permet de lire un objet ORM SqlAlchemy