from fastapi.testclient import TestClient

from api.usuario import obtener_usuario_actual
from main import app
from schemas.asistencia import EstadoAsistencia


def test_obtener_clase_por_id(client: TestClient, clase_test):
    response = client.get(f"/clases/{clase_test.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == clase_test.id
    assert data["nombre"] == clase_test.nombre


def test_actualizar_clase(client: TestClient, clase_test, profesor_test):
    # Sobrescribe la dependencia de usuario actual para que devuelva el profesor
    app.dependency_overrides[obtener_usuario_actual] = lambda: profesor_test
    nuevo_nombre = "DAW 1B"
    payload = {
        "nombre": nuevo_nombre,
        "fecha": str(clase_test.fecha),
        "horaInicio": str(clase_test.horaInicio),
        "horaFin": str(clase_test.horaFin),
    }
    response = client.put(f"/clases/{clase_test.id}", json=payload)
    # Elimina la sobrescritura de la dependencia
    del app.dependency_overrides[obtener_usuario_actual]
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == nuevo_nombre
    assert data["id"] == clase_test.id


def test_eliminar_clase(client: TestClient, clase_test, profesor_test):
    app.dependency_overrides[obtener_usuario_actual] = lambda: profesor_test
    response = client.delete(f"/clases/{clase_test.id}")
    del app.dependency_overrides[obtener_usuario_actual]
    assert response.status_code == 204
    # Verifica que la clase ha sido eliminada
    response = client.get(f"/clases/{clase_test.id}")
    assert response.status_code == 404


def test_obtener_asistencia_por_id(client: TestClient, clase_test, estudiante_test):
    # Crear una asistencia
    payload = {
        "usuarioId": estudiante_test.id,
        "claseId": clase_test.id,
        "estado": EstadoAsistencia.presente,
    }
    response = client.post("/asistencias/", json=payload)
    assert response.status_code == 200
    asistencia_id = response.json()["id"]
    # Obtener por ID
    response = client.get(f"/asistencias/{asistencia_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == asistencia_id
    assert data["usuarioId"] == estudiante_test.id


def test_actualizar_asistencia(client: TestClient, clase_test, estudiante_test):
    # Crear una asistencia
    payload = {
        "usuarioId": estudiante_test.id,
        "claseId": clase_test.id,
        "estado": EstadoAsistencia.presente,
    }
    response = client.post("/asistencias/", json=payload)
    asistencia_id = response.json()["id"]
    # Actualizar una asistencia
    update_payload = {
        "usuarioId": estudiante_test.id,
        "claseId": clase_test.id,
        "estado": EstadoAsistencia.ausente,
    }
    response = client.put(f"/asistencias/{asistencia_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["estado"] == EstadoAsistencia.ausente


def test_eliminar_asistencia(client: TestClient, clase_test, estudiante_test):
    # Crear una asistencia
    payload = {
        "usuarioId": estudiante_test.id,
        "claseId": clase_test.id,
        "estado": EstadoAsistencia.presente,
    }
    response = client.post("/asistencias/", json=payload)
    asistencia_id = response.json()["id"]
    # Eliminar una asistencia
    response = client.delete(f"/asistencias/{asistencia_id}")
    assert response.status_code == 204
    # Verificar que la asistencia ha sido eliminada
    response = client.get(f"/asistencias/{asistencia_id}")
    assert response.status_code == 404


def test_lista_asistencias_filtros(client: TestClient, clase_test, estudiante_test):
    # Crear una asistencia
    payload = {
        "usuarioId": estudiante_test.id,
        "claseId": clase_test.id,
        "estado": EstadoAsistencia.presente,
    }
    client.post("/asistencias/", json=payload)
    # Filtrar por claseId
    response = client.get(f"/asistencias/?claseId={clase_test.id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["claseId"] == clase_test.id
    # Filtrar por usuarioId
    response = client.get(f"/asistencias/?usuarioId={estudiante_test.id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["usuarioId"] == estudiante_test.id
