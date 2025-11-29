# Importaciones
from fastapi import HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from models.Asistencia import Asistencia
from models.Usuario import Usuario
from models.Clase import Clase
from schemas.asistencia import CrearAsistencia
from typing import Optional


def crear_asistencia_service(db: Session, asistencia: CrearAsistencia) -> Asistencia:
    """
    Crea una nueva asistencia en la base de datos.
    Valida que el usuario y la clase existan.

    Argumentos:
        db: Sesión de base de datos
        asistencia: Datos de la asistencia a crear

    Retorna:
        Asistencia creada

    Excepciones:
        HTTPException: Si el usuario o clase no existen
    """
    usuario = db.exec(select(Usuario).where(Usuario.id == asistencia.usuarioId)).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )

    clase = db.exec(select(Clase).where(Clase.id == asistencia.claseId)).first()

    if not clase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Clase no encontrada"
        )

    try:
        db_asistencia = Asistencia(
            usuarioId=asistencia.usuarioId,
            claseId=asistencia.claseId,
            estado=asistencia.estado,
        )

        db.add(db_asistencia)
        db.commit()
        db.refresh(db_asistencia)

        return db_asistencia

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear la asistencia",
        )


def obtener_asistencias_service(
    db: Session, skip: int = 0, limit: int = 100
) -> list[Asistencia]:
    """
    Obtiene una lista de asistencias con paginación.

    Argumentos:
        db: Sesión de base de datos
        skip: Número de registros a saltar
        limit: Número máximo de registros a devolver

    Retorna:
        Lista de asistencias
    """
    statement = select(Asistencia).offset(skip).limit(limit)
    return db.exec(statement).all()


def obtener_asistencia_service(
    db: Session,
    id_clase: Optional[str] = None,
    id_usuario: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> list[Asistencia]:
    """
    Obtiene asistencias filtradas por clase y/o usuario con paginación.

    Argumentos:
        db: Sesión de base de datos
        id_clase: ID de la clase (opcional)
        id_usuario: ID del usuario (opcional)
        skip: Número de registros a saltar
        limit: Número máximo de registros a devolver

    Retorna:
        Lista de asistencias filtradas
    """
    statement = select(Asistencia)

    if id_clase:
        statement = statement.where(Asistencia.claseId == id_clase)

    if id_usuario:
        statement = statement.where(Asistencia.usuarioId == id_usuario)

    statement = statement.offset(skip).limit(limit)
    return db.exec(statement).all()


def obtener_asistencia_id_service(db: Session, id_asistencia: str) -> Asistencia:
    """
    Obtiene una asistencia por su ID.

    Argumentos:
        db: Sesión de base de datos
        id_asistencia: ID de la asistencia

    Retorna:
        Asistencia encontrada

    Excepciones:
        HTTPException: Si la asistencia no existe
    """
    statement = select(Asistencia).where(Asistencia.id == id_asistencia)
    asistencia = db.exec(statement).first()

    if not asistencia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Asistencia no encontrada"
        )

    return asistencia


def actualizar_asistencia_service(
    db: Session, id_asistencia: str, asistencia_data: CrearAsistencia
) -> Asistencia:
    """
    Actualiza una asistencia existente.

    Argumentos:
        db: Sesión de base de datos
        id_asistencia: ID de la asistencia a actualizar
        asistencia_data: Nuevos datos de la asistencia

    Retorna:
        Asistencia actualizada

    Excepciones:
        HTTPException: Si la asistencia no existe
    """
    db_asistencia = obtener_asistencia_id_service(db, id_asistencia)

    db_asistencia.estado = asistencia_data.estado

    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia


def eliminar_asistencia_service(db: Session, id_asistencia: str) -> None:
    """
    Elimina una asistencia de la base de datos.

    Argumentos:
        db: Sesión de base de datos
        id_asistencia: ID de la asistencia a eliminar
    """
    db_asistencia = obtener_asistencia_id_service(db, id_asistencia)
    db.delete(db_asistencia)
    db.commit()
