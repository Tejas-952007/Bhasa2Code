import uuid
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.database.models.generated_code import GeneratedCode
from backend.app.database.repositories.base_repository import BaseRepository


class GeneratedCodeRepository(BaseRepository[GeneratedCode]):
    """Repository handling database operations for generated code artifacts."""

    def __init__(self, db: Session) -> None:
        super().__init__(db, GeneratedCode)

    def create(
        self,
        session_id: str,
        message_id: str,
        code: str,
        language: str = "python",
        validation_status: str = "unvalidated",
        id: Optional[str] = None,
        commit: bool = True,
    ) -> GeneratedCode:
        """Create and persist a generated code record."""
        generated = GeneratedCode(
            id=id or str(uuid.uuid4()),
            session_id=session_id,
            message_id=message_id,
            code=code,
            language=language,
            validation_status=validation_status,
        )
        return self._save(generated, commit=commit)

    def create_generated_code(
        self,
        session_id: str,
        message_id: str,
        code: str,
        language: str = "python",
        validation_status: str = "unvalidated",
        id: Optional[str] = None,
        commit: bool = True,
    ) -> GeneratedCode:
        """Alias for create()."""
        return self.create(
            session_id=session_id,
            message_id=message_id,
            code=code,
            language=language,
            validation_status=validation_status,
            id=id,
            commit=commit,
        )

    def get_generated_code_by_id(self, code_id: str) -> Optional[GeneratedCode]:
        """Fetch a generated code record by ID."""
        return self.get_by_id(code_id)

    def get_code_for_message(self, message_id: str) -> List[GeneratedCode]:
        """Fetch all code artifacts associated with a specific message."""
        stmt = (
            select(GeneratedCode)
            .where(GeneratedCode.message_id == message_id)
            .order_by(GeneratedCode.created_at.desc())
        )
        return list(self.db.scalars(stmt).all())

    def list_code_by_session(
        self,
        session_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> List[GeneratedCode]:
        """List code artifacts generated in a session, ordered by newest first."""
        stmt = (
            select(GeneratedCode)
            .where(GeneratedCode.session_id == session_id)
            .order_by(GeneratedCode.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())

    def update_validation_status(
        self,
        code_id: str,
        validation_status: str,
        commit: bool = True,
    ) -> Optional[GeneratedCode]:
        """Update the validation status of a generated code artifact."""
        record = self.get_by_id(code_id)
        if record is None:
            return None

        record.validation_status = validation_status
        return self._save(record, commit=commit)
