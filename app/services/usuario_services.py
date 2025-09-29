from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.usuarios import CrearUsuario, ActualizarUsuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def cifrar_contrasena(password: str) -> str:
    return pwd_context.hash(password)

def crear_usuario(db: Session, usuario: CrearUsuario):
    contrasena_cifrada = cifrar_contrasena(usuario.contrasena)
    db_usuario = Usuario(
        nombre = usuario.nombre,
        apellido = usuario.apellido,
        correoElectronico = usuario.correoElectronico,
        contrasena = contrasena_cifrada,
        rol = usuario.rol
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuarios(db: Session):
    return db.query(Usuario).all()

def obtener_usuario_id(db: Session, id_usuario: str):
    return db.query(Usuario).filter(Usuario.id == id_usuario, Usuario.activo == True).first()

def obtener_usuario_correo_electronico(db: Session, correo_electronico: str):
    return db.query(Usuario).filter(Usuario.correoElectronico == correo_electronico, Usuario.activo == True).first()

def actualizar_usuario_id(db: Session, db_usuario: Usuario, actualizar_usuario: ActualizarUsuario):
    if actualizar_usuario.nombre:
        db_usuario.nombre = actualizar_usuario.nombre
    if actualizar_usuario.apellido:
        db_usuario.apellido = actualizar_usuario.apellido
    if actualizar_usuario.contrasena:
        db_usuario.contrasena = cifrar_contrasena(actualizar_usuario.contrasena)
    if actualizar_usuario.rol:
        db_usuario.rol = actualizar_usuario.rol
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def desactivar_usuario(db: Session, db_usuario: Usuario):
    db_usuario.activo = False
    db.commit()
    return db_usuario

def verificar_contrasena(contrasena: str, contrasena_cifrada: str) -> bool:
    return pwd_context.verify(contrasena, contrasena_cifrada)