# Importaciones
import uuid
from sqlmodel import SQLModel, Field
from datetime import datetime
from database.zone_horary import madrid_utc
from models.Enum import RolUsuario


class Usuario(SQLModel, table=True):
    """
    Modelo que define la tabla de usuarios.

    Campos:
        id: str (pk) - UUID4 genera un identificador único global de 128 bits.
        nombre: str - Nombre del usuario.
        apellido: str - Apellido del usuario.
        correoElectronico: str - Correo electrónico del usuario.
        contrasena: str - Contraseña del usuario.
        rol: RolUsuario - Rol del usuario.
        fechaRegistro: datetime - Fecha de registro del usuario.
        activo: bool - Estado del usuario.
    """

    __tablename__ = "usuario"  # Nombre de la tabla en la base de datos.

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Identificador único del usuario",
    )
    nombre: str = Field(max_length=50, nullable=False, description="Nombre del usuario")
    apellido: str = Field(
        max_length=60, nullable=False, description="Apellido del usuario"
    )
    correoElectronico: str = Field(
        max_length=100,
        unique=True,
        index=True,
        nullable=False,
        description="Correo electrónico del usuario",
    )
    contrasena: str = Field(nullable=False, description="Contraseña del usuario")
    rol: RolUsuario = Field(nullable=False, description="Rol del usuario")
    fechaRegistro: datetime = Field(
        default_factory=madrid_utc, description="Fecha de registro del usuario"
    )
    activo: bool = Field(default=True, description="Estado del usuario")
