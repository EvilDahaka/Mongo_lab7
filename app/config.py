from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuration loaded from .env"""

    # MongoDB settings (required in .env)
    mongodb_url: str
    mongodb_db_name: str
    mongodb_username: str = "root"
    mongodb_password: str

    # App settings
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False

    # JWT / auth (must be set in .env)
    secret_key: str
    jwt_lifetime_seconds: int = 3600

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
