"""
    Column: es la función principal para definir una columna de una tabla en SQLAlchemy. Se usa dentro de una clase que hereda de Base(declarative_base())
    
    Integer: representa numero enteros para la columna.
    
    ForeignKey: define una relación con otra tabla (clave foránea). Se pasa como argumento una referencia en forma de cadena (tabla.columna).
    
    Date: representa fechas (solo dia, mes y año) para columna.
    
    String: representa cadenas de texto para la columna.
"""
from sqlalchemy import Column, Integer, ForeignKey, Date, String

"""
    relationship: no crea columnas en la base de datos. Es una función de SQLAlchemy que define cómo las clases Python (modelos) se relacionan entre sí. Permite acceder a los objetos relacionados de forma automática, sin tener que escribir joins manuales en SQL.

    Permite definir cascadas, es decir, eliminar automáticamente los objetos relacionados si se borra el padre.
"""
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Asistencia(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "asistencias"

    # Datos y claves foraneas
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"))
    clase_id = Column(Integer, ForeignKey("clases.id"))
    fecha = Column(Date, nullable=False)
    estado = Column(String(10), nullable=False)

    # Relaciones
    estudiante = relationship("Estudiante", backref="asistencias")
    clase = relationship("Clase", backref="asistencias")