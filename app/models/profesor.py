from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Profesor(Base):
    __tablename__ = "profesores"

    # Datos y claves foraneas
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    especialidad = Column(String(80), nullable=False)

    # Relaciones
    clases = relationship("Clase", back_populates="profesor")