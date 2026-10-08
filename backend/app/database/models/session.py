import uuid
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import String, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base


class Session(Base):
    """Represents one persistent coding/study conversation session."""

    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="Untitled Session",
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
    )
    current_language: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    programming_language: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    current_code: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="sessions")
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )
    generated_codes: Mapped[List["GeneratedCode"]] = relationship(
        "GeneratedCode",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    debug_histories: Mapped[List["DebugHistory"]] = relationship(
        "DebugHistory",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    notes: Mapped[List["Note"]] = relationship(
        "Note",
        back_populates="session",
    )

    def __repr__(self) -> str:
        return f"<Session(id='{self.id}', user_id='{self.user_id}', title='{self.title}', status='{self.status}')>"

