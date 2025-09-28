"""
    Column: es la función principal para definir una columna de una tabla en SQLAlchemy. Se usa dentro de una clase que hereda de Base(declarative_base())
    
    ForeignKey: define una relación con otra tabla (clave foránea). Se pasa como argumento una referencia en forma de cadena (tabla.columna).
    
    String: representa cadenas de texto para la columna.

    relationship: no crea columnas en la base de datos. Es una función de SQLAlchemy que define cómo las clases Python (modelos) se relacionan entre sí. Permite acceder a los objetos relacionados de forma automática, sin tener que escribir joins manuales en SQL.

    Permite definir cascadas, es decir, eliminar automáticamente los objetos relacionados si se borra el padre.
"""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Clase(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "clases"

    # Datos y claves foraneas
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(50), nullable=False)
    fecha = Column(DateTime, nullable=False)
    horaInicio = Column(DateTime, nullable=False)
    horaFin = Column(DateTime, nullable=False)
    profesorId = Column(String(36), ForeignKey("usuarios.id"))

    # Relaciones
    profesor = relationship("Usuario", back_populates="clases")
    asistencias = relationship("Asistencia", back_populates="clase")
