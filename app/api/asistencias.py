"""
    APIRouter: sirve para organizar rutas de manera modular. Permite separar los endpoints en módulos independientes y facilita agregar prefijos, tags y dependencias comunes a grupos de rutas.
    
    Depends: Sirve para inyectar dependencias en los endpoints. Permite reutilizar funciones que proporcionan servicios, autenticación, sesiones de base de datos, etc. FastAPI las llama automáticamente y pasa el resultado al endpoint. 
    
    HTTPException: Sirve para devolver errores HTTP con código y detalle. Detiene la ejecución del endpoint y envía una respuesta HTTP con el código de error.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

"""
    List: es un tipo genérico que se usa para anotar listas con tipos específicos de elementos. 
    
    · Se puede usar List[str] directamente.
    · Se usa para tipado estático, validación y autocompletado.
    · Muy común en pydantic y FastAPI para definir campos que son listas de valores.

    · List[int]: lista de enteros.
    · List[str]: lista de cadenas de texto.
    · List[float]: lista de números flotantes.
"""
from typing import List
from typing import List
from app.schemas.asistencia import AsistenciaCreate, AsistenciaResponse
from app.services.asistencia_service import (create_asistencia, get_asistencias, get_asistencia_by_id, update_asistencia_by_id, delete_asistencia_by_id) 
from app.database.connection import SessionLocal

"""
    El prefix significa que todos los endpoints de ese archivo estará bajo esa ruta. 
    El tags organiza mejor la documentación en /docs.
"""
router = APIRouter(prefix="/asistencias", tags=["Asistencias"])

# Depedencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear asistencia
@router.post("/", response_model=AsistenciaResponse)
def create_asistencia_endpoint(asistencia: AsistenciaCreate, db: Session = Depends(get_db)):
    return create_asistencia(db, asistencia)

# Listar asistencias
@router.get("/", response_model=List[AsistenciaResponse])
def list_asistencias(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_asistencias(db, skip=skip, limit=limit)

# Obtener asistencia por ID
@router.get("/{asistencia_id}", response_model=AsistenciaResponse)
def get_asistencia(asistencia_id: int, db: Session = Depends(get_db)):
    db_asistencia = get_asistencia_by_id(db, asistencia_id)

    if not db_asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    
    return db_asistencia

# Actualizar asistencia por ID
@router.put("/{asistencia_id}", response_model=AsistenciaResponse)
def update_asistencia_by_id(asistencia_id: int, asistencia_data: AsistenciaCreate, db: Session = Depends(get_db)):
    db_asistencia = update_asistencia_by_id(db, asistencia_id, asistencia_data)

    if not db_asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    
    return db_asistencia

# Eliminar asistencia por ID
@router.delete("/{asistencia_id}", response_model=AsistenciaResponse)
def delete_asistencia_by_id(asistencia_id: int, db: Session = Depends(get_db)):
    db_asistencia = delete_asistencia_by_id(db, asistencia_id)

    if not db_asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    
    return db_asistencia