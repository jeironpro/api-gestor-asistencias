"""
    APIRouter: sirve para organizar rutas de manera modular. Permite separar los endpoints en módulos independientes y facilita agregar prefijos, tags y dependencias comunes a grupos de rutas.
    
    Depends: Sirve para inyectar dependencias en los endpoints. Permite reutilizar funciones que proporcionan servicios, autenticación, sesiones de base de datos, etc. FastAPI las llama automáticamente y pasa el resultado al endpoint. 
    
    HTTPException: Sirve para devolver errores HTTP con código y detalle. Detiene la ejecución del endpoint y envía una respuesta HTTP con el código de error.
    
    List: es un tipo genérico que se usa para anotar listas con tipos específicos de elementos. 
    
    · Se puede usar List[str] directamente.
    · Se usa para tipado estático, validación y autocompletado.
    · Muy común en pydantic y FastAPI para definir campos que son listas de valores.

    · List[int]: lista de enteros.
    · List[str]: lista de cadenas de texto.
    · List[float]: lista de números flotantes.
"""
import jwt
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from jwt import PyJWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.usuarios import RolUsuario, Usuario
from app.schemas.usuarios import RolUsuario, CrearUsuario, ActualizarUsuario, RespuestaUsuario, Token
from app.services.usuario_services import obtener_usuarios, obtener_usuario_id, obtener_usuario_correo_electronico, crear_usuario, actualizar_usuario_id, desactivar_usuario, verificar_contrasena
from app.database.connection import obtener_db

CLAVE_SECRETA = secrets.token_hex(32) # 32 carácteres hexadecimales

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

def crear_token_acceso(datos: dict, delta_expira: timedelta | None = None):
    codifica = datos.copy()
    expira = datetime.utcnow() + (delta_expira if delta_expira else timedelta(minutes=15))
    codifica.update({"exp": expira})

    return jwt.encode(codifica, CLAVE_SECRETA, algorithm="HS256")

def obtener_usuario_actual(db: Session = Depends(obtener_db), token: str = Depends(OAuth2PasswordBearer(tokenUrl="usuarios/inicio_sesion"))):
    print(token)
    try:
        datos = jwt.decode(token, CLAVE_SECRETA, algorithms="HS256")
        id_usuario: str = datos.get("sub")

        if id_usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido...")
    
    usuario = obtener_usuario_id(db, id_usuario)

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    
    return usuario

def requerir_rol(rol: RolUsuario):
    def verificar_rol(usuario: Usuario = Depends(obtener_usuario_actual)):
        print(usuario.rol)
        print(rol)
        if usuario.rol != rol:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permiso denegado")
        return usuario
    return verificar_rol

@router.post("/", response_model=RespuestaUsuario)
def crear_usaurio(usuario: CrearUsuario, db: Session = Depends(obtener_db)):
    if obtener_usuario_correo_electronico(db, usuario.correoElectronico):
        raise HTTPException(status_code=400, detail="EL correo electrónico ya esta registrado")
    return crear_usuario(db, usuario)

@router.get("/", response_model=List[RespuestaUsuario])
def lista_usuarios(db: Session = Depends(obtener_db), admin: Usuario = Depends(requerir_rol(RolUsuario.admin))):
    return obtener_usuarios(db)

@router.put("/{id_usuario}", response_model=RespuestaUsuario)
def actualizar_usuario(id_usuario: str, actualizar_usuario: ActualizarUsuario, db: Session = Depends(obtener_db), usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    db_usuario = obtener_usuario_id(db, id_usuario)
    
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if usuario_actual.rol != RolUsuario.admin and usuario_actual.id != id_usuario:
        raise HTTPException(status_code=403, detail="Permiso denegado")
    return actualizar_usuario_id(db, id_usuario, actualizar_usuario)

@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: str, db: Session = Depends(obtener_db)):
    db_usuario = obtener_usuario_id(db, id_usuario)

    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    desactivar_usuario(db, db_usuario)
    return {"detalle": "Usuario desactivado"}

@router.post("/inicio_sesion", response_model=Token)
def inicio_sesion(datos_formulario: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(obtener_db)):
    usuario = obtener_usuario_correo_electronico(db, datos_formulario.username)

    if not usuario or not verificar_contrasena(datos_formulario.password, usuario.contrasena):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    token_acceso = crear_token_acceso({"sub": usuario.id}, timedelta(minutes=60))
    return {"access_token": token_acceso, "token_type": "bearer"}

@router.get("/me", response_model=RespuestaUsuario)
def me(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    return usuario_actual