import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import String, DateTime, Text, JSON, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base

if TYPE_CHECKING:
    from backend.app.database.models.session import Session
    from backend.app.database.models.generated_code import GeneratedCode
    from backend.app.database.models.debug_history import DebugHistory
    from backend.app.database.models.saved_message import SavedMessage


class Message(Base):
    """Represents one conversation turn in a session."""

    __tablename__ = "messages"
    __table_args__ = (
        CheckConstraint(
            "role IN ('user', 'assistant', 'system')",
            name="ck_messages_role",
        ),
    )

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
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    detected_language: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    intent: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    tone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    programming_language: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    context_metadata: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        index=True,
    )

    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="messages")
    generated_codes: Mapped[List["GeneratedCode"]] = relationship(
        "GeneratedCode",
        back_populates="message",
        cascade="all, delete-orphan",
    )
    debug_histories: Mapped[List["DebugHistory"]] = relationship(
        "DebugHistory",
        back_populates="message",
    )
    saved_messages: Mapped[List["SavedMessage"]] = relationship(
        "SavedMessage",
        back_populates="message",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Message(id='{self.id}', session_id='{self.session_id}', role='{self.role}')>"

