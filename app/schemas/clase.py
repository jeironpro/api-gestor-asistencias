from pydantic import BaseModel, ConfigDict

class ClaseBase(BaseModel):
    nombre: str
    horario: str

# Para crear una clase (POST)
class ClaseCreate(ClaseBase):
    profesor_id: int

# Para devolver una clase en respuesta
class ClaseResponse(ClaseBase):
    id: int
    profesor_id: int

    model_config = ConfigDict(from_attributes=True)