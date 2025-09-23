def test_create_profesor_api(client):
    payload = {
        "nombre": "Moises Giron",
        "correo": "moisesgiron@gmail.com",
        "especialidad": "Programacion"
    }

    response = client.post("/profesores/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == payload["nombre"]
    assert data["correo"] == payload["correo"]
    assert data["especialidad"] == payload["especialidad"]

def test_list_profesores_api(client):
    response = client.get("/profesores/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0