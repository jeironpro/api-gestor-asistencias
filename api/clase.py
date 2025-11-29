# Importaciones
from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from models.Usuario import Usuario, RolUsuario
from api.usuario import requerir_rol
from schemas.clase import CrearClase, RespuestaClase
from services.clase_service import crear_clase_service, obtener_clases_service
from database.connection import obtener_db

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
