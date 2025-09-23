import pytest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base
from app.services.asistencia_service import create_asistencia
from app.schemas.asistencia import AsistenciaCreate

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

def test_create_asistencia_service(db):
    asistencia_data = AsistenciaCreate(
        fecha = "2025-09-21",
        estado = "presente",
        estudiante_id = 1,
        clase_id = 1
    )
    nuevo = create_asistencia(db, asistencia_data)

    assert nuevo.id is not None
    assert nuevo.fecha == datetime.date(2025, 9, 21)
    assert nuevo.estado == "presente"
    assert nuevo.estudiante_id == 1
    assert nuevo.clase_id == 1