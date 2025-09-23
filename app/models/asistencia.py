from sqlalchemy import Column, Integer, ForeignKey, Date, String
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