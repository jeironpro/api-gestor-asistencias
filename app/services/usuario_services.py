from sqlalchemy.orm import Session
from app.models.usuarios import Usuario
from app.schemas.usuarios import CrearUsuario, ActualizarUsuario
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_usuarios(db: Session):
    return db.query(Usuario).all()

def obtener_usuario_id(db: Session, id_usuario: str):
    return db.query(Usuario).filter(Usuario.id == id_usuario, Usuario.activo == True).first()

def obtener_usuario_correo_electronico(db: Session, correo_electronico: str):
    return db.query(Usuario).filter(Usuario.correoEletronico == correo_electronico, Usuario.activo == True).first()

def crear_usuario(db: Session, usuario: CrearUsuario):
    hashed_contrasena = pwd_context.hash(usuario.contrasena)
    db_usuario = Usuario(
        nombre = usuario.nombre,
        apellido = usuario.apellido,
        correo_electronico = usuario.correoEletronico,
        contrasena = hashed_contrasena,
        rol = usuario.rol
    )

    db.add()
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def actualizar_usuario_id(db: Session, db_usuario: Usuario, actualizar_usuario: ActualizarUsuario):
    if actualizar_usuario.nombre:
        db_usuario.nombre = actualizar_usuario.nombre
    if actualizar_usuario.apellido:
        db_usuario.apellido = actualizar_usuario.apellido
    if actualizar_usuario.contrasena:
        db_usuario.contrasena = pwd_context.hash(actualizar_usuario.contrasena)
    if actualizar_usuario.rol:
        db_usuario.rol = actualizar_usuario.rol
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def desactivar_usuario(db: Session, db_usuario: Usuario):
    db_usuario.activo = False
    db.commit()
    return db_usuario

def verificar_contrasena(contrasena, hashed_contrasena):
    return pwd_context.verify(contrasena, hashed_contrasena)
