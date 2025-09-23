def test_create_clase_api(client):
    payload = {
        "nombre": "DAW 1B",
        "horario": "08:00 - 13:30",
        "profesor_id": 1
    }

    response = client.post("/clases/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == payload["nombre"]
    assert data["horario"] == payload["horario"]
    assert data["profesor_id"] == payload["profesor_id"]

def test_list_clases_api(client):
    response = client.get("/clases/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0