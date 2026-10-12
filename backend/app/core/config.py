import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()


class Settings(BaseModel):
    PROJECT_NAME: str = Field(default="Bhasha2Code")
    APP_ENV: str = Field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    BACKEND_HOST: str = Field(default_factory=lambda: os.getenv("BACKEND_HOST", "127.0.0.1"))
    BACKEND_PORT: int = Field(default_factory=lambda: int(os.getenv("BACKEND_PORT", "8000")))
    DATABASE_URL: str = Field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./data/bhasha2code.db")
    )
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
            ).split(",")
            if origin.strip()
        ]
    )
    DEFAULT_USER_ID: str = Field(
        default_factory=lambda: os.getenv("DEFAULT_USER_ID", "default-user")
    )
    DEFAULT_USER_NAME: str = Field(
        default_factory=lambda: os.getenv("DEFAULT_USER_NAME", "Local User")
    )
    API_V1_STR: str = Field(default="/api/v1")


settings = Settings()

