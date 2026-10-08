import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from backend.app.database.models.session import Session
from backend.app.database.repositories.base_repository import BaseRepository


class SessionRepository(BaseRepository[Session]):
    """Repository handling database operations for Session records with ownership and isolation support."""

    def __init__(self, db: DbSession) -> None:
        super().__init__(db, Session)

    def create(
        self,
        user_id: str,
        title: str = "Untitled Session",
        status: str = "active",
        current_language: Optional[str] = None,
        programming_language: Optional[str] = None,
        current_code: Optional[str] = None,
        id: Optional[str] = None,
        commit: bool = True,
    ) -> Session:
        """Create and persist a new conversation session for a user."""
        session = Session(
            id=id or str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            status=status,
            current_language=current_language,
            programming_language=programming_language,
            current_code=current_code,
        )
        return self._save(session, commit=commit)

    def create_session(
        self,
        user_id: str,
        title: str = "Untitled Session",
        status: str = "active",
        current_language: Optional[str] = None,
        programming_language: Optional[str] = None,
        current_code: Optional[str] = None,
        id: Optional[str] = None,
        commit: bool = True,
    ) -> Session:
        """Alias for create()."""
        return self.create(
            user_id=user_id,
            title=title,
            status=status,
            current_language=current_language,
            programming_language=programming_language,
            current_code=current_code,
            id=id,
            commit=commit,
        )

    def get_by_id(
        self,
        session_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Session]:
        """Fetch a session by ID, optionally validating user ownership."""
        stmt = select(Session).where(Session.id == session_id)
        if user_id is not None:
            stmt = stmt.where(Session.user_id == user_id)
        return self.db.scalars(stmt).first()

    def get_session_by_id(
        self,
        session_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Session]:
        """Alias for get_by_id()."""
        return self.get_by_id(session_id=session_id, user_id=user_id)

    def list_by_user(
        self,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Session]:
        """List sessions belonging to a specific user, ordered by updated_at descending."""
        stmt = select(Session).where(Session.user_id == user_id)
        if status is not None:
            stmt = stmt.where(Session.status == status)
        stmt = stmt.order_by(Session.updated_at.desc()).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def list_sessions_by_user(
        self,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Session]:
        """Alias for list_by_user()."""
        return self.list_by_user(
            user_id=user_id,
            status=status,
            limit=limit,
            offset=offset,
        )

    def update(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
        current_language: Optional[str] = None,
        programming_language: Optional[str] = None,
        current_code: Optional[str] = None,
        commit: bool = True,
    ) -> Optional[Session]:
        """Update session fields with ownership validation."""
        session = self.get_by_id(session_id, user_id=user_id)
        if session is None:
            return None

        if title is not None:
            session.title = title
        if status is not None:
            session.status = status
        if current_language is not None:
            session.current_language = current_language
        if programming_language is not None:
            session.programming_language = programming_language
        if current_code is not None:
            session.current_code = current_code

        session.updated_at = datetime.now(timezone.utc)
        return self._save(session, commit=commit)

    def update_session(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
        current_language: Optional[str] = None,
        programming_language: Optional[str] = None,
        current_code: Optional[str] = None,
        commit: bool = True,
    ) -> Optional[Session]:
        """Alias for update()."""
        return self.update(
            session_id=session_id,
            user_id=user_id,
            title=title,
            status=status,
            current_language=current_language,
            programming_language=programming_language,
            current_code=current_code,
            commit=commit,
        )

    def delete(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        commit: bool = True,
    ) -> bool:
        """Delete a session, optionally verifying user ownership."""
        session = self.get_by_id(session_id, user_id=user_id)
        if session is None:
            return False

        try:
            self.db.delete(session)
            if commit:
                self.db.commit()
            else:
                self.db.flush()
            return True
        except Exception:
            self.db.rollback()
            raise

    def delete_session(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        commit: bool = True,
    ) -> bool:
        """Alias for delete()."""
        return self.delete(session_id=session_id, user_id=user_id, commit=commit)

    def search(
        self,
        user_id: str,
        query: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Session]:
        """Search sessions by title for a specific user, ordered by updated_at descending."""
        escaped_query = f"%{query}%"
        stmt = (
            select(Session)
            .where(
                Session.user_id == user_id,
                Session.title.ilike(escaped_query),
            )
            .order_by(Session.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def search_sessions(
        self,
        user_id: str,
        query: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Session]:
        """Alias for search()."""
        return self.search(
            user_id=user_id,
            query=query,
            limit=limit,
            offset=offset,
        )
