# Importaciones
from datetime import datetime

from sqlmodel import SQLModel

from models.Asistencia import EstadoAsistencia


class CrearAsistencia(SQLModel):
    """
    Esquema para crear una asistencia.

    Campos:
        usuarioId: str - Identificador del usuario (clave foranea).
        claseId: str - Identificador de la clase (clave foranea).
        estado: EstadoAsistencia - Estado de la asistencia.
    """

    usuarioId: str
    claseId: str
    estado: EstadoAsistencia


class RespuestaAsistencia(SQLModel):
    """
    Esquema para devolver una asistencia.

    Campos:
        id: str - Identificador único del usuario
        usuarioId: str - Identificador del usuario (clave foranea).
        claseId: str - Identificador de la clase (clave foranea).
        fecha: datetime - Fecha de la asistencia.
        estado: EstadoAsistencia - Estado de la asistencia.
    """

    id: str
    usuarioId: str
    claseId: str
    fecha: datetime
    estado: EstadoAsistencia
