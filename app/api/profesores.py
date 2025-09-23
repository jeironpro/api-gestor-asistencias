"""
    APIRouter es una mini-app dentro de FastAPI, que permite organizar rutas de forma modular y escalable.
"""
# Importar el objeto APIRouter que permite organizar y agrupar rutas (endpoints) en la app
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.profesor import ProfesorCreate, ProfesorResponse
from app.services.profesor_service import (create_profesor, get_profesores, get_profesor_by_id, update_profesor_by_id, delete_profesor_by_id)
from app.database.connection import SessionLocal

# Crear el objeto
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