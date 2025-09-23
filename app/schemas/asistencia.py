from pydantic import BaseModel, ConfigDict
from datetime import date

class AsistenciaBase(BaseModel):
    fecha: date
    estado: str

# Para crear asistencia (POST)
class AsistenciaCreate(AsistenciaBase):
    estudiante_id: int
    clase_id: int

# Para devolver una asistencia en respuesta
class AsistenciaResponse(AsistenciaBase):
    id: int
    estudiante_id: int
    clase_id: int

    model_config = ConfigDict(from_attributes=True)