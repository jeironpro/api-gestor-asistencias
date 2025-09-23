from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Construcción de la URL de la base de datos con el tipo de base datos + libreria://usuario/contraseña@anfitrion:puerto que usa el tipo de base de datos/nombre de la base datos desde settings
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Creación del motor de SQLAlchemy usando la función create_engine de su libreria
engine = create_engine(DATABASE_URL, echo=True)

# Crear SessionLocal para manejar las sesiones usando el creador de sesiones sessionmaker de SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para heredar en los modelos
Base = declarative_base()