from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Construcción de la URL de la base de datos con el tipo de base datos + libreria://usuario/contraseña@anfitrion:puerto que usa el tipo de base de datos/nombre de la base datos desde settings
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Creación del motor de SQLAlchemy usando la función create_engine de su libreria
"""
    create_engine(): es la función que crea el motor de conexión con la base de datos.
    El engine es el objeto central de SQLAlchemy que sabe cómo hablar con la base de datos (MySQL, PostgreSQL, SQLite, etc.).

    Parámetro URL: es una cadena de conexión que le dice a SQLAlchemy: 
    · qué motor usar. 
    · en qué servidor está la base de datos.
    · qué usuario / contraseña.
    · qué puerto.
    · qué nombre de base de datos

    Parámetro echo: imprime en la consola todas las sentencias SQL que ejecuta. 
"""
engine = create_engine(DATABASE_URL, echo=True)

# Crear SessionLocal para manejar las sesiones usando el creador de sesiones sessionmaker de SQLAlchemy
"""
    sessionmaker(): es un fabricante de sesiones. Donde una sesión es el objeto que maneja todas las operaciones sobre la base de datos como: consultas, inserciones, actualizaciones y eliminaciones.

    Crea objetos Session configurados para el engine. 

    Parámetro autocommit=False: necesitas llamar a commit() manualmente.
    Parámetro autoflush=False: sincroniza automáticamente los cambios pendientes anter de ejecutar sentencias.
    Parámetro bind=engine: le dice al sessionmaker a qué motor debe conectarse cuando se crea una sesión.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para heredar en los modelos
"""
    declarative_base(): es una función de SQLAlchemy que devuelve una clase base.
    Esa clase base sirve como punto de partuda para crear modelos ORM (clases de Python que representan tablas de la base de datos).

    Crea dinámicamente una clase llamada Base. Esa Clase contiene:
    · Un mapeador ORM que conecta las clases con las tablas.
    · Un atributo especial .metadata donde se guarda toda la información del esquema (tablas, columnas, relaciones...).
"""
Base = declarative_base()

# Depedencia para obtener la sesión de la BD
def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()