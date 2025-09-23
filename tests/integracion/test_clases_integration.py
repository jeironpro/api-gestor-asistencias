from app.services.profesor_service import create_profesor
from app.services.clase_service import create_clase, get_clases
from app.schemas.clase import ClaseCreate
from app.schemas.profesor import ProfesorCreate

def test_create_and_list_clase(db):
    profesor_data = ProfesorCreate(
        nombre = "Nuria Pujol",
        correo = "nurialpujol@gmail.com",
        especialidad = "Python" 
    )

    profesor = create_profesor(db, profesor_data)

    clase_data = ClaseCreate(
        nombre = "DAW 1B",
        horario = "15:30 - 21:00",
        profesor_id = profesor.id
    )

    clase = create_clase(db, clase_data)

    assert clase.id is not None
    assert clase.nombre == "DAW 1B"

    # Test a la lista de clases
    clases = get_clases(db)
    assert len(clases) == 1
    assert clases[0].profesor_id == profesor.id