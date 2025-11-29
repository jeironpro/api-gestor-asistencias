# Importaciones
from sqlmodel import SQLModel
from datetime import date, time

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

class RespuestaClase(SQLModel):
    """
        Esquema para devolver una clase.

        Campos:
            id: str - Identificador único del usuario
            profesorId: str - Identificador del usuario (clave foranea).
    """
    id: str
    profesorId: str