# Importar FastAPI de su libreria
from fastapi import FastAPI

# Importar los endpoints desde la API
from api import asistencia, clase, usuario
from sqlmodel import SQLModel

# Importar la base de datos y la conexión
from database.connection import engine, obtener_db
from models.Usuario import Usuario

# Inicializar la API agregando un titulo, descripción y versión para que aparezca en la documentación automática
app = FastAPI(
    title="Gestor de Asistencia",
    description="API para gestionar estudiantes, profesores, clases y asistencias",
    version="1.0.0",
)

# Registrar las rutas (endpoints) desde los módulos.
app.include_router(usuario.router)
app.include_router(clase.router)
app.include_router(asistencia.router)

# Crear todas las tablas definidas
# engine = engine() # Ya es una instancia importada

if engine:
    SQLModel.metadata.create_all(engine)
