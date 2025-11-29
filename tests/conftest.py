# Importaciones
import uuid
from datetime import date, time

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from database.connection import obtener_db
from main import app
from models.Usuario import RolUsuario, Usuario
from schemas.clase import CrearClase
from services.clase_service import crear_clase_service

# Base de datos de pruebas
TEST_DATABASE_URL = "sqlite:///:memory:"

# Crear la base de datos de pruebas
engine_test = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear la base de datos de pruebas
SQLModel.metadata.create_all(bind=engine_test)


def obtener_test_session():
    # Obtiene una sesión de la base de datos de pruebas.
    with Session(engine_test) as session:
        yield session


app.dependency_overrides[obtener_db] = obtener_test_session


@pytest.fixture(scope="function")
def db():
    # Devuelve una sesión del engine_test de test
    with Session(engine_test) as session:
        yield session
        session.rollback()


@pytest.fixture(scope="function")
def client():
    # Devuelve un cliente de prueba
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def profesor_test(db):
    # Crear un profesor de prueba
    profesor = Usuario(
        id=str(uuid.uuid4()),
        nombre="Test",
        apellido="Profesor",
        correoElectronico="profesor@test.com",
        contrasena="hashed_password",
        rol=RolUsuario.profesor,
    )
    db.add(profesor)
    db.commit()
    db.refresh(profesor)

    return profesor


@pytest.fixture(scope="function")
def estudiante_test(db):
    # Crear un estudiante y profesor de prueba
    estudiante = Usuario(
        id=str(uuid.uuid4()),
        nombre="Test",
        apellido="Estudiante",
        correoElectronico="estudiante@test.com",
        contrasena="hashed_password",
        rol=RolUsuario.estudiante,
    )

    db.add(estudiante)
    db.commit()
    db.refresh(estudiante)

    return estudiante


@pytest.fixture(scope="function")
def clase_test(db, profesor_test):
    # Crear una clase de prueba
    clase_data = CrearClase(
        nombre="DAW 1A",
        fecha=date(2025, 9, 21),
        horaInicio=time(8, 0),
        horaFin=time(13, 30),
    )

    return crear_clase_service(db, clase_data, profesor_test.id)
