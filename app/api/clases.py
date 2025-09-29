"""
    APIRouter: sirve para organizar rutas de manera modular. Permite separar los endpoints en módulos independientes y facilita agregar prefijos, tags y dependencias comunes a grupos de rutas.
    
    El prefix significa que todos los endpoints de ese archivo estará bajo esa ruta. 
    El tags organiza mejor la documentación en /docs.
    
    Depends: Sirve para inyectar dependencias en los endpoints. Permite reutilizar funciones que proporcionan servicios, autenticación, sesiones de base de datos, etc. FastAPI las llama automáticamente y pasa el resultado al endpoint. 
    
    HTTPException: Sirve para devolver errores HTTP con código y detalle. Detiene la ejecución del endpoint y envía una respuesta HTTP con el código de error.

    List: es un tipo genérico que se usa para anotar listas con tipos específicos de elementos. 
    
    · Se puede usar List[str] directamente.
    · Se usa para tipado estático, validación y autocompletado.
    · Muy común en pydantic y FastAPI para definir campos que son listas de valores.

    · List[int]: lista de enteros.
    · List[str]: lista de cadenas de texto.
    · List[float]: lista de números flotantes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.usuarios import Usuario, RolUsuario
from app.api.usuarios import requerir_rol
from app.schemas.clases import CrearClase, RespuestaClase
from app.services.clase_service import crear_clase_service, obtener_clases_service
from app.database.connection import obtener_db

router = APIRouter(prefix="/clases", tags=["clases"])

# Crear clase
@router.post("/", response_model=RespuestaClase)
def crear_clase(clase: CrearClase, db: Session = Depends(obtener_db), profesor: Usuario = Depends(requerir_rol(RolUsuario.profesor))):
    return crear_clase_service(db, clase, profesor.id)

# Listar clases
@router.get("/", response_model=List[RespuestaClase])
def lista_clases(db: Session = Depends(obtener_db)):
    return obtener_clases_service(db)
