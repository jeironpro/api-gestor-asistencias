from pydantic import BaseModel, ConfigDict

class EstudianteBase(BaseModel):
    nombre: str
    matricula: str
    curso: str
    correo: str

# Para crear un estudiante (POST)
class EstudianteCreate(EstudianteBase):
    pass

# Para devolver un estudiante en respuesta
class EstudianteResponse(EstudianteBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)