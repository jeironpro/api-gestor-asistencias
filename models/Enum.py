# Importaciones
import enum


class RolUsuario(str, enum.Enum):
    """
    Enum que define los roles de los usuarios.
    """

    admin = "admin"
    profesor = "profesor"
    estudiante = "estudiante"


class EstadoAsistencia(str, enum.Enum):
    """
    Enum que define los estados de las asistencias.
    """

    presente = "presente"
    ausente = "ausente"
    retraso = "retraso"
