import logging
import os
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from backend.app.core.config import settings
from backend.app.database.base import Base

logger = logging.getLogger("bhasha2code.database")


def get_engine_args(url: str) -> dict:
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return {"connect_args": connect_args}


def create_db_engine(url: str | None = None):
    db_url = url or settings.DATABASE_URL
    return create_engine(db_url, **get_engine_args(db_url))


engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Dependency for providing a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_sqlite_directory(url: str) -> None:
    """Ensure parent directory exists for local SQLite database file."""
    if url.startswith("sqlite:///") and not url.startswith("sqlite:///:memory:"):
        db_path = url.replace("sqlite:///", "", 1)
        parent_dir = os.path.dirname(db_path)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)


def init_db(target_engine=None, url: str | None = None) -> None:
    """Safely initialize database tables and directories without destructive recreation."""
    active_engine = target_engine or engine
    db_url = url or str(active_engine.url)
    ensure_sqlite_directory(db_url)
    Base.metadata.create_all(bind=active_engine)
    logger.info("Database initialized successfully at %s", db_url)


def check_db_connection(target_engine=None) -> bool:
    """Check whether a database connection can be established."""
    active_engine = target_engine or engine
    try:
        with active_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.error("Database connection check failed: %s", exc)
        return False
