# Importaciones
import uuid
from sqlmodel import SQLModel, Field
from datetime import datetime, time
from database.zone_horary import madrid_utc

class Clase(SQLModel, table=True):
    """
        Modelo que define la tabla de clases.

        Campos:
            id: str (primary key) - Identificador único del usuario (UUID4 genera un identificador único global de 128 bits).
            nombre: str - Nombre de la clase.
            fecha: datetime - Fecha de la clase.
            horaInicio: time - Hora de inicio de la clase.
            horaFin: time - Hora de fin de la clase.
            profesorId: str - Identificador del profesor (clave foranea).
    """
    __tablename__ = "clase" # Nombre de la tabla en la base de datos

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="Identificador único del usuario"
    )
    nombre: str = Field(max_length=50, nullable=False, description="Nombre de la clase")
    fecha: datetime = Field(default_factory=madrid_utc, description="Fecha de la clase")
    horaInicio: time = Field(nullable=False, description="Hora de inicio de la clase")
    horaFin: time = Field(nullable=False, description="Hora de fin de la clase")
    profesorId: str = Field(
        foreign_key="usuario.id",
        nullable=False,
        description="Identificador del profesor (clave foranea)"
    )
