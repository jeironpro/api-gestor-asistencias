# Importaciones
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.usuario import requerir_rol
from database.connection import obtener_db
from models.Usuario import RolUsuario, Usuario
from schemas.clase import CrearClase, RespuestaClase
from services.clase_service import (
    actualizar_clase_service,
    crear_clase_service,
    eliminar_clase_service,
    obtener_clase_id_service,
    obtener_clases_service,
)

# Rutas de clase
router = APIRouter(prefix="/clases", tags=["clases"])


# Ruta para crear una clase
@router.post("/", response_model=RespuestaClase)
def crear_clase(
    clase: CrearClase,
    db: Session = Depends(obtener_db),
    profesor: Usuario = Depends(requerir_rol(RolUsuario.profesor)),
):
    return crear_clase_service(db, clase, profesor.id)


# Ruta para obtener lista de clases
@router.get("/", response_model=List[RespuestaClase])
def lista_clases(db: Session = Depends(obtener_db)):
    return obtener_clases_service(db)


# Ruta para obtener una clase por ID
@router.get("/{id_clase}", response_model=RespuestaClase)
def obtener_clase(id_clase: str, db: Session = Depends(obtener_db)):
    return obtener_clase_id_service(db, id_clase)


# Ruta para actualizar una clase
@router.put("/{id_clase}", response_model=RespuestaClase)
def actualizar_clase(
    id_clase: str,
    clase: CrearClase,
    db: Session = Depends(obtener_db),
    profesor: Usuario = Depends(requerir_rol(RolUsuario.profesor)),
):
    return actualizar_clase_service(db, id_clase, clase)


# Ruta para eliminar una clase
@router.delete("/{id_clase}", status_code=204)
def eliminar_clase(
    id_clase: str,
    db: Session = Depends(obtener_db),
    profesor: Usuario = Depends(requerir_rol(RolUsuario.profesor)),
):
    eliminar_clase_service(db, id_clase)
