import uuid
from typing import List, Optional
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.database.models.message import Message
from backend.app.database.repositories.base_repository import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """Repository handling database operations for conversation messages with strict session isolation."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, Message)

    def create(
        self,
        session_id: str,
        role: str,
        content: str,
        detected_language: Optional[str] = None,
        intent: Optional[str] = None,
        tone: Optional[str] = None,
        programming_language: Optional[str] = None,
        context_metadata: Optional[dict] = None,
        id: Optional[str] = None,
        commit: bool = True,
    ) -> Message:
        """Create and persist a conversation message within a session."""
        message = Message(
            id=id or str(uuid.uuid4()),
            session_id=session_id,
            role=role,
            content=content,
            detected_language=detected_language,
            intent=intent,
            tone=tone,
            programming_language=programming_language,
            context_metadata=context_metadata,
        )
        return self._save(message, commit=commit)

    def create_message(
        self,
        session_id: str,
        role: str,
        content: str,
        detected_language: Optional[str] = None,
        intent: Optional[str] = None,
        tone: Optional[str] = None,
        programming_language: Optional[str] = None,
        context_metadata: Optional[dict] = None,
        id: Optional[str] = None,
        commit: bool = True,
    ) -> Message:
        """Alias for create()."""
        return self.create(
            session_id=session_id,
            role=role,
            content=content,
            detected_language=detected_language,
            intent=intent,
            tone=tone,
            programming_language=programming_language,
            context_metadata=context_metadata,
            id=id,
            commit=commit,
        )

    def get_by_id(
        self,
        message_id: str,
        session_id: Optional[str] = None,
    ) -> Optional[Message]:
        """Fetch a message by ID, optionally scoped to a session for isolation."""
        stmt = select(Message).where(Message.id == message_id)
        if session_id is not None:
            stmt = stmt.where(Message.session_id == session_id)
        return self.db.scalars(stmt).first()

    def get_message_by_id(
        self,
        message_id: str,
        session_id: Optional[str] = None,
    ) -> Optional[Message]:
        """Alias for get_by_id()."""
        return self.get_by_id(message_id=message_id, session_id=session_id)

    def list_by_session(
        self,
        session_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Message]:
        """List messages for a session in deterministic chronological order (created_at ASC)."""
        stmt = (
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def list_messages_by_session(
        self,
        session_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Message]:
        """Alias for list_by_session()."""
        return self.list_by_session(
            session_id=session_id,
            limit=limit,
            offset=offset,
        )

    def delete(
        self,
        message_id: str,
        session_id: Optional[str] = None,
        commit: bool = True,
    ) -> bool:
        """Delete a message, optionally verifying session association."""
        message = self.get_by_id(message_id, session_id=session_id)
        if message is None:
            return False

        try:
            self.db.delete(message)
            if commit:
                self.db.commit()
            else:
                self.db.flush()
            return True
        except Exception:
            self.db.rollback()
            raise

    def delete_message(
        self,
        message_id: str,
        session_id: Optional[str] = None,
        commit: bool = True,
    ) -> bool:
        """Alias for delete()."""
        return self.delete(message_id=message_id, session_id=session_id, commit=commit)

    def search(
        self,
        session_id: str,
        query: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Message]:
        """Search message text within a specific session, ordered by created_at ASC."""
        escaped_query = f"%{query}%"
        stmt = (
            select(Message)
            .where(
                Message.session_id == session_id,
                Message.content.ilike(escaped_query),
            )
            .order_by(Message.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def search_messages(
        self,
        session_id: str,
        query: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Message]:
        """Alias for search()."""
        return self.search(
            session_id=session_id,
            query=query,
            limit=limit,
            offset=offset,
        )

    def count_by_session(self, session_id: str) -> int:
        """Count total messages in a session."""
        stmt = (
            select(func.count())
            .select_from(Message)
            .where(Message.session_id == session_id)
        )
        return self.db.scalar(stmt) or 0

    def get_latest_message(self, session_id: str) -> Optional[Message]:
        """Fetch the most recent message in a session."""
        stmt = (
            select(Message)
            .where(Message.session_id == session_id)
            .order_by(Message.created_at.desc())
            .limit(1)
        )
        return self.db.scalars(stmt).first()
