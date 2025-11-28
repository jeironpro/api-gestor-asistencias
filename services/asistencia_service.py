"""
    Session: es el objeto que maneja todas las operaciones sobre la base de datos usando ORM. Es el intermediario entre tus modelos (clases Python) y la base de datos.

    A través de una sesión puedes:
    · Insertar registros (add, add_all)
    · Consultar registros (query)
    · Actualizar registros
    · Eliminar registros
    · Confirmar cambios con commit()
    · Revertir cambios con rollback()
"""
from sqlalchemy.orm import Session
from models.asistencias import Asistencia
from schemas.asistencias import CrearAsistencia
from typing import Optional

# Crear asistencia
def crear_asistencia_service(db: Session, asistencia: CrearAsistencia):
    db_asistencia = Asistencia(
        usuarioId=asistencia.usuarioId,
        claseId=asistencia.claseId,
        estado=asistencia.estado
    )

    db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia

def obtener_asistencias_service(db: Session):
    return db.query(Asistencia).all()

# Obtener asistencias dependiendo si es por la clase o por el usuario
def obtener_asistencia_service(db: Session, id_clase: Optional[str] = None, id_usuario: Optional[str] = None):
    asistencia =  db.query(Asistencia)

    if id_clase:
        asistencia = asistencia.filter(Asistencia.claseId == id_clase)

    if id_usuario:
        asistencia = asistencia.filter(Asistencia.usuarioId == id_usuario)

    return asistencia.all()