# Importaciones
import os

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

# Cargar variables de entorno
load_dotenv()


# Obtener motor de la base de datos
def get_engine():
    # URL de conexión de la base de datos
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        DATABASE_URL = "sqlite:///database.db"

    return create_engine(DATABASE_URL, echo=True)


# Motor de la base de datos
engine = get_engine()


# Depedencia para obtener la sesión de la BD
def obtener_db():
    with Session(engine) as session:
        yield session
