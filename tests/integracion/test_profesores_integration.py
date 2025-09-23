from app.services.profesor_service import create_profesor, get_profesores
from app.schemas.profesor import ProfesorCreate

def test_create_and_list_profesor(db):
    profesor_data = ProfesorCreate(
        nombre = "Josep Oriol",
        correo = "joseporiol@gmail.com",
        especialidad = "Diseño de aplicaciones web"
    )

    profesor = create_profesor(db, profesor_data)
    assert profesor.id is not None
    assert profesor.nombre == "Josep Oriol"

    # Test a lista de profesores
    profesores = get_profesores(db)
    assert len(profesores) == 1
    assert profesores[0].correo == "joseporiol@gmail.com"
