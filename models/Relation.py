# Importaciones
from sqlmodel import Relationship
from typing import TYPE_CHECKING

# Importaciones de modelos
if TYPE_CHECKING:
    from .Usuario import Usuario
    from .Clase import Clase
    from .Asistencia import Asistencia

# Relaciones Usuario
Usuario.clases = Relationship(
    back_populates="profesor",
    sa_relationship_kwargs={"cascade": "all, delete-orphan, save-update"},
)

Usuario.asistencias = Relationship(
    back_populates="usuario",
    sa_relationship_kwargs={"cascade": "all, delete-orphan, save-update"},
)

# Relaciones Clase
Clase.profesor = Relationship(back_populates="clases")
Clase.asistencias = Relationship(back_populates="clase")

# Relaciones Asistencia
Asistencia.usuario = Relationship(back_populates="asistencias")
Asistencia.clase = Relationship(back_populates="asistencias")
