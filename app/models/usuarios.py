import enum
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from datetime import datetime, timezone
from app.database.connection import Base

class RolUsuario(str, enum.Enum):
    admin = "admin"
    profesor = "profesor"
    estudiante = "estudiante"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, index=True, default=lambda:str(uuid.uuid4()))
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correoEletronico = Column(String, unique=True, index=True, nullable=False)
    contrasena = Column(String, nullable=False)
    rol = Column(Enum(RolUsuario), nullable=False)
    fechaRegistro = Column(DateTime, default=datetime.utcnow())
    activo = Column(Boolean, default=True)