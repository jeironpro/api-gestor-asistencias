from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Clase(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "clases"

    # Datos y claves foraneas
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    profesor_id = Column(Integer, ForeignKey("profesores.id"))
    horario = Column(String(30), nullable=False)

    # Relaciones
    profesor = relationship("Profesor", back_populates="clases")
