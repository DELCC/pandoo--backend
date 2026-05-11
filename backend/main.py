from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Importation de la base de données et des modèles
from db.database import engine
import models

# Importation des routeurs
from routers import users, children, products

# --- CRÉATION DES TABLES ---
# Cela crée le fichier pandoo.db automatiquement s'il n'existe pas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pandoo API",
    description="Backend pour l'application de nutrition enfantine",
    version="1.1.0"
)

# --- CONFIGURATION CORS ---
# Permet à ton application Kivy (ou un navigateur) de communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- INCLUSION DES ROUTEURS ---
app.include_router(users.router)
app.include_router(children.router)
app.include_router(products.router)

# --- ROUTE RACINE (Correction des accents) ---
@app.get("/", tags=["Root"])
async def read_root():
    return JSONResponse(
        content={"message": "API Pandoo opérationnelle"},
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

# --- POINT D'ENTRÉE ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)