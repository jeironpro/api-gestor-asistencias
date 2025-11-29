# Importaciones
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from models.Clase import Clase
from schemas.clase import CrearClase


def crear_clase_service(db: Session, clase: CrearClase, profesorId: str) -> Clase:
    """
    Crea una nueva clase en la base de datos.

    Argumentos:
        db: Sesión de base de datos
        clase: Datos de la clase a crear
        profesorId: ID del profesor que imparte la clase

    Retorna:
        Clase creada

    Excepciones:
        HTTPException: Si el profesor no existe
    """
    try:
        db_clase = Clase(
            nombre=clase.nombre,
            fecha=clase.fecha,
            horaInicio=clase.horaInicio,
            horaFin=clase.horaFin,
            profesorId=profesorId,
        )

        db.add(db_clase)
        db.commit()
        db.refresh(db_clase)

        return db_clase

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al crear la clase. Verifica que el profesor existe.",
        )


def obtener_clases_service(db: Session, skip: int = 0, limit: int = 100) -> list[Clase]:
    """
    Obtiene una lista de clases con paginación.

    Argumentos:
        db: Sesión de base de datos
        skip: Número de registros a saltar
        limit: Número máximo de registros a devolver

    Retorna:
        Lista de clases
    """
    statement = select(Clase).offset(skip).limit(limit)
    return db.exec(statement).all()


def obtener_clase_id_service(db: Session, id_clase: str) -> Clase:
    """
    Obtiene una clase por su ID.
    Lanza HTTPException 404 si no existe.

    Argumentos:
        db: Sesión de base de datos
        id_clase: ID de la clase

    Retorna:
        Clase encontrada

    Excepciones:
        HTTPException: Si la clase no existe
    """
    statement = select(Clase).where(Clase.id == id_clase)
    clase = db.exec(statement).first()

    if not clase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Clase no encontrada"
        )

    return clase


def actualizar_clase_service(
    db: Session, id_clase: str, clase_data: CrearClase
) -> Clase:
    """
    Actualiza una clase existente.

    Argumentos:
        db: Sesión de base de datos
        id_clase: ID de la clase a actualizar
        clase_data: Nuevos datos de la clase

    Retorna:
        Clase actualizada
    """
    db_clase = obtener_clase_id_service(db, id_clase)

    db_clase.nombre = clase_data.nombre
    db_clase.fecha = clase_data.fecha
    db_clase.horaInicio = clase_data.horaInicio
    db_clase.horaFin = clase_data.horaFin

    db.commit()
    db.refresh(db_clase)
    return db_clase


def eliminar_clase_service(db: Session, id_clase: str) -> Clase:
    """
    Elimina una clase de la base de datos.

    Argumentos:
        db: Sesión de base de datos
        id_clase: ID de la clase a eliminar

    Retorna:
        Clase eliminada
    """
    db_clase = obtener_clase_id_service(db, id_clase)
    db.delete(db_clase)
    db.commit()
    return db_clase
