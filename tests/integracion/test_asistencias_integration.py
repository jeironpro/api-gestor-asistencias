from app.services.estudiante_service import create_estudiante
from app.services.profesor_service import create_profesor
from app.services.clase_service import create_clase
from app.services.asistencia_service import create_asistencia, get_asistencias
from app.schemas.estudiante import EstudianteCreate
from app.schemas.profesor import ProfesorCreate
from app.schemas.clase import ClaseCreate
from app.schemas.asistencia import AsistenciaCreate

def test_create_asistencia_relation(db):
    # Crear estudiante
    estudiante = create_estudiante(db, EstudianteCreate(
        nombre = "Jeiron",
        matricula = "J-2024",
        correo = "jeiron@gmail.com",
        curso = "DAW"
    ))

    # Crear profesor
    profesor = create_profesor(db, ProfesorCreate(
        nombre = "Alba",
        correo = "alba@gmail.com",
        especialidad = "Trabajos & Empresas"
    ))

    # Crear clase
    clase = create_clase(db, ClaseCreate(
        nombre = "DAM 1B",
        horario = "08:00 - 13:30",
        profesor_id = profesor.id
    ))

    # Crear asistencia
    asistencia = create_asistencia(db, AsistenciaCreate(
        fecha = "2025-09-21",
        estado = "presente",
        estudiante_id = estudiante.id,
        clase_id = clase.id
    ))

    assert asistencia.id is not None
    assert asistencia.estado == "presente"

    # Verificar listado
    asistencias = get_asistencias(db)
    assert len(asistencias) == 1
    assert asistencias[0].estudiante_id == estudiante.id

