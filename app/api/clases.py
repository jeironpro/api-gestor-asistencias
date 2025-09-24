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
from app.schemas.clase import ClaseCreate, ClaseResponse
from app.services.clase_service import (create_clase, get_clases, get_clase_by_id, update_clase_by_id, delete_clase_by_id)
from app.database.connection import SessionLocal

"""
    El prefix significa que todos los endpoints de ese archivo estará bajo esa ruta. 
    El tags organiza mejor la documentación en /docs.
"""
router = APIRouter(prefix="/clases", tags=["Clases"])

# Depedencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear clase
@router.post("/", response_model=ClaseResponse)
def create_clase_endpoint(clase: ClaseCreate, db: Session = Depends(get_db)):
    return create_clase(db, clase)

# Listar clases
@router.get("/", response_model=List[ClaseResponse])
def list_clases(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_clases(db, skip=skip, limit=limit)

# Obtener clase por ID
@router.get("/{clase_id}", response_model=ClaseResponse)
def get_clase(clase_id: int, db: Session = Depends(get_db)):
    db_clase = get_clase_by_id(db, clase_id)

    if not db_clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    
    return db_clase

# Actualizar clase por ID
@router.put("/{clase_id}", response_model=ClaseResponse)
def update_clase_by_id(clase_id: int, clase_data: ClaseCreate, db: Session = Depends(get_db)):
    db_clase = update_clase_by_id(db, clase_id, clase_data)

    if not db_clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    
    return db_clase

# Eliminar clase por ID
@router.delete("/{clase_id}", response_model=ClaseResponse)
def delete_clase_by_id(clase_id: int, db: Session = Depends(get_db)):
    db_clase = delete_clase_by_id(db, clase_id)

    if not db_clase:
        raise HTTPException(status_code=404, detail="Clase no encontrada")
    
    return db_clase