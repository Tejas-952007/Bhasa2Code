"""Health check endpoints for Bhasha2Code."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, get_llm_service, get_sandbox_runner
from backend.app.api.schemas import HealthResponse
from backend.app.database.engine import check_db_connection
from backend.app.llm.llm_service import LLMService
from backend.app.sandbox.sandbox_runner import SandboxRunner

router = APIRouter(tags=["health"])


@router.get("/health", summary="Basic health check")
async def basic_health():
    """Unversioned health check for backward compatibility."""
    return {"status": "healthy"}


@router.get("/api/v1/health", response_model=HealthResponse, summary="Comprehensive system health check")
async def system_health(
    llm_service: LLMService = Depends(get_llm_service),
    sandbox_runner: SandboxRunner = Depends(get_sandbox_runner),
    db: Session = Depends(get_db),
):
    """Detailed health check validating DB, Ollama, and Docker sandbox status."""
    db_ok = check_db_connection()
    ollama_ok = llm_service.is_available()
    sandbox_ok = sandbox_runner.is_available()

    model_name = llm_service.settings.model

    status_str = "healthy" if db_ok and ollama_ok else ("degraded" if db_ok else "unhealthy")

    return HealthResponse(
        status=status_str,
        ollama="available" if ollama_ok else "unavailable",
        model=model_name,
        sandbox="available" if sandbox_ok else "unavailable",
        database="available" if db_ok else "unavailable",
    )
