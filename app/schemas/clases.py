"""
    BaseModel: es la clase base de pydantic para definir modelos de datos tipados y validados. Cuando se crea una clase que hereda de BaseModel, pydantic:
    · Valida automáticamente los tipos de los campos.
    · Permite valores por defecto.
    · Convierte tipos automáticamente si es posible (coerción de tipos).
    · Genera métodos útiles como .dict(), .json(), .copy().

    ConfigDict: reemplaza a la antigua clase Config usada en pydatic v1. Sirve para configurar el comportamiento del modelo:
    · Validación estricta o permisiva.
    · Alias de campos.
    · Cómo serializar/parsear datos.
    · Configuraciones generales del modelo.

    Parámetros comunes de ConfigDict:
    extra: "ignore", "allow", "forbid" para campos extra.
    frozen: True hace el modelo inmutable.
    populate_by_name: permite usar alias de campos al crear el modelo.
    validate_assignment: valida valores al reasignarlos después de crear el modelo.
    from_attributes: True habilita la creación de modelos a partir de objetos con atributos, no solo diccionarios. Es ideal para integrar pydantic con ORM. Se usa junto con model_config.
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ClaseBase(BaseModel):
    nombre: str
    fecha: datetime
    horaInicio: datetime
    horaFin: datetime

# Para crear una clase (POST)
class CrearClase(ClaseBase):
    pass

# Para devolver una clase en respuesta
class RespuestaClase(ClaseBase):
    id: str
    profesorId: str

    model_config = ConfigDict(from_attributes=True)