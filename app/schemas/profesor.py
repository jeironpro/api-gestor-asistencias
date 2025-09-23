from pydantic import BaseModel, ConfigDict

class ProfesorBase(BaseModel):
    nombre: str
    correo: str
    especialidad: str

# Para crear un profesor (POST)
class ProfesorCreate(ProfesorBase):
    pass

# Para devolver un profesor en respuesta
class ProfesorResponse(ProfesorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)