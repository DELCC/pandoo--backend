from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

# Importation de la connexion à la base de données
from db.database import engine, get_db

# Importation de tes modèles pour que SQLAlchemy les connaisse
import models 

# Importation de tes routes
from routers import users, children, products

# --- INITIALISATION DE LA BASE DE DONNÉES ---
# Cette ligne va lire ton fichier models.py et créer toutes les tables 
# (utilisateurs, enfants, produits, histoires) si elles n'existent pas encore.
models.Base.metadata.create_all(bind=engine)

# --- CRÉATION DE L'APPLICATION ---
app = FastAPI(
    title="Pandoo API",
    description="Backend pour l'application Pandoo - Scan nutritionnel pour enfants",
    version="1.0.0"
)

# --- INCLUSION DES ROUTEURS ---
app.include_router(users.router)
app.include_router(children.router)
app.include_router(products.router)

# --- ROUTES DE TEST ET SANTÉ ---

@app.get("/", tags=["Health"])
def root():
    """Vérifie si l'API est en ligne."""
    return {"message": "API Pandoo opérationnelle"}

@app.get("/test-db", tags=["Health"])
def test_db(db: Session = Depends(get_db)):
    """Vérifie si la connexion à la base de données SQLite fonctionne."""
    try:
        # Exécute une requête simple
        db.execute(text("SELECT 1"))
        return {"status": "success", "message": "Connexion à la base de données OK"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Pour lancer le serveur :
# uvicorn main:app --reload