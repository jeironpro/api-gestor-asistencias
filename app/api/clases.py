"""
    APIRouter es una mini-app dentro de FastAPI, que permite organizar rutas de forma modular y escalable.
"""
# Importar el objeto APIRouter que permite organizar y agrupar rutas (endpoints) en la app
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.clase import ClaseCreate, ClaseResponse
from app.services.clase_service import (create_clase, get_clases, get_clase_by_id, update_clase_by_id, delete_clase_by_id)
from app.database.connection import SessionLocal

# Crear el objeto
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