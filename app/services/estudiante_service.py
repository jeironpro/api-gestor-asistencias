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
from app.models.estudiante import Estudiante
from app.schemas.estudiante import EstudianteCreate

# Crear un estudiante
def create_estudiante(db: Session, estudiante: EstudianteCreate):
    db_estudiante = Estudiante(
        nombre=estudiante.nombre, 
        matricula=estudiante.matricula, 
        curso=estudiante.curso, 
        correo=estudiante.correo
    )
    
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)

    return db_estudiante

# Obtener estudiantes
def get_estudiantes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Estudiante).offset(skip).limit(limit).all()

# Obtener estudiante por ID
def get_estudiante_by_id(db: Session, estudiante_id: int):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()

    if not estudiante:
        return None
    
    return estudiante

# Actualizar estudiante por ID
def update_estudiante_by_id(db: Session, estudiante_id: int, estudiante_data: EstudianteCreate):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()

    if not estudiante:
        return None
    
    estudiante.nombre = estudiante_data.nombre
    estudiante.matricula = estudiante_data.matricula
    estudiante.curso = estudiante_data.curso
    estudiante.correo = estudiante_data.correo

    db.commit()
    db.refresh(estudiante)
    return estudiante

# Eliminar estudiante por ID
def delete_estudiante_by_id(db: Session, estudiante_id: int):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()

    if not estudiante:
        return None
    
    db.delete(estudiante)
    db.commit()
    return estudiante