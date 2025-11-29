# Importaciones
from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from schemas.asistencia import CrearAsistencia, RespuestaAsistencia
from services.asistencia_service import crear_asistencia_service, obtener_asistencias_service, obtener_asistencia_service
from database.connection import obtener_db

# Rutas de asistencia
router = APIRouter(prefix="/asistencias", tags=["Asistencias"])

# Ruta para crear una asistencia
@router.post("/", response_model=RespuestaAsistencia)
def crear_asistencia(asistencia: CrearAsistencia, db: Session = Depends(obtener_db)):
    return crear_asistencia_service(db, asistencia)

# Ruta para obtener lista de asistencias
@router.get("/", response_model=List[RespuestaAsistencia])
def lista_asistencias(db: Session = Depends(obtener_db)):
    return obtener_asistencias_service(db)
