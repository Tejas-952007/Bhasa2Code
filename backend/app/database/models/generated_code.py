import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base


class GeneratedCode(Base):
    """Represents structured code artifacts generated during a session."""

    __tablename__ = "generated_code"

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
    message_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    language: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="python",
    )
    code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    validation_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="unvalidated",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

    # Relationships
    session: Mapped["Session"] = relationship("Session", back_populates="generated_codes")
    message: Mapped["Message"] = relationship("Message", back_populates="generated_codes")

    def __repr__(self) -> str:
        return f"<GeneratedCode(id='{self.id}', session_id='{self.session_id}', language='{self.language}')>"

