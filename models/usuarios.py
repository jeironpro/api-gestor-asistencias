import enum
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from database.connection import Base
from datetime import datetime
from zoneinfo import ZoneInfo

zona_es = ZoneInfo("Europe/Madrid")

class RolUsuario(str, enum.Enum):
    admin = "admin"
    profesor = "profesor"
    estudiante = "estudiante"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String(36), primary_key=True, index=True, default=lambda:str(uuid.uuid4()))
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(60), nullable=False)
    correoElectronico = Column(String(100), unique=True, index=True, nullable=False)
    contrasena = Column(String(100), nullable=False)
    rol = Column(Enum(RolUsuario), nullable=False)
    fechaRegistro = Column(DateTime, default=lambda: datetime.now(zona_es))
    activo = Column(Boolean, default=True)

    clases = relationship("Clase", back_populates="profesor")
    asistencias = relationship("Asistencia", back_populates="usuario")