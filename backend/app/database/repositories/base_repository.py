import logging
from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.database.base import Base

logger = logging.getLogger("bhasha2code.database.repository")

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic base repository providing shared query, existence, and transaction-safe operations."""

    def __init__(self, db: Session, model: Type[ModelType]) -> None:
        self.db = db
        self.model = model

    def _save(self, instance: ModelType, commit: bool = True) -> ModelType:
        """Add and persist an instance with automatic rollback on error.
        
        If commit is True, the transaction commits and refreshes the model instance.
        If commit is False, the session is flushed, allowing caller-level transaction management.
        """
        try:
            self.db.add(instance)
            if commit:
                self.db.commit()
                self.db.refresh(instance)
            else:
                self.db.flush()
            return instance
        except Exception as exc:
            self.db.rollback()
            logger.error("Database operation failed on %s: %s", self.model.__name__, exc)
            raise

    def get_by_id(self, id: str) -> Optional[ModelType]:
        """Fetch a single record by its primary key ID."""
        stmt = select(self.model).where(self.model.id == id)
        return self.db.scalars(stmt).first()

    def list_all(self, limit: int = 100, offset: int = 0) -> List[ModelType]:
        """Fetch records with simple pagination."""
        stmt = select(self.model).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def count(self) -> int:
        """Count total records for this entity."""
        stmt = select(func.count()).select_from(self.model)
        return self.db.scalar(stmt) or 0

    def exists(self, id: str) -> bool:
        """Check whether a record with the specified ID exists."""
        stmt = select(func.count()).select_from(self.model).where(self.model.id == id)
        count = self.db.scalar(stmt) or 0
        return count > 0

    def delete(self, id: str, commit: bool = True) -> bool:
        """Delete a record by ID. Returns True if deleted, False if not found."""
        instance = self.get_by_id(id)
        if instance is None:
            return False
        try:
            self.db.delete(instance)
            if commit:
                self.db.commit()
            else:
                self.db.flush()
            return True
        except Exception as exc:
            self.db.rollback()
            logger.error("Failed to delete %s id=%s: %s", self.model.__name__, id, exc)
            raise
