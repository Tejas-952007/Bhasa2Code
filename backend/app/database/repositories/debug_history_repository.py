import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models.debug_history import DebugHistory
from backend.app.database.repositories.base_repository import BaseRepository


class DebugHistoryRepository(BaseRepository[DebugHistory]):
    """Repository handling append-oriented storage and retrieval of debugging iterations."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, DebugHistory)

    def create(
        self,
        session_id: str,
        original_code: str,
        error_message: str,
        message_id: Optional[str] = None,
        corrected_code: Optional[str] = None,
        validation_status: str = "pending",
        attempt_count: int = 1,
        id: Optional[str] = None,
        commit: bool = True,
    ) -> DebugHistory:
        """Create and persist a new append-only debug history record."""
        debug_record = DebugHistory(
            id=id or str(uuid.uuid4()),
            session_id=session_id,
            message_id=message_id,
            original_code=original_code,
            error_message=error_message,
            corrected_code=corrected_code,
            validation_status=validation_status,
            attempt_count=attempt_count,
        )
        return self._save(debug_record, commit=commit)

    def create_debug_record(
        self,
        session_id: str,
        original_code: str,
        error_message: str,
        message_id: Optional[str] = None,
        corrected_code: Optional[str] = None,
        validation_status: str = "pending",
        attempt_count: int = 1,
        id: Optional[str] = None,
        commit: bool = True,
    ) -> DebugHistory:
        """Alias for create()."""
        return self.create(
            session_id=session_id,
            original_code=original_code,
            error_message=error_message,
            message_id=message_id,
            corrected_code=corrected_code,
            validation_status=validation_status,
            attempt_count=attempt_count,
            id=id,
            commit=commit,
        )

    def get_debug_record_by_id(self, debug_id: str) -> Optional[DebugHistory]:
        """Fetch a debug record by ID."""
        return self.get_by_id(debug_id)

    def list_by_session(
        self,
        session_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[DebugHistory]:
        """List debug iterations for a session in chronological order (created_at ASC)."""
        stmt = (
            select(DebugHistory)
            .where(DebugHistory.session_id == session_id)
            .order_by(DebugHistory.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def list_debug_history_by_session(
        self,
        session_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[DebugHistory]:
        """Alias for list_by_session()."""
        return self.list_by_session(
            session_id=session_id,
            limit=limit,
            offset=offset,
        )

    def list_by_message(
        self,
        message_id: str,
    ) -> List[DebugHistory]:
        """List all debug attempts related to a specific conversation message."""
        stmt = (
            select(DebugHistory)
            .where(DebugHistory.message_id == message_id)
            .order_by(DebugHistory.created_at.asc())
        )
        return list(self.db.scalars(stmt).all())

    def get_latest_for_session(self, session_id: str) -> Optional[DebugHistory]:
        """Fetch the most recent debug iteration for a session."""
        stmt = (
            select(DebugHistory)
            .where(DebugHistory.session_id == session_id)
            .order_by(DebugHistory.created_at.desc())
            .limit(1)
        )
        return self.db.scalars(stmt).first()
