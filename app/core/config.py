from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Gestor de Asistencia"
    APP_VERSION: str = "1.0.0"

    # Configuración de base de datos mysql
    DB_USER: str = "root"
    DB_PASSWORD: str = "jeironpro"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "gestor_asistencia"

    class Config:
        env_file = ".env"

settings = Settings()