"""
    Column: es la función principal para definir una columna de una tabla en SQLAlchemy. Se usa dentro de una clase que hereda de Base(declarative_base())
    
    ForeignKey: define una relación con otra tabla (clave foránea). Se pasa como argumento una referencia en forma de cadena (tabla.columna).
    
    Date: representa fechas (solo dia, mes y año) para columna.
    
    String: representa cadenas de texto para la columna.

    relationship: no crea columnas en la base de datos. Es una función de SQLAlchemy que define cómo las clases Python (modelos) se relacionan entre sí. Permite acceder a los objetos relacionados de forma automática, sin tener que escribir joins manuales en SQL.

    Permite definir cascadas, es decir, eliminar automáticamente los objetos relacionados si se borra el padre.
"""
import enum
import uuid
from sqlalchemy import Column, DateTime, String, ForeignKey, Enum

from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime

class EstadoAsistencia(str, enum.Enum):
    presente = "presente"
    ausente = "ausente"
    tarde = "tarde"

class Asistencia(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "asistencias"

    # Datos y claves foraneas
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuarioId = Column(String(36), ForeignKey("usuarios.id"))
    claseId = Column(String(36), ForeignKey("clases.id"))
    fecha = Column(DateTime, default=datetime.utcnow)
    estado = Column(Enum(EstadoAsistencia), nullable=False)

    # Relaciones
    usuario = relationship("Usuario", back_populates="asistencias")
    clase = relationship("Clase", back_populates="asistencias")