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
from models.clases import Clase
from schemas.clases import CrearClase

# Crear clase
def crear_clase_service(db: Session, clase: CrearClase, profesorId: str):
    db_clase = Clase(
        nombre=clase.nombre,
        fecha=clase.fecha,
        horaInicio=clase.horaInicio,
        horaFin=clase.horaFin,
        profesorId=profesorId
    )

    db.add(db_clase)
    db.commit()
    db.refresh(db_clase)
    return db_clase

# Obtener clase
def obtener_clases_service(db: Session):
    return db.query(Clase).all()

# Obtener clase por ID
def obtener_clase_id_service(db: Session, id_clase: str):
    return db.query(Clase).filter(Clase.id == id_clase).first()