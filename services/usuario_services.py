# Importaciones
from fastapi import HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from models.Usuario import Usuario
from schemas.usuario import CrearUsuario, ActualizarUsuario
from passlib.context import CryptContext

# Inicialización del contexto de cifrado
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def cifrar_contrasena(password: str) -> str:
    """
        Cifra la contraseña usando Argon2

        Argumentos:
            password: Contraseña a cifrar

        Retorna:
            Contraseña cifrada
    """
    return pwd_context.hash(password)

def verificar_contrasena(contrasena: str, contrasena_cifrada: str) -> bool:
    """
        Verifica si la contraseña coincide con el hash.

        Argumentos:
            contrasena: Contraseña a verificar
            contrasena_cifrada: Contraseña cifrada para verificar

        Retorna:
            True si la contraseña coincide, False en caso contrario
    """
    return pwd_context.verify(contrasena, contrasena_cifrada)

def crear_usuario(db: Session, usuario: CrearUsuario) -> Usuario:
    """
        Crea un nuevo usuario en la base de datos.
        Lanza HTTPException 400 si el correo ya existe.

        Argumentos:
            db: Sesión de base de datos
            usuario: Datos del usuario a crear

        Retorna:
            Usuario creado

        Excepciones:
            HTTPException: Si el correo ya existe
    """
    try:
        contrasena_cifrada = cifrar_contrasena(usuario.contrasena)
        db_usuario = Usuario(
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            correoElectronico=usuario.correoElectronico,
            contrasena=contrasena_cifrada,
            rol=usuario.rol
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )

def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    """
        Obtiene una lista de usuarios con paginación.

        Argumentos:
            db: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a devolver

        Retorna:
            Lista de usuarios
    """
    statement = select(Usuario).offset(skip).limit(limit)
    return db.exec(statement).all()

def obtener_usuario_id(db: Session, id_usuario: str) -> Usuario | None:
    """
        Obtiene un usuario por ID. Retorna None si no existe o no está activo.

        Argumentos:
            db: Sesión de base de datos
            id_usuario: ID del usuario

        Retorna:
            Usuario encontrado
    """
    statement = select(Usuario).where(Usuario.id == id_usuario, Usuario.activo == True)
    return db.exec(statement).first()

def obtener_usuario_correo_electronico(db: Session, correo_electronico: str) -> Usuario | None:
    """
        Obtiene un usuario por correo electrónico.

        Argumentos:
            db: Sesión de base de datos
            correo_electronico: Correo electrónico del usuario

        Retorna:
            Usuario encontrado
    """
    statement = select(Usuario).where(Usuario.correoElectronico == correo_electronico, Usuario.activo == True)
    return db.exec(statement).first()

def actualizar_usuario_id(db: Session, id_usuario: str, actualizar_usuario: ActualizarUsuario) -> Usuario:
    """
        Actualiza un usuario existente.
        Lanza HTTPException 404 si el usuario no existe.

        Argumentos:
            db: Sesión de base de datos
            id_usuario: ID del usuario
            actualizar_usuario: Datos del usuario a actualizar

        Retorna:
            Usuario actualizado

        Excepciones:
            HTTPException: Si el usuario no existe
    """
    db_usuario = obtener_usuario_id(db, id_usuario)
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

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

def desactivar_usuario(db: Session, id_usuario: str) -> Usuario:
    """
        Desactiva (borrado lógico) un usuario.
        Lanza HTTPException 404 si el usuario no existe.

        Argumentos:
            db: Sesión de base de datos
            id_usuario: ID del usuario

        Retorna:
            Usuario desactivado

        Excepciones:
            HTTPException: Si el usuario no existe
    """
    db_usuario = obtener_usuario_id(db, id_usuario)
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    
    db_usuario.activo = False
    db.commit()
    return db_usuario