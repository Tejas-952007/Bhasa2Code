import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models.saved_message import SavedMessage
from backend.app.database.repositories.base_repository import BaseRepository


class SavedMessageRepository(BaseRepository[SavedMessage]):
    """Repository handling database operations for user-bookmarked/saved messages."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, SavedMessage)

    def save_message(
        self,
        user_id: str,
        message_id: str,
        label: Optional[str] = None,
        id: Optional[str] = None,
        commit: bool = True,
    ) -> SavedMessage:
        """Save/bookmark a message for a user.
        
        Handles duplicate save idempotently: if already saved, updates label if provided,
        and returns the existing record without violating unique constraint.
        """
        existing = self.get_saved_message(user_id=user_id, message_id=message_id)
        if existing is not None:
            if label is not None and existing.label != label:
                existing.label = label
                return self._save(existing, commit=commit)
            return existing

        saved_message = SavedMessage(
            id=id or str(uuid.uuid4()),
            user_id=user_id,
            message_id=message_id,
            label=label,
        )
        return self._save(saved_message, commit=commit)

    def get_by_id(
        self,
        saved_message_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[SavedMessage]:
        """Fetch a saved message record by ID, optionally verifying user ownership."""
        stmt = select(SavedMessage).where(SavedMessage.id == saved_message_id)
        if user_id is not None:
            stmt = stmt.where(SavedMessage.user_id == user_id)
        return self.db.scalars(stmt).first()

    def get_saved_message(
        self,
        user_id: str,
        message_id: str,
    ) -> Optional[SavedMessage]:
        """Fetch a saved message record for a specific user and message pair."""
        stmt = select(SavedMessage).where(
            SavedMessage.user_id == user_id,
            SavedMessage.message_id == message_id,
        )
        return self.db.scalars(stmt).first()

    def list_saved_messages(
        self,
        user_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[SavedMessage]:
        """List all saved messages for a user, ordered by saved timestamp descending."""
        stmt = (
            select(SavedMessage)
            .where(SavedMessage.user_id == user_id)
            .order_by(SavedMessage.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def unsave_message(
        self,
        user_id: str,
        message_id: str,
        commit: bool = True,
    ) -> bool:
        """Remove a saved message bookmark by user_id and message_id. Returns True if removed."""
        record = self.get_saved_message(user_id=user_id, message_id=message_id)
        if record is None:
            return False

        try:
            self.db.delete(record)
            if commit:
                self.db.commit()
            else:
                self.db.flush()
            return True
        except Exception:
            self.db.rollback()
            raise

    def is_saved(self, user_id: str, message_id: str) -> bool:
        """Check whether a specific message is saved by a user."""
        return self.get_saved_message(user_id=user_id, message_id=message_id) is not None
