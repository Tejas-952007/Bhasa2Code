"""FastAPI route dependencies and singleton service providers."""

import logging
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.database.engine import get_db
from backend.app.database.repositories.user_repository import UserRepository
from backend.app.llm.llm_service import LLMService
from backend.app.nlp.pipeline.nlp_pipeline import NLPPipeline
from backend.app.prompt.prompt_builder import PromptBuilder
from backend.app.sandbox.sandbox_runner import SandboxRunner
from backend.app.validation.response_validator import ResponseValidator

logger = logging.getLogger("bhasha2code.api.deps")

# Global instances initialized on-demand
_nlp_pipeline: NLPPipeline | None = None
_prompt_builder: PromptBuilder | None = None
_llm_service: LLMService | None = None
_response_validator: ResponseValidator | None = None
_sandbox_runner: SandboxRunner | None = None


def get_current_user_id(db: Session = Depends(get_db)) -> str:
    """Ensure local default user row exists and return its user_id."""
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(settings.DEFAULT_USER_ID)
    if user is None:
        try:
            user = user_repo.create(
                id=settings.DEFAULT_USER_ID,
                name=settings.DEFAULT_USER_NAME,
                commit=True,
            )
        except Exception:
            # If created concurrently
            db.rollback()
            user = user_repo.get_by_id(settings.DEFAULT_USER_ID)

    return settings.DEFAULT_USER_ID


def get_nlp_pipeline() -> NLPPipeline:
    global _nlp_pipeline
    if _nlp_pipeline is None:
        _nlp_pipeline = NLPPipeline()
    return _nlp_pipeline


def get_prompt_builder() -> PromptBuilder:
    global _prompt_builder
    if _prompt_builder is None:
        _prompt_builder = PromptBuilder()
    return _prompt_builder


def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service


def get_response_validator() -> ResponseValidator:
    global _response_validator
    if _response_validator is None:
        _response_validator = ResponseValidator()
    return _response_validator


def get_sandbox_runner() -> SandboxRunner:
    global _sandbox_runner
    if _sandbox_runner is None:
        _sandbox_runner = SandboxRunner()
    return _sandbox_runner
