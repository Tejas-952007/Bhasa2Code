"""Exceptions for the Context Manager module."""


class ContextError(Exception):
    """Base exception for all Context Manager domain errors."""
    pass


class SessionNotFoundError(ContextError):
    """Raised when a requested session cannot be found in the database."""
    pass


class UnauthorizedSessionError(ContextError, PermissionError):
    """Raised when a user attempts to access a session they do not own."""
    pass
