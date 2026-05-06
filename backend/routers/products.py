from fastapi import APIRouter


router = APIRouter(prefix='/products')

@router.get("/")
def root():
    return {"message": "Router Products OK"}
