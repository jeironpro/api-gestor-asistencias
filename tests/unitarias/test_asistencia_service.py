import pytest
from fastapi import HTTPException

from models.Asistencia import EstadoAsistencia
from schemas.asistencia import CrearAsistencia
from services.asistencia_service import (
    actualizar_asistencia_service,
    crear_asistencia_service,
    eliminar_asistencia_service,
    obtener_asistencia_id_service,
    obtener_asistencia_service,
    obtener_asistencias_service,
)


def test_crear_asistencia_service(db, estudiante_test, clase_test):
    session = db
    estudiante_id = estudiante_test.id
    clase_id = clase_test.id

    asistencia_data = CrearAsistencia(
        usuarioId=estudiante_id, claseId=clase_id, estado=EstadoAsistencia.presente
    )
    nueva_asistencia = crear_asistencia_service(session, asistencia_data)

    assert nueva_asistencia.id is not None
    assert nueva_asistencia.estado == EstadoAsistencia.presente
    assert nueva_asistencia.usuarioId == estudiante_id
    assert nueva_asistencia.claseId == clase_id


def test_crear_asistencia_usuario_no_existe(db, clase_test):
    session = db
    clase_id = clase_test.id

    asistencia_data = CrearAsistencia(
        usuarioId="id-inexistente", claseId=clase_id, estado=EstadoAsistencia.presente
    )

    with pytest.raises(HTTPException) as exc_info:
        crear_asistencia_service(session, asistencia_data)

    assert exc_info.value.status_code == 404
    assert "Usuario no encontrado" in exc_info.value.detail


def test_crear_asistencia_clase_no_existe(db, estudiante_test):
    session = db
    estudiante_id = estudiante_test.id

    asistencia_data = CrearAsistencia(
        usuarioId=estudiante_id,
        claseId="id-inexistente",
        estado=EstadoAsistencia.presente,
    )

    with pytest.raises(HTTPException) as exc_info:
        crear_asistencia_service(session, asistencia_data)

    assert exc_info.value.status_code == 404
    assert "Clase no encontrada" in exc_info.value.detail


def test_obtener_asistencias_service(db, estudiante_test, clase_test):
    session = db
    estudiante_id = estudiante_test.id
    clase_id = clase_test.id

    asistencia1 = CrearAsistencia(
        usuarioId=estudiante_id, claseId=clase_id, estado=EstadoAsistencia.presente
    )
    asistencia2 = CrearAsistencia(
        usuarioId=estudiante_id, claseId=clase_id, estado=EstadoAsistencia.ausente
    )

    crear_asistencia_service(session, asistencia1)
    crear_asistencia_service(session, asistencia2)

    asistencias = obtener_asistencias_service(session)
    assert len(asistencias) == 2


def test_obtener_asistencias_paginacion(db, estudiante_test, clase_test):
    session = db
    estudiante_id = estudiante_test.id
    clase_id = clase_test.id

    for i in range(5):
        asistencia = CrearAsistencia(
            usuarioId=estudiante_id, claseId=clase_id, estado=EstadoAsistencia.presente
        )
        crear_asistencia_service(session, asistencia)

    asistencias = obtener_asistencias_service(session, skip=0, limit=3)
    assert len(asistencias) == 3

    asistencias = obtener_asistencias_service(session, skip=3, limit=3)
    assert len(asistencias) == 2


def test_obtener_asistencia_filtro_clase(db, estudiante_test, clase_test):
    session = db
    estudiante_id = estudiante_test.id
    clase_id = clase_test.id

    asistencia = CrearAsistencia(
        usuarioId=estudiante_id, claseId=clase_id, estado=EstadoAsistencia.presente
    )
    crear_asistencia_service(session, asistencia)

    asistencias = obtener_asistencia_service(session, id_clase=clase_id)
    assert len(asistencias) == 1
    assert asistencias[0].claseId == clase_id


def test_obtener_asistencia_filtro_usuario(db, estudiante_test, clase_test):
    session = db
    estudiante_id = estudiante_test.id
    clase_id = clase_test.id

    asistencia = CrearAsistencia(
        usuarioId=estudiante_id, claseId=clase_id, estado=EstadoAsistencia.presente
    )
    crear_asistencia_service(session, asistencia)

    asistencias = obtener_asistencia_service(session, id_usuario=estudiante_id)
    assert len(asistencias) == 1
    assert asistencias[0].usuarioId == estudiante_id


def test_obtener_asistencia_id_service(db, estudiante_test, clase_test):
    session = db
    estudiante_id = estudiante_test.id
    clase_id = clase_test.id

    asistencia_data = CrearAsistencia(
        usuarioId=estudiante_id, claseId=clase_id, estado=EstadoAsistencia.presente
    )
    nueva_asistencia = crear_asistencia_service(session, asistencia_data)

    asistencia_encontrada = obtener_asistencia_id_service(session, nueva_asistencia.id)
    assert asistencia_encontrada is not None
    assert asistencia_encontrada.id == nueva_asistencia.id


def test_obtener_asistencia_id_no_existe(db):
    session = db

    with pytest.raises(HTTPException) as exc_info:
        obtener_asistencia_id_service(session, "id-inexistente")

    assert exc_info.value.status_code == 404


def test_actualizar_asistencia_service(db, estudiante_test, clase_test):
    session = db
    estudiante_id = estudiante_test.id
    clase_id = clase_test.id

    asistencia_data = CrearAsistencia(
        usuarioId=estudiante_id, claseId=clase_id, estado=EstadoAsistencia.presente
    )
    nueva_asistencia = crear_asistencia_service(session, asistencia_data)

    actualizar_data = CrearAsistencia(
        usuarioId=estudiante_id, claseId=clase_id, estado=EstadoAsistencia.retraso
    )
    asistencia_actualizada = actualizar_asistencia_service(
        session, nueva_asistencia.id, actualizar_data
    )

    assert asistencia_actualizada.estado == EstadoAsistencia.retraso


def test_eliminar_asistencia_service(db, estudiante_test, clase_test):
    session = db
    estudiante_id = estudiante_test.id
    clase_id = clase_test.id

    asistencia_data = CrearAsistencia(
        usuarioId=estudiante_id, claseId=clase_id, estado=EstadoAsistencia.presente
    )
    nueva_asistencia = crear_asistencia_service(session, asistencia_data)

    eliminar_asistencia_service(session, nueva_asistencia.id)

    with pytest.raises(HTTPException):
        obtener_asistencia_id_service(session, nueva_asistencia.id)
