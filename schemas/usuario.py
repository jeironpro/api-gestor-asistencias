# Importaciones
from sqlmodel import SQLModel
from models.Usuario import RolUsuario
from typing import Optional
from datetime import datetime


class CrearUsuario(SQLModel):
    """
    Esquema para crear un usuario.

    Campos:
        nombre: str - Nombre del usuario.
        apellido: str - Apellido del usuario.
        correoElectronico: str - Correo electrónico del usuario.
        contrasena: str - Contraseña del usuario.
        rol: RolUsuario - Rol del usuario.
    """

    nombre: str
    apellido: str
    correoElectronico: str
    contrasena: str
    rol: RolUsuario


class ActualizarUsuario(SQLModel):
    """
    Esquema para actualizar un usuario.

    Campos:
        nombre: Optional[str] - Nombre del usuario.
        apellido: Optional[str] - Apellido del usuario.
        contrasena: Optional[str] - Contraseña del usuario.
        rol: Optional[RolUsuario] - Rol del usuario.
    """

    nombre: Optional[str] = None
    apellido: Optional[str] = None
    contrasena: Optional[str] = None
    rol: Optional[RolUsuario] = None


class RespuestaUsuario(SQLModel):
    """
    Esquema para devolver un usuario.

    Campos:
        id: str - Identificador único del usuario
        nombre: str - Nombre del usuario.
        apellido: str - Apellido del usuario.
        correoElectronico: str - Correo electrónico del usuario.
        rol: RolUsuario - Rol del usuario.
        fechaRegistro: datetime - Fecha de registro del usuario.
        activo: bool - Estado del usuario.
    """

    id: str
    nombre: str
    apellido: str
    correoElectronico: str
    rol: RolUsuario
    fechaRegistro: datetime
    activo: bool


class Token(SQLModel):
    """
    Esquema para devolver un token.

    Campos:
        access_token: str - Token de acceso.
        token_type: str - Tipo de token.
    """

    access_token: str
    token_type: str
