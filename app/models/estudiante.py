from sqlalchemy import Column, Integer, String
from app.database.connection import Base

class Estudiante(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "estudiantes"

    # Datos y claves foraneas
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    matricula = Column(String(50), unique=True, nullable=False)
    curso = Column(String(20), nullable=False)
    correo = Column(String(100), nullable=False)
