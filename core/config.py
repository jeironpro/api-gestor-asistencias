"""
    BaseSettings: es una clase base de pydantic diseñada para cargar configuraciones de la aplicación desde:
    · Variables de entorno (ENV)
    · Archivos (.env)
    · Diccionarios u otras fuentes.

    Permite crear una clase de configuración con validación de tipos automática.

    · Tipos verificados automáticamente (str, int, bool, etc.).
    · Valores por defecto si no existen en el entorno
    · Fácil integración con FastAPI u otras aplicaciones.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Gestor de Asistencia"
    APP_VERSION: str = "1.0.0"

    # Configuración de base de datos mysql
    DB_USER: str = "root"
    DB_PASSWORD: str = "jeironpro"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "gestor_asistencias"

    class Config:
        env_file = ".env"

settings = Settings()