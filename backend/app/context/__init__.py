"""Context Manager module for conversational history and code context retrieval."""

from backend.app.context.context_manager import ContextManager
from backend.app.context.exceptions import (
    ContextError,
    SessionNotFoundError,
    UnauthorizedSessionError,
)
from backend.app.context.policies import ContextPolicy, is_follow_up
from backend.app.context.schemas import (
    ContextCode,
    ContextMessage,
    ContextMetadata,
    ContextPackage,
)

__all__ = [
    "ContextManager",
    "ContextPackage",
    "ContextMessage",
    "ContextCode",
    "ContextMetadata",
    "ContextPolicy",
    "is_follow_up",
    "ContextError",
    "SessionNotFoundError",
    "UnauthorizedSessionError",
]
