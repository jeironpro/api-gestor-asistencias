def test_create_asistencia_api(client):
    payload = {
        "fecha": "2025-09-21",
        "estado": "ausente",
        "estudiante_id": 2,
        "clase_id": 2
    }

    response = client.post("/asistencias/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["fecha"] == payload["fecha"]
    assert data["estado"] == payload["estado"]
    assert data["estudiante_id"] == payload["estudiante_id"]
    assert data["clase_id"] == payload["clase_id"]

def test_list_profesores_api(client):
    response = client.get("/asistencias/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0