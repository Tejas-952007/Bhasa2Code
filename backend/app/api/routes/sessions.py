"""Session management API endpoints for Bhasha2Code."""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_current_user_id
from backend.app.api.exceptions import (
    SessionNotFoundAPIError,
    UnauthorizedSessionAPIError,
)
from backend.app.api.schemas import (
    MessageItemResponse,
    SessionCreateRequest,
    SessionDetailResponse,
    SessionResponse,
    SessionUpdateRequest,
)
from backend.app.database.engine import get_db
from backend.app.database.repositories.generated_code_repository import (
    GeneratedCodeRepository,
)
from backend.app.database.repositories.message_repository import MessageRepository
from backend.app.database.repositories.session_repository import SessionRepository

logger = logging.getLogger("bhasha2code.api.sessions")

router = APIRouter(prefix="/sessions", tags=["sessions"])

EXTENSION_MAP = {
    "python": "py",
    "c": "c",
    "cpp": "cpp",
    "c++": "cpp",
    "java": "java",
    "javascript": "js",
    "sql": "sql",
}


def _get_filename(language: Optional[str]) -> str:
    lang = (language or "python").lower()
    ext = EXTENSION_MAP.get(lang, "py")
    return f"main.{ext}"


@router.get("", response_model=List[SessionResponse], summary="List user sessions")
def list_sessions(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> List[SessionResponse]:
    """Retrieve all sessions belonging to the current user, newest first."""
    session_repo = SessionRepository(db)
    sessions = session_repo.list_by_user(user_id=user_id, limit=limit, offset=offset)
    return [
        SessionResponse(
            id=s.id,
            title=s.title,
            status=s.status,
            created_at=s.created_at.isoformat() if s.created_at else "",
            updated_at=s.updated_at.isoformat() if s.updated_at else "",
            current_language=s.current_language,
            programming_language=s.programming_language,
        )
        for s in sessions
    ]


@router.post(
    "",
    response_model=SessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new session",
)
def create_session(
    payload: SessionCreateRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> SessionResponse:
    """Create a new session for the current user."""
    session_repo = SessionRepository(db)
    title = (payload.title or "").strip() or "Untitled Chat"

    session = session_repo.create(
        user_id=user_id,
        title=title,
        status="active",
        commit=True,
    )
    return SessionResponse(
        id=session.id,
        title=session.title,
        status=session.status,
        created_at=session.created_at.isoformat() if session.created_at else "",
        updated_at=session.updated_at.isoformat() if session.updated_at else "",
        current_language=session.current_language,
        programming_language=session.programming_language,
    )


@router.get(
    "/{session_id}",
    response_model=SessionDetailResponse,
    summary="Get session details and messages",
)
def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> SessionDetailResponse:
    """Retrieve a session with all its messages and code artifacts."""
    session_repo = SessionRepository(db)
    session = session_repo.get_by_id(session_id=session_id)

    if session is None:
        raise SessionNotFoundAPIError()

    if session.user_id != user_id:
        raise UnauthorizedSessionAPIError()

    msg_repo = MessageRepository(db)
    code_repo = GeneratedCodeRepository(db)

    messages = msg_repo.list_by_session(session_id=session_id)
    message_items: List[MessageItemResponse] = []

    for msg in messages:
        metadata = msg.context_metadata or {}
        code_block = metadata.get("code_block")
        study = metadata.get("study")

        # If not stored in context_metadata, look up generated code artifacts
        if not code_block:
            codes = code_repo.get_code_for_message(msg.id)
            if codes:
                primary = codes[0]
                code_block = {
                    "id": primary.id,
                    "language": primary.language or "python",
                    "filename": _get_filename(primary.language),
                    "code": primary.code,
                    "validationStatus": (primary.validation_status or "VALID").upper(),
                }

        message_items.append(
            MessageItemResponse(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                detected_language=msg.detected_language,
                intent=msg.intent,
                tone=msg.tone,
                code_block=code_block,
                study=study,
                created_at=msg.created_at.isoformat() if msg.created_at else "",
            )
        )

    return SessionDetailResponse(
        id=session.id,
        title=session.title,
        status=session.status,
        created_at=session.created_at.isoformat() if session.created_at else "",
        updated_at=session.updated_at.isoformat() if session.updated_at else "",
        messages=message_items,
    )


@router.patch(
    "/{session_id}",
    response_model=SessionResponse,
    summary="Update session title",
)
def update_session(
    session_id: str,
    payload: SessionUpdateRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> SessionResponse:
    """Rename an existing session."""
    session_repo = SessionRepository(db)
    session = session_repo.get_by_id(session_id=session_id)

    if session is None:
        raise SessionNotFoundAPIError()

    if session.user_id != user_id:
        raise UnauthorizedSessionAPIError()

    new_title = payload.title.strip() if payload.title else "Untitled Chat"
    updated = session_repo.update(
        session_id=session_id,
        user_id=user_id,
        title=new_title,
        commit=True,
    )

    if updated is None:
        raise SessionNotFoundAPIError()

    return SessionResponse(
        id=updated.id,
        title=updated.title,
        status=updated.status,
        created_at=updated.created_at.isoformat() if updated.created_at else "",
        updated_at=updated.updated_at.isoformat() if updated.updated_at else "",
        current_language=updated.current_language,
        programming_language=updated.programming_language,
    )


@router.delete(
    "/{session_id}",
    summary="Delete a session",
)
def delete_session(
    session_id: str,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
) -> dict:
    """Delete a session and all its associated messages."""
    session_repo = SessionRepository(db)
    session = session_repo.get_by_id(session_id=session_id)

    if session is None:
        raise SessionNotFoundAPIError()

    if session.user_id != user_id:
        raise UnauthorizedSessionAPIError()

    deleted = session_repo.delete(session_id=session_id, user_id=user_id, commit=True)
    if not deleted:
        raise SessionNotFoundAPIError()

    return {"ok": True, "message": "Session deleted successfully"}
