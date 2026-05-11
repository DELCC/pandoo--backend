from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# On définit le chemin pour que la DB soit à la racine du dossier backend
BASE_DIR = Path(__file__).resolve().parent.parent
SQLALCHEMY_DATABASE_URL = f"sqlite:///{BASE_DIR}/pandoo.db"

# Mise à jour du moteur avec support explicite de l'UTF-8
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Optionnel : Forcer SQLite à utiliser l'encodage UTF-8 à chaque connexion
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA encoding = 'UTF-8'")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()