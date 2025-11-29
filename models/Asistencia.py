# Importaciones
import uuid
from datetime import datetime

from sqlmodel import Field, SQLModel

from database.zone_horary import madrid_utc
from models.Enum import EstadoAsistencia


class Asistencia(SQLModel, table=True):
    """
    Modelo que define la tabla de asistencias.

    Campos:
        id: str (pk) - UUID4 genera un identificador único global de 128 bits.
        fecha: datetime - Fecha de la asistencia.
        estado: EstadoAsistencia - Estado de la asistencia.
        usuarioId: str - Identificador del usuario (fk).
        claseId: str - Identificador de la clase (fk).
    """

    __tablename__ = "asistencia"  # Nombre de la tabla en la base de datos

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Identificador único del usuario",
    )
    fecha: datetime = Field(
        default_factory=madrid_utc, description="Fecha de la asistencia"
    )
    estado: EstadoAsistencia = Field(
        nullable=False, description="Estado de la asistencia"
    )

    usuarioId: str = Field(
        foreign_key="usuario.id",
        nullable=False,
        description="Identificador del usuario",
    )
    claseId: str = Field(
        foreign_key="clase.id", nullable=False, description="Identificador de la clase"
    )
