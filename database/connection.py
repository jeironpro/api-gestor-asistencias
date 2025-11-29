# Importaciones
import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# URL de conexión de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)


# Depedencia para obtener la sesión de la BD
def obtener_db():
    db = Session(engine)

    try:
        yield db
    finally:
        db.close()

    return db
