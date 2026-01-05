from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "PyTarot"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: str = "pytarot"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "pytarot_db"
    POSTGRES_PORT: str = "5432"
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # If POSTGRES_SERVER is 'localhost' but no DB is running, it might fail.
        # For this environment, we force SQLite if we want to ensure it works.
        if self.POSTGRES_SERVER and self.POSTGRES_SERVER not in ["None", "", "localhost"]:
            return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return "sqlite+aiosqlite:///./tarot.db"
    
    # AI Service
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
