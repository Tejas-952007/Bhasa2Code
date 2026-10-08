import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base

if TYPE_CHECKING:
    from backend.app.database.models.session import Session
    from backend.app.database.models.message import Message


class DebugHistory(Base):
    """Represents a code debugging iteration and outcome."""

    __tablename__ = "debug_history"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    message_id: Mapped[Optional[str]] = mapped_column(
        String(36),
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    original_code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    error_message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    corrected_code: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    validation_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )
    attempt_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="debug_histories")
    message: Mapped[Optional["Message"]] = relationship("Message", back_populates="debug_histories")

    def __repr__(self) -> str:
        return f"<DebugHistory(id='{self.id}', session_id='{self.session_id}', validation_status='{self.validation_status}', attempt={self.attempt_count})>"

