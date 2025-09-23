import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base
from app.services.profesor_service import create_profesor
from app.schemas.profesor import ProfesorCreate

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

def test_create_profesor_service(db):
    profesor_data = ProfesorCreate(
        nombre = "Jordi Quezada",
        correo = "jordiquezada@gmail.com",
        especialidad = "Base de datos"
    )
    nuevo = create_profesor(db, profesor_data)

    assert nuevo.id is not None
    assert nuevo.nombre == "Jordi Quezada"
    assert nuevo.correo == "jordiquezada@gmail.com"
    assert nuevo.especialidad == "Base de datos"