import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base

if TYPE_CHECKING:
    from backend.app.database.models.session import Session
    from backend.app.database.models.saved_message import SavedMessage
    from backend.app.database.models.note import Note


class User(Base):
    """Represents a Bhasha2Code user."""

    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="Default User",
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
    sessions: Mapped[List["Session"]] = relationship(
        "Session",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    saved_messages: Mapped[List["SavedMessage"]] = relationship(
        "SavedMessage",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    notes: Mapped[List["Note"]] = relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User(id='{self.id}', name='{self.name}')>"

