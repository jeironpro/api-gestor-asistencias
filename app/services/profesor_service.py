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
from app.models.profesor import Profesor
from app.schemas.profesor import ProfesorCreate

# Crear un profesor
def create_profesor(db: Session, profesor: ProfesorCreate):
    db_profesor = Profesor(
        nombre=profesor.nombre, 
        especialidad=profesor.especialidad,
        correo=profesor.correo
    )

    db.add(db_profesor)
    db.commit()
    db.refresh(db_profesor)

    return db_profesor

# Obtener profesores
def get_profesores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Profesor).offset(skip).limit(limit).all()

# Obtener profesor por ID
def get_profesor_by_id(db: Session, profesor_id: int):
    profesor = db.query(Profesor).filter(Profesor.id == profesor_id).first()

    if not profesor:
        return None
    
    return profesor

# Actualizar profesor por ID
def update_profesor_by_id(db: Session, profesor_id: int, profesor_data: ProfesorCreate):
    profesor = db.query(Profesor).filter(Profesor.id == profesor_id).first()

    if not profesor:
        return None
    
    profesor.nombre = profesor_data.nombre
    profesor.especialidad = profesor_data.especialidad
    profesor.correo = profesor_data.correo

    db.commit()
    db.refresh(profesor)
    return profesor

# Eliminar profesor por ID
def delete_profesor_by_id(db: Session, profesor_id: int):
    profesor = db.query(Profesor).filter(Profesor.id == profesor_id).first()

    if not profesor:
        return None
    
    db.delete(profesor)
    db.commit()
    return profesor