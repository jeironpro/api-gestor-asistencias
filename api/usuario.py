# Importaciones
import secrets
from datetime import datetime, timedelta
from typing import List

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from database.connection import obtener_db
from models.Usuario import RolUsuario, Usuario
from schemas.usuario import ActualizarUsuario, CrearUsuario, RespuestaUsuario, Token
from services.usuario_services import (
    actualizar_usuario_id,
    crear_usuario,
    desactivar_usuario,
    obtener_usuario_correo_electronico,
    obtener_usuario_id,
    obtener_usuarios,
    verificar_contrasena,
)

CLAVE_SECRETA = secrets.token_hex(32)  # 32 carácteres hexadecimales

# Rutas de usuario
router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def crear_token_acceso(datos: dict, delta_expira: timedelta | None = None):
    """
    Crea un token de acceso.

    Argumentos:
        datos: Datos a codificar
        delta_expira: Tiempo de expiración del token

    Retorna:
        Token de acceso
    """
    codifica = datos.copy()
    expira = datetime.utcnow() + (
        delta_expira if delta_expira else timedelta(minutes=15)
    )
    codifica.update({"exp": expira})

    return jwt.encode(codifica, CLAVE_SECRETA, algorithm="HS256")


def obtener_usuario_actual(
    db: Session = Depends(obtener_db),
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="usuarios/inicio_sesion")),
):
    """
    Obtiene el usuario actual.

    Argumentos:
        db: Sesión de base de datos
        token: Token de acceso

    Retorna:
        Usuario actual

    Excepciones:
        HTTPException: Si el token es inválido
    """
    try:
        datos = jwt.decode(token, CLAVE_SECRETA, algorithms="HS256")
        id_usuario: str = datos.get("sub")

        if id_usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido...")

    usuario = obtener_usuario_id(db, id_usuario)

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    return usuario


def requerir_rol(rol: RolUsuario):
    """
    Requiere un rol específico.

    Argumentos:
        rol: Rol requerido

    Retorna:
        Decorador que verifica el rol

    Excepciones:
        HTTPException: Si el usuario no tiene el rol requerido
    """

    def verificar_rol(usuario: Usuario = Depends(obtener_usuario_actual)):
        if usuario.rol != rol:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado"
            )
        return usuario

    return verificar_rol


# Ruta para crear un usuario
@router.post("/", response_model=RespuestaUsuario)
def crear_usuario_endpoint(usuario: CrearUsuario, db: Session = Depends(obtener_db)):
    return crear_usuario(db, usuario)


# Ruta para obtener lista de usuarios
@router.get("/", response_model=List[RespuestaUsuario])
def lista_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(obtener_db),
    admin: Usuario = Depends(requerir_rol(RolUsuario.admin)),
):
    return obtener_usuarios(db, skip=skip, limit=limit)


# Ruta para actualizar un usuario
@router.put("/{id_usuario}", response_model=RespuestaUsuario)
def actualizar_usuario(
    id_usuario: str,
    actualizar_usuario: ActualizarUsuario,
    db: Session = Depends(obtener_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
):
    if usuario_actual.rol != RolUsuario.admin and usuario_actual.id != id_usuario:
        raise HTTPException(status_code=403, detail="Permiso denegado")
    return actualizar_usuario_id(db, id_usuario, actualizar_usuario)


# Ruta para eliminar un usuario
@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: str, db: Session = Depends(obtener_db)):
    desactivar_usuario(db, id_usuario)
    return {"detalle": "Usuario desactivado"}


# Ruta para iniciar sesión
@router.post("/inicio_sesion", response_model=Token)
def inicio_sesion(
    datos_formulario: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(obtener_db),
):
    usuario = obtener_usuario_correo_electronico(db, datos_formulario.username)

    if not usuario or not verificar_contrasena(
        datos_formulario.password, usuario.contrasena
    ):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    token_acceso = crear_token_acceso({"sub": usuario.id}, timedelta(minutes=60))
    return {"access_token": token_acceso, "token_type": "bearer"}


# Ruta para obtener el usuario actual
@router.get("/me", response_model=RespuestaUsuario)
def me(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return usuario_actual
