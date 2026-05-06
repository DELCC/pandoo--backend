from fastapi import APIRouter


router = APIRouter(prefix='/users')

@router.get("/")
def root():
    return {"message": "Router Users OK"}

@router.post("/")
def create_user ():
    return 