"""Pydantic schemas for Bhasha2Code FastAPI API endpoints."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Error Response Models
# ---------------------------------------------------------------------------

class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail


# ---------------------------------------------------------------------------
# Health Models
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str = "healthy"
    ollama: str = "available"
    model: str = "qwen2.5-coder:3b"
    sandbox: str = "available"
    database: str = "available"


# ---------------------------------------------------------------------------
# Session Models
# ---------------------------------------------------------------------------

class SessionCreateRequest(BaseModel):
    title: Optional[str] = None


class SessionUpdateRequest(BaseModel):
    title: Optional[str] = None


class SessionResponse(BaseModel):
    id: str
    title: str
    status: str = "active"
    created_at: str
    updated_at: str
    current_language: Optional[str] = None
    programming_language: Optional[str] = None


class MessageItemResponse(BaseModel):
    id: str
    role: str
    content: str
    detected_language: Optional[str] = None
    intent: Optional[str] = None
    tone: Optional[str] = None
    code_block: Optional[Dict[str, Any]] = None
    study: Optional[Dict[str, Any]] = None
    created_at: str


class SessionDetailResponse(BaseModel):
    id: str
    title: str
    status: str = "active"
    created_at: str
    updated_at: str
    messages: List[MessageItemResponse] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Chat Models
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    study_mode: bool = False


class ChatUserMessage(BaseModel):
    id: str
    content: str
    detected_language: Optional[str] = None


class ChatAssistantMessage(BaseModel):
    id: str
    content: str
    explanation: List[str] = Field(default_factory=list)
    example: Optional[str] = None


class ChatNLPInfo(BaseModel):
    language: str
    tone: str
    intent: str


class CodeArtifactResponse(BaseModel):
    id: str
    language: str
    filename: str
    content: str
    validation_status: str


class StudySectionResponse(BaseModel):
    problem_understanding: Optional[str] = None
    algorithm: List[str] = Field(default_factory=list)
    flowchart: Optional[str] = None
    important_points: List[str] = Field(default_factory=list)
    viva_questions: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    session_id: str
    message_id: str
    user_message: ChatUserMessage
    assistant_message: ChatAssistantMessage
    nlp: ChatNLPInfo
    code: List[CodeArtifactResponse] = Field(default_factory=list)
    study: Optional[StudySectionResponse] = None
    execution: Optional[Dict[str, Any]] = None


# ---------------------------------------------------------------------------
# Code Validate and Run Models
# ---------------------------------------------------------------------------

class CodeValidateRequest(BaseModel):
    language: str
    code: str


class CodeValidateResponse(BaseModel):
    language: str
    status: str
    is_valid: bool
    diagnostics: List[str] = Field(default_factory=list)
    line_count: int


class CodeRunRequest(BaseModel):
    language: str
    code: str
    stdin: Optional[str] = ""


class CodeRunResponse(BaseModel):
    status: str
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    duration_ms: float = 0.0
    diagnostics: List[str] = Field(default_factory=list)
