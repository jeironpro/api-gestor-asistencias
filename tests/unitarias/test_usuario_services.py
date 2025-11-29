import pytest
from sqlmodel import create_engine, Session, SQLModel
from services.usuario_services import (
    crear_usuario, obtener_usuarios, obtener_usuario_id,
    obtener_usuario_correo_electronico, actualizar_usuario_id,
    desactivar_usuario, cifrar_contrasena, verificar_contrasena
)
from schemas.usuario import CrearUsuario, ActualizarUsuario
from models.Usuario import Usuario, RolUsuario
from fastapi import HTTPException

def test_crear_usuario(db):
    usuario_data = CrearUsuario(
        nombre="Juan",
        apellido="Pérez",
        correoElectronico="juan@test.com",
        contrasena="password123",
        rol=RolUsuario.estudiante
    )
    nuevo_usuario = crear_usuario(db, usuario_data)

    assert nuevo_usuario.id is not None
    assert nuevo_usuario.nombre == "Juan"
    assert nuevo_usuario.apellido == "Pérez"
    assert nuevo_usuario.correoElectronico == "juan@test.com"
    assert nuevo_usuario.rol == RolUsuario.estudiante
    assert nuevo_usuario.activo == True
    assert nuevo_usuario.contrasena != "password123"
    assert verificar_contrasena("password123", nuevo_usuario.contrasena)

def test_crear_usuario_duplicado(db):
    usuario_data = CrearUsuario(
        nombre="Juan",
        apellido="Pérez",
        correoElectronico="juan@test.com",
        contrasena="password123",
        rol=RolUsuario.estudiante
    )
    crear_usuario(db, usuario_data)
    
    with pytest.raises(HTTPException) as exc_info:
        crear_usuario(db, usuario_data)
    
    assert exc_info.value.status_code == 400
    assert "correo electrónico ya está registrado" in exc_info.value.detail

def test_obtener_usuarios_paginacion(db):
    for i in range(5):
        usuario_data = CrearUsuario(
            nombre=f"Usuario{i}",
            apellido="Test",
            correoElectronico=f"usuario{i}@test.com",
            contrasena="password123",
            rol=RolUsuario.estudiante
        )
        crear_usuario(db, usuario_data)
    
    usuarios = obtener_usuarios(db, skip=0, limit=3)
    assert len(usuarios) == 3
    
    usuarios = obtener_usuarios(db, skip=3, limit=3)
    assert len(usuarios) == 2

def test_obtener_usuario_id(db):
    usuario_data = CrearUsuario(
        nombre="Juan",
        apellido="Pérez",
        correoElectronico="juan@test.com",
        contrasena="password123",
        rol=RolUsuario.estudiante
    )
    nuevo_usuario = crear_usuario(db, usuario_data)
    
    usuario_encontrado = obtener_usuario_id(db, nuevo_usuario.id)
    assert usuario_encontrado is not None
    assert usuario_encontrado.id == nuevo_usuario.id
    assert usuario_encontrado.nombre == "Juan"

def test_obtener_usuario_id_no_existe(db):
    usuario = obtener_usuario_id(db, "id-inexistente")
    assert usuario is None

def test_obtener_usuario_correo(db):
    usuario_data = CrearUsuario(
        nombre="Juan",
        apellido="Pérez",
        correoElectronico="juan@test.com",
        contrasena="password123",
        rol=RolUsuario.estudiante
    )
    crear_usuario(db, usuario_data)
    
    usuario_encontrado = obtener_usuario_correo_electronico(db, "juan@test.com")
    assert usuario_encontrado is not None
    assert usuario_encontrado.correoElectronico == "juan@test.com"

def test_actualizar_usuario(db):
    usuario_data = CrearUsuario(
        nombre="Juan",
        apellido="Pérez",
        correoElectronico="juan@test.com",
        contrasena="password123",
        rol=RolUsuario.estudiante
    )
    nuevo_usuario = crear_usuario(db, usuario_data)
    
    actualizar_data = ActualizarUsuario(
        nombre="Juan Carlos",
        apellido="Pérez García"
    )
    usuario_actualizado = actualizar_usuario_id(db, nuevo_usuario.id, actualizar_data)
    
    assert usuario_actualizado.nombre == "Juan Carlos"
    assert usuario_actualizado.apellido == "Pérez García"
    assert usuario_actualizado.correoElectronico == "juan@test.com"

def test_actualizar_usuario_no_existe(db):
    actualizar_data = ActualizarUsuario(nombre="Test")
    
    with pytest.raises(HTTPException) as exc_info:
        actualizar_usuario_id(db, "id-inexistente", actualizar_data)
    
    assert exc_info.value.status_code == 404

def test_desactivar_usuario(db):
    usuario_data = CrearUsuario(
        nombre="Juan",
        apellido="Pérez",
        correoElectronico="juan@test.com",
        contrasena="password123",
        rol=RolUsuario.estudiante
    )
    nuevo_usuario = crear_usuario(db, usuario_data)
    
    usuario_desactivado = desactivar_usuario(db, nuevo_usuario.id)
    assert usuario_desactivado.activo == False
    
    usuario_encontrado = obtener_usuario_id(db, nuevo_usuario.id)
    assert usuario_encontrado is None

def test_desactivar_usuario_no_existe(db):
    with pytest.raises(HTTPException) as exc_info:
        desactivar_usuario(db, "id-inexistente")
    
    assert exc_info.value.status_code == 404

def test_cifrar_y_verificar_contrasena():
    password = "mi_password_seguro"
    hashed = cifrar_contrasena(password)
    
    assert hashed != password
    assert verificar_contrasena(password, hashed) == True
    assert verificar_contrasena("password_incorrecto", hashed) == False
