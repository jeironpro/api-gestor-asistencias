# Importaciones
from datetime import date, time

from sqlmodel import SQLModel


class CrearClase(SQLModel):
    """
    Esquema para crear una clase.

    Campos:
        nombre: str - Nombre de la clase.
        fecha: date - Fecha de la clase.
        horaInicio: time - Hora de inicio de la clase.
        horaFin: time - Hora de fin de la clase.
    """

    nombre: str
    fecha: date
    horaInicio: time
    horaFin: time


class RespuestaClase(CrearClase):
    """
    Esquema para devolver una clase.

    Hereda de CrearClase.
    Campos heredados:
        nombre: str - Nombre de la clase.
        fecha: date - Fecha de la clase.
        horaInicio: time - Hora de inicio de la clase.
        horaFin: time - Hora de fin de la clase.

    Campos adicionales:
        id: str - Identificador único del usuario
        profesorId: str - Identificador del usuario (clave foranea).
    """

    id: str
    profesorId: str
