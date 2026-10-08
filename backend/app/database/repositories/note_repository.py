import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from backend.app.database.models.note import Note
from backend.app.database.repositories.base_repository import BaseRepository


class NoteRepository(BaseRepository[Note]):
    """Repository handling database operations for personal and session-linked notes."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, Note)

    def create(
        self,
        user_id: str,
        title: str = "Untitled Note",
        content: str = "",
        session_id: Optional[str] = None,
        id: Optional[str] = None,
        commit: bool = True,
    ) -> Note:
        """Create and persist a new note."""
        note = Note(
            id=id or str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            content=content,
            session_id=session_id,
        )
        return self._save(note, commit=commit)

    def create_note(
        self,
        user_id: str,
        title: str = "Untitled Note",
        content: str = "",
        session_id: Optional[str] = None,
        id: Optional[str] = None,
        commit: bool = True,
    ) -> Note:
        """Alias for create()."""
        return self.create(
            user_id=user_id,
            title=title,
            content=content,
            session_id=session_id,
            id=id,
            commit=commit,
        )

    def get_by_id(
        self,
        note_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Note]:
        """Fetch a note by ID, optionally validating user ownership."""
        stmt = select(Note).where(Note.id == note_id)
        if user_id is not None:
            stmt = stmt.where(Note.user_id == user_id)
        return self.db.scalars(stmt).first()

    def get_note_by_id(
        self,
        note_id: str,
        user_id: Optional[str] = None,
    ) -> Optional[Note]:
        """Alias for get_by_id()."""
        return self.get_by_id(note_id=note_id, user_id=user_id)

    def list_notes_by_user(
        self,
        user_id: str,
        session_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Note]:
        """List notes belonging to a user, optionally filtered by session_id, ordered by updated_at descending."""
        stmt = select(Note).where(Note.user_id == user_id)
        if session_id is not None:
            stmt = stmt.where(Note.session_id == session_id)
        stmt = stmt.order_by(Note.updated_at.desc()).offset(offset).limit(limit)
        return list(self.db.scalars(stmt).all())

    def list_by_user(
        self,
        user_id: str,
        session_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Note]:
        """Alias for list_notes_by_user()."""
        return self.list_notes_by_user(
            user_id=user_id,
            session_id=session_id,
            limit=limit,
            offset=offset,
        )

    def update(
        self,
        note_id: str,
        user_id: Optional[str] = None,
        title: Optional[str] = None,
        content: Optional[str] = None,
        session_id: Optional[str] = None,
        commit: bool = True,
    ) -> Optional[Note]:
        """Update an existing note with ownership validation."""
        note = self.get_by_id(note_id, user_id=user_id)
        if note is None:
            return None

        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if session_id is not None:
            note.session_id = session_id

        note.updated_at = datetime.now(timezone.utc)
        return self._save(note, commit=commit)

    def update_note(
        self,
        note_id: str,
        user_id: Optional[str] = None,
        title: Optional[str] = None,
        content: Optional[str] = None,
        session_id: Optional[str] = None,
        commit: bool = True,
    ) -> Optional[Note]:
        """Alias for update()."""
        return self.update(
            note_id=note_id,
            user_id=user_id,
            title=title,
            content=content,
            session_id=session_id,
            commit=commit,
        )

    def delete(
        self,
        note_id: str,
        user_id: Optional[str] = None,
        commit: bool = True,
    ) -> bool:
        """Delete a note with ownership validation."""
        note = self.get_by_id(note_id, user_id=user_id)
        if note is None:
            return False

        try:
            self.db.delete(note)
            if commit:
                self.db.commit()
            else:
                self.db.flush()
            return True
        except Exception:
            self.db.rollback()
            raise

    def delete_note(
        self,
        note_id: str,
        user_id: Optional[str] = None,
        commit: bool = True,
    ) -> bool:
        """Alias for delete()."""
        return self.delete(note_id=note_id, user_id=user_id, commit=commit)

    def search(
        self,
        user_id: str,
        query: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Note]:
        """Search notes by title or content for a user, ordered by updated_at descending."""
        escaped_query = f"%{query}%"
        stmt = (
            select(Note)
            .where(
                Note.user_id == user_id,
                or_(
                    Note.title.ilike(escaped_query),
                    Note.content.ilike(escaped_query),
                ),
            )
            .order_by(Note.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def search_notes(
        self,
        user_id: str,
        query: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Note]:
        """Alias for search()."""
        return self.search(
            user_id=user_id,
            query=query,
            limit=limit,
            offset=offset,
        )
