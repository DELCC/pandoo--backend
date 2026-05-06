from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from db.database import get_db
from models import User
from routers import users, children, products

app = FastAPI()
app.include_router(users.router)
app.include_router(children.router)
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "API OK"}


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"message": "Connexion DB OK"}

    except Exception as e:
        return {"error": str(e)}


