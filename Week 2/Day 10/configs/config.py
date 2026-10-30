from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "REST Mini Project API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"

settings = Settings()
