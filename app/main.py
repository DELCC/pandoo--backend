from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base
from app.models import User, Child, Scan, Reward

app = FastAPI(
    title="Pandoo API",
    description="Le backend de Pandoo, l'application nutrition pour enfants 🐼",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API Pandoo 🐼"}