# Importaciones
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.connection import obtener_db
from schemas.asistencia import CrearAsistencia, RespuestaAsistencia
from services.asistencia_service import (
    actualizar_asistencia_service,
    crear_asistencia_service,
    eliminar_asistencia_service,
    obtener_asistencia_id_service,
    obtener_asistencia_service,
)

# Rutas de asistencia
router = APIRouter(prefix="/asistencias", tags=["Asistencias"])


# Ruta para crear una asistencia
@router.post("/", response_model=RespuestaAsistencia)
def crear_asistencia(asistencia: CrearAsistencia, db: Session = Depends(obtener_db)):
    return crear_asistencia_service(db, asistencia)


# Ruta para obtener lista de asistencias (con filtros opcionales)
@router.get("/", response_model=List[RespuestaAsistencia])
def lista_asistencias(
    claseId: str | None = None,
    usuarioId: str | None = None,
    db: Session = Depends(obtener_db),
):
    return obtener_asistencia_service(db, id_clase=claseId, id_usuario=usuarioId)


# Ruta para obtener una asistencia por ID
@router.get("/{id_asistencia}", response_model=RespuestaAsistencia)
def obtener_asistencia(id_asistencia: str, db: Session = Depends(obtener_db)):
    return obtener_asistencia_id_service(db, id_asistencia)


# Ruta para actualizar una asistencia
@router.put("/{id_asistencia}", response_model=RespuestaAsistencia)
def actualizar_asistencia(
    id_asistencia: str, asistencia: CrearAsistencia, db: Session = Depends(obtener_db)
):
    return actualizar_asistencia_service(db, id_asistencia, asistencia)


# Ruta para eliminar una asistencia
@router.delete("/{id_asistencia}", status_code=204)
def eliminar_asistencia(id_asistencia: str, db: Session = Depends(obtener_db)):
    eliminar_asistencia_service(db, id_asistencia)
