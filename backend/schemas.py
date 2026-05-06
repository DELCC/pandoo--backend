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

class ChildRead(BaseModel):
    id : int
    name : str
    id_parent : int

model_config = {"from_attributes": True} # Permet de lire un objet ORM SqlAlchemy