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
from app.models.asistencia import Asistencia
from app.schemas.asistencia import AsistenciaCreate

# Crear asistencia
def create_asistencia(db: Session, asistencia: AsistenciaCreate):
    db_asistencia = Asistencia(
        fecha=asistencia.fecha, 
        estudiante_id=asistencia.estudiante_id,
        clase_id=asistencia.clase_id,
        estado=asistencia.estado
    )

    db.add(db_asistencia)
    db.commit()
    db.refresh(db_asistencia)
    return db_asistencia

# Listar asistencias
def get_asistencias(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Asistencia).offset(skip).limit(limit).all()

# Buscar asistencia por ID
def get_asistencia_by_id(db: Session, asistencia_id: int):
    asistencia =  db.query(Asistencia).filter(Asistencia.id == asistencia_id).first() 

    if not asistencia:
        return None
    
    return asistencia

# Actualizar asistencia por ID
def update_asistencia_by_id(db: Session, asistencia_id: int, asistencia_data: AsistenciaCreate):
    asistencia = db.query(Asistencia).filter(Asistencia.id == asistencia_id).first()

    if not asistencia:
        return None
    
    asistencia.estado = asistencia_data.estado
    
    db.commit()
    db.refresh(asistencia)
    return asistencia

# Eliminar asistencia por ID
def delete_asistencia_by_id(db: Session, asistencia_id):
    asistencia = db.query(Asistencia).filter(Asistencia.id == asistencia_id).first()

    if not asistencia:
        return None
    
    db.delete(asistencia)
    db.commit()
    return asistencia