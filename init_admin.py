from sqlalchemy.orm import Session
from models.usuarios import Usuario
from services.usuario_services import cifrar_contrasena

def crear_admin(db: Session):
    admin = db.query(Usuario).filter(Usuario.rol == "admin").first()

    if not admin:
        usuario_admin = Usuario(
            nombre="jeiron",
            apellido="espinal",
            correoElectronico="jeironprogrammer@gmail.com",
            contrasena=cifrar_contrasena("jeironpro2303"),
            rol="admin"
        )
        db.add(usuario_admin)
        db.commit()
    else:
        return None