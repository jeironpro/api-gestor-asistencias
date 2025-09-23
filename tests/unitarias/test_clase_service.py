import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base
from app.services.clase_service import create_clase
from app.schemas.clase import ClaseCreate

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

def test_create_clase_service(db):
    clase_data = ClaseCreate(
        nombre = "DAW 2B",
        horario = "15:30 - 21:00",
        profesor_id = 1
    )
    nuevo = create_clase(db, clase_data)

    assert nuevo.id is not None
    assert nuevo.nombre == "DAW 2B"
    assert nuevo.horario == "15:30 - 21:00"
    assert nuevo.profesor_id == 1