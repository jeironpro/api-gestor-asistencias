import pytest
from datetime import date, time
from services.clase_service import (
    crear_clase_service,
    obtener_clases_service,
    obtener_clase_id_service,
    actualizar_clase_service,
    eliminar_clase_service,
)
from schemas.clase import CrearClase
from fastapi import HTTPException


def test_crear_clase_service(db, profesor_test):
    session = db
    profesor_id = profesor_test.id

    clase_data = CrearClase(
        nombre="DAW 2B",
        fecha=date(2025, 9, 21),
        horaInicio=time(15, 30),
        horaFin=time(21, 0),
    )
    nueva_clase = crear_clase_service(session, clase_data, profesor_id)

    assert nueva_clase.id is not None
    assert nueva_clase.nombre == "DAW 2B"
    assert nueva_clase.horaInicio == time(15, 30)
    assert nueva_clase.horaFin == time(21, 0)
    assert nueva_clase.profesorId == profesor_id


def test_obtener_clases_service(db, profesor_test):
    session = db
    profesor_id = profesor_test.id

    # Crear dos clases
    clase1 = CrearClase(
        nombre="DAW 1A",
        fecha=date(2025, 9, 21),
        horaInicio=time(8, 0),
        horaFin=time(13, 30),
    )
    clase2 = CrearClase(
        nombre="DAW 2B",
        fecha=date(2025, 9, 22),
        horaInicio=time(15, 30),
        horaFin=time(21, 0),
    )

    crear_clase_service(session, clase1, profesor_id)
    crear_clase_service(session, clase2, profesor_id)

    clases = obtener_clases_service(session)
    assert len(clases) == 2
    assert clases[0].nombre == "DAW 1A"
    assert clases[1].nombre == "DAW 2B"


def test_obtener_clases_paginacion(db, profesor_test):
    session = db
    profesor_id = profesor_test.id

    for i in range(5):
        clase = CrearClase(
            nombre=f"Clase {i}",
            fecha=date(2025, 9, 21),
            horaInicio=time(8, 0),
            horaFin=time(13, 30),
        )
        crear_clase_service(session, clase, profesor_id)

    clases = obtener_clases_service(session, skip=0, limit=3)
    assert len(clases) == 3

    clases = obtener_clases_service(session, skip=3, limit=3)
    assert len(clases) == 2


def test_obtener_clase_id_service(db, profesor_test):
    session = db
    profesor_id = profesor_test.id

    clase_data = CrearClase(
        nombre="DAM 1B",
        fecha=date(2025, 9, 21),
        horaInicio=time(8, 0),
        horaFin=time(13, 30),
    )
    nueva_clase = crear_clase_service(session, clase_data, profesor_id)

    clase_encontrada = obtener_clase_id_service(session, nueva_clase.id)
    assert clase_encontrada is not None
    assert clase_encontrada.id == nueva_clase.id
    assert clase_encontrada.nombre == "DAM 1B"


def test_obtener_clase_id_no_existe(db):
    session = db

    with pytest.raises(HTTPException) as exc_info:
        obtener_clase_id_service(session, "id-inexistente")

    assert exc_info.value.status_code == 404
    assert "Clase no encontrada" in exc_info.value.detail


def test_actualizar_clase_service(db, profesor_test):
    session = db
    profesor_id = profesor_test.id

    clase_data = CrearClase(
        nombre="DAW 1A",
        fecha=date(2025, 9, 21),
        horaInicio=time(8, 0),
        horaFin=time(13, 30),
    )
    nueva_clase = crear_clase_service(session, clase_data, profesor_id)

    actualizar_data = CrearClase(
        nombre="DAW 1A - Actualizado",
        fecha=date(2025, 9, 22),
        horaInicio=time(9, 0),
        horaFin=time(14, 0),
    )
    clase_actualizada = actualizar_clase_service(
        session, nueva_clase.id, actualizar_data
    )

    assert clase_actualizada.nombre == "DAW 1A - Actualizado"
    assert clase_actualizada.fecha.date() == date(2025, 9, 22)
    assert clase_actualizada.horaInicio == time(9, 0)


def test_eliminar_clase_service(db, profesor_test):
    session = db
    profesor_id = profesor_test.id

    clase_data = CrearClase(
        nombre="DAW 1A",
        fecha=date(2025, 9, 21),
        horaInicio=time(8, 0),
        horaFin=time(13, 30),
    )
    nueva_clase = crear_clase_service(session, clase_data, profesor_id)

    eliminar_clase_service(session, nueva_clase.id)

    with pytest.raises(HTTPException):
        obtener_clase_id_service(session, nueva_clase.id)
