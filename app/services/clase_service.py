from sqlalchemy.orm import Session
from app.models.clase import Clase
from app.schemas.clase import ClaseCreate

# Crear clase
def create_clase(db: Session, clase: ClaseCreate):
    db_clase = Clase(
        nombre=clase.nombre, 
        profesor_id=clase.profesor_id,
        horario=clase.horario
    )

    db.add(db_clase)
    db.commit()
    db.refresh(db_clase)

    return db_clase

# Obtener clase
def get_clases(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Clase).offset(skip).limit(limit).all()

# Obtener clase por ID
def get_clase_by_id(db: Session, clase_id: int):
    clase = db.query(Clase).filter(Clase.id == clase_id).first()

    if not clase:
        return None
    
    return clase

# Actualizar clase por ID
def update_clase_by_id(db: Session, clase_id: int, clase_data: ClaseCreate):
    clase = db.query(Clase).filter(Clase.id == clase_id).first()

    if not clase:
        return None
    
    clase.nombre = clase_data.nombre
    clase.profesor_id = clase_data.profesor_id
    clase.horario = clase_data.horario

    db.commit()
    db.refresh(clase)
    return clase

# Eliminar clase por ID
def delete_clase_by_id(db: Session, clase_id: int):
    clase = db.query(Clase).filter(Clase.id == clase_id).first()

    if not clase:
        return None
    
    db.delete(clase)
    db.commit()
    return clase