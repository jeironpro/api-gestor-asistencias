from app.services.estudiante_service import create_estudiante, get_estudiantes
from app.schemas.estudiante import EstudianteCreate

def test_create_and_list_estudiante(db):
    estudiante_data = EstudianteCreate(
        nombre = "Mercedes Roa",
        matricula = "mr-2025",
        curso = "ASIX 1A",
        correo = "mercedesroa@gmail.com",
    )
    estudiante = create_estudiante(db, estudiante_data)

    assert estudiante.id is not None
    assert estudiante.nombre == "Mercedes Roa"

    # Test a la lista de estudiantes
    estudiantes = get_estudiantes(db)
    assert len(estudiantes) == 1
    assert estudiantes[0].matricula == "ASIX 1A"