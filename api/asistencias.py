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
from typing import List
from schemas.asistencias import CrearAsistencia, RespuestaAsistencia
from services.asistencia_service import crear_asistencia_service, obtener_asistencias_service, obtener_asistencia_service
from database.connection import obtener_db

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])

# Crear asistencia
@router.post("/", response_model=RespuestaAsistencia)
def crear_asistencia(asistencia: CrearAsistencia, db: Session = Depends(obtener_db)):
    return crear_asistencia_service(db, asistencia)

# Lista de asistencias
@router.get("/", response_model=List[RespuestaAsistencia])
def lista_asistencias(db: Session = Depends(obtener_db)):
    return obtener_asistencias_service(db)

# Lista asistencias por clase o estudiante
# @router.get("/", response_model=List[RespuestaAsistencia])
# def lista_asistencias_clase_usuario(id_clase: str | None = None, id_usuario: str | None = None, db: Session = Depends(obtener_db)):
#     return obtener_asistencia_service(db, id_clase, id_usuario)