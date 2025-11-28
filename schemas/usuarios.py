from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime

class RolUsuario(str, Enum):
    admin = "admin"
    profesor = "profesor"
    estudiante = "estudiante"

class CrearUsuario(BaseModel):
    nombre: str
    apellido: str
    correoElectronico: str
    contrasena: str
    rol: RolUsuario

class ActualizarUsuario(BaseModel):
    nombre: Optional[str]
    apellido: Optional[str]
    contrasena: Optional[str]
    rol: Optional[RolUsuario]

class RespuestaUsuario(BaseModel):
    id: str
    nombre: str
    apellido: str
    correoElectronico: str
    rol: RolUsuario
    fechaRegistro: datetime
    activo: bool

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str