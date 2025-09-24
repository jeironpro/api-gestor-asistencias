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
from app.schemas.estudiante import EstudianteCreate, EstudianteResponse
from app.services.estudiante_service import (create_estudiante, get_estudiantes, get_estudiante_by_id, update_estudiante_by_id, delete_estudiante_by_id)
from app.database.connection import SessionLocal

"""
    El prefix significa que todos los endpoints de ese archivo estará bajo esa ruta. 
    El tags organiza mejor la documentación en /docs.
"""
router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

# Depedencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear estudiante
@router.post("/", response_model=EstudianteResponse)
def create_estudiante_endpoint(estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    return create_estudiante(db, estudiante)

# Listar estudiantes
@router.get("/", response_model=List[EstudianteResponse])
def list_estudiantes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_estudiantes(db, skip=skip, limit=limit)

# Obtener estudiante por ID
@router.get("/{estudiante_id}", response_model=EstudianteResponse)
def get_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    db_estudiante = get_estudiante_by_id(db, estudiante_id)

    if not db_estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return db_estudiante

# Actualizar estudiante por ID
@router.put("/{estudiante_id}", response_model=EstudianteResponse)
def update_estudiante_by_id(estudiante_id: int, estudiante_data: EstudianteCreate, db: Session = Depends(get_db)):
    db_estudiante = update_estudiante_by_id(db, estudiante_id, estudiante_data)

    if not db_estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return db_estudiante

# Eliminar estudiante por ID
@router.delete("/{estudiante_id}", response_model=EstudianteResponse)
def delete_estudiante_by_id(estudiante_id: int, db: Session = Depends(get_db)):
    db_estudiante = delete_estudiante_by_id(db, estudiante_id)

    if not db_estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return db_estudiante