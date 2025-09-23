import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base
from app.services.estudiante_service import create_estudiante
from app.schemas.estudiante import EstudianteCreate

# Base de datos en memoria (only for test)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

Base.metadata.drop_all(bind=engine)

def test_create_estudiante_service(db):
    estudiante_data = EstudianteCreate(
        nombre = "Jeiron Espinal",
        matricula = "2024-jjec",
        curso = "DAW",
        correo = "jeironespinal@gmail.com"
    )
    nuevo = create_estudiante(db, estudiante_data)

    assert nuevo.id is not None
    assert nuevo.nombre == "Jeiron Espinal"
    assert nuevo.matricula == "2024-jjec"
    assert nuevo.curso == "DAW"
    assert nuevo.correo == "jeironespinal@gmail.com"