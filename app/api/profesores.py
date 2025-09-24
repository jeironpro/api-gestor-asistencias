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
from app.schemas.profesor import ProfesorCreate, ProfesorResponse
from app.services.profesor_service import (create_profesor, get_profesores, get_profesor_by_id, update_profesor_by_id, delete_profesor_by_id)
from app.database.connection import SessionLocal

"""
    El prefix significa que todos los endpoints de ese archivo estará bajo esa ruta. 
    El tags organiza mejor la documentación en /docs.
"""
router = APIRouter(prefix="/profesores", tags=["Profesores"])

# Depedencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear profesor
@router.post("/", response_model=ProfesorResponse)
def create_profesor_endpoint(profesor: ProfesorCreate, db: Session = Depends(get_db)):
    return create_profesor(db, profesor)

# Listar profesores
@router.get("/", response_model=List[ProfesorResponse])
def get_profesores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_profesores(db, skip=skip, limit=limit)

# Obtener profesor por ID
@router.get("/{profesor_id}", response_model=ProfesorResponse)
def get_profesor(profesor_id: int, db: Session = Depends(get_db)):
    db_profesor = get_profesor_by_id(db, profesor_id)

    if not db_profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    return db_profesor

# Actualizar profesor por ID
@router.put("/{profesor_id}", response_model=ProfesorResponse)
def update_profesor_by_id(profesor_id: int, profesor_data: ProfesorCreate, db: Session = Depends(get_db)):
    db_profesor = update_profesor_by_id(db, profesor_id, profesor_data)

    if not db_profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    return db_profesor

# Eliminar profesor por ID
@router.delete("/{profesor_id}", response_model=ProfesorResponse)
def delete_profesor_by_id(profesor_id: int, db: Session = Depends(get_db)):
    db_profesor = delete_profesor_by_id(db, profesor_id)

    if not db_profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    return db_profesor