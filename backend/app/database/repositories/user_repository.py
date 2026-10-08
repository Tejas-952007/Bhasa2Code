import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models.user import User
from backend.app.database.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository handling database operations for User records."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, User)

    def create(
        self,
        name: str = "Default User",
        id: Optional[str] = None,
        commit: bool = True,
    ) -> User:
        """Create and persist a new User."""
        user = User(
            id=id or str(uuid.uuid4()),
            name=name,
        )
        return self._save(user, commit=commit)

    def create_user(
        self,
        name: str = "Default User",
        id: Optional[str] = None,
        commit: bool = True,
    ) -> User:
        """Alias for create()."""
        return self.create(name=name, id=id, commit=commit)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Fetch a user by their ID."""
        return self.get_by_id(user_id)

    def list_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        """List users ordered by creation date descending."""
        stmt = (
            select(User)
            .order_by(User.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def update(
        self,
        user_id: str,
        name: Optional[str] = None,
        commit: bool = True,
    ) -> Optional[User]:
        """Update user properties."""
        user = self.get_by_id(user_id)
        if user is None:
            return None

        if name is not None:
            user.name = name
        user.updated_at = datetime.now(timezone.utc)

        return self._save(user, commit=commit)

    def delete_user(self, user_id: str, commit: bool = True) -> bool:
        """Delete a user by ID. Returns True if deleted, False if not found."""
        return self.delete(user_id, commit=commit)
