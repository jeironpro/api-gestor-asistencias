def test_create_estudiante_api(client):
    payload = {
        "nombre": "Jey Junior Cruz",
        "matricula": "2024-jjc",
        "curso": "DAW 2B",
        "correo": "jeyjuniorcruz@gmail.com"
    }

    response = client.post("/estudiantes/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == payload["nombre"]
    assert data["matricula"] == payload["matricula"]
    assert data["curso"] == payload["curso"]
    assert data["correo"] == payload["correo"]

def test_list_estudiantes_api(client):
    response = client.get("/estudiantes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0