"""
    Column: es la función principal para definir una columna de una tabla en SQLAlchemy. Se usa dentro de una clase que hereda de Base(declarative_base())
    
    Integer: representa numero enteros para la columna.
    
    String: representa cadenas de texto para la columna.
"""
from sqlalchemy import Column, Integer, String

"""
    relationship: no crea columnas en la base de datos. Es una función de SQLAlchemy que define cómo las clases Python (modelos) se relacionan entre sí. Permite acceder a los objetos relacionados de forma automática, sin tener que escribir joins manuales en SQL.

    Permite definir cascadas, es decir, eliminar automáticamente los objetos relacionados si se borra el padre.
"""
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