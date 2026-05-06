from fastapi import APIRouter


router = APIRouter(prefix='/children')

@router.get("/")
def root():
    return {"message": "Router Children OK"}

