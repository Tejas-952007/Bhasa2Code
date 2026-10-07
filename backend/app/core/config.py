import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    PROJECT_NAME: str = Field(default="Bhasha2Code")
    APP_ENV: str = Field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    BACKEND_HOST: str = Field(default_factory=lambda: os.getenv("BACKEND_HOST", "127.0.0.1"))
    BACKEND_PORT: int = Field(default_factory=lambda: int(os.getenv("BACKEND_PORT", "8000")))
    DATABASE_URL: str = Field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./data/bhasha2code.db")
    )


settings = Settings()
