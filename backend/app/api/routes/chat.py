"""Chat API endpoint coordinating NLP, Context, Prompt, Ollama, Validation, and Persistence."""

import logging
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.deps import (
    get_current_user_id,
    get_llm_service,
    get_nlp_pipeline,
    get_prompt_builder,
    get_response_validator,
)
from backend.app.api.exceptions import (
    APIException,
    BadRequestAPIError,
    OllamaModelNotFoundAPIError,
    OllamaUnavailableAPIError,
    SessionNotFoundAPIError,
    UnauthorizedSessionAPIError,
)
from backend.app.api.parsers import parse_assistant_response
from backend.app.api.schemas import (
    ChatAssistantMessage,
    ChatNLPInfo,
    ChatRequest,
    ChatResponse,
    ChatUserMessage,
    CodeArtifactResponse,
)
from backend.app.context.context_manager import ContextManager
from backend.app.database.engine import get_db
from backend.app.database.repositories.generated_code_repository import (
    GeneratedCodeRepository,
)
from backend.app.database.repositories.message_repository import MessageRepository
from backend.app.database.repositories.session_repository import SessionRepository
from backend.app.llm.exceptions import (
    OllamaError,
    OllamaModelNotFoundError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)
from backend.app.llm.llm_service import LLMService
from backend.app.nlp.pipeline.nlp_pipeline import NLPPipeline
from backend.app.prompt.prompt_builder import PromptBuilder
from backend.app.validation.response_validator import ResponseValidator

logger = logging.getLogger("bhasha2code.api.chat")

router = APIRouter(prefix="/chat", tags=["chat"])

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
    return f"solution.{ext}"


@router.post("", response_model=ChatResponse, summary="Send message and generate code response")
def send_chat_message(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
    nlp_pipeline: NLPPipeline = Depends(get_nlp_pipeline),
    prompt_builder: PromptBuilder = Depends(get_prompt_builder),
    llm_service: LLMService = Depends(get_llm_service),
    response_validator: ResponseValidator = Depends(get_response_validator),
) -> ChatResponse:
    """Execute end-to-end Bhasha2Code pipeline for user message."""
    raw_message = (payload.message or "").strip()
    if not raw_message:
        raise BadRequestAPIError("Message content cannot be empty.")

    session_repo = SessionRepository(db)
    msg_repo = MessageRepository(db)
    code_repo = GeneratedCodeRepository(db)

    # 1. Session Resolution or Creation
    session_id = payload.session_id
    if session_id:
        existing_session = session_repo.get_by_id(session_id=session_id)
        if existing_session is None:
            raise SessionNotFoundAPIError()
        if existing_session.user_id != user_id:
            raise UnauthorizedSessionAPIError()
        session = existing_session
    else:
        # Create safe title from prompt snippet
        snippet = raw_message[:35].strip()
        safe_title = f"{snippet}..." if len(raw_message) > 35 else snippet
        session = session_repo.create(
            user_id=user_id,
            title=safe_title or "New Chat",
            status="active",
            commit=True,
        )
        session_id = session.id

    # 2. T14 NLP Pipeline Analysis
    try:
        nlp_result = nlp_pipeline.process(raw_message)
        detected_lang = nlp_result.language.primary_language.name
        detected_tone = nlp_result.tone.primary_tone.name
        detected_intent = nlp_result.intent.primary_intent.name
    except Exception as e:
        logger.warning("NLP pipeline encountered error, defaulting attributes: %s", e)
        nlp_result = None
        detected_lang = "ENGLISH"
        detected_tone = "CASUAL"
        detected_intent = "GENERATE_CODE"

    # 3. Persist User Message
    user_msg_id = str(uuid.uuid4())
    user_msg = msg_repo.create(
        id=user_msg_id,
        session_id=session_id,
        role="user",
        content=raw_message,
        detected_language=detected_lang,
        intent=detected_intent,
        tone=detected_tone,
        commit=True,
    )

    # 4. T15 Context Manager Multi-Turn Assembly
    context_mgr = ContextManager(
        session_repository=session_repo,
        message_repository=msg_repo,
        generated_code_repository=code_repo,
    )
    context_package = context_mgr.build_context(
        user_id=user_id,
        session_id=session_id,
        current_message=raw_message,
        nlp_result=nlp_result,
    )

    # 5. T16 Prompt Builder Specification
    prompt_spec = prompt_builder.build(
        user_message=raw_message,
        nlp_result=nlp_result,
        context_package=context_package,
        study_mode=payload.study_mode,
    )

    # 6. T17 Local Ollama Generation
    try:
        llm_response = llm_service.generate(prompt_spec)
        response_text = llm_response.text
    except OllamaUnavailableError as e:
        logger.error("Ollama service unavailable: %s", e)
        raise OllamaUnavailableAPIError(
            "The local model could not respond. Please check Ollama and try again."
        )
    except OllamaModelNotFoundError as e:
        logger.error("Model not found in Ollama: %s", e)
        raise OllamaModelNotFoundAPIError(model_name=e.model_name)
    except OllamaTimeoutError as e:
        logger.error("Ollama generation timed out: %s", e)
        raise APIException(
            code="EXECUTION_TIMEOUT",
            message="Local model response timed out. Please try again.",
            status_code=504,
        )
    except OllamaError as e:
        logger.error("Ollama general error: %s", e)
        raise APIException(
            code="OLLAMA_UNAVAILABLE",
            message="The local model encountered an error. Please check Ollama.",
            status_code=503,
        )

    # 7. T18 Response Validation
    lang_hint = None
    if context_package.generated_code:
        lang_hint = context_package.generated_code[0].language
    elif context_package.session_metadata:
        lang_hint = context_package.session_metadata.get("programming_language")
    validation_result = response_validator.validate(response_text, language_hint=lang_hint)

    # 8. Parse Sections (Explanation, Example, Study Sections)
    main_prose, explanation_bullets, example_text, study_response = parse_assistant_response(
        response_text, study_mode=payload.study_mode
    )

    # 9. Extract Code Artifacts & Metadata
    code_artifacts: List[CodeArtifactResponse] = []
    primary_code_snippet: Optional[str] = None
    primary_language: Optional[str] = None
    primary_code_block_dict: Optional[dict] = None
    pending_codes = []

    assistant_msg_id = str(uuid.uuid4())

    for idx, block in enumerate(validation_result.code_blocks, 1):
        block_lang = block.language or lang_hint or "python"
        block_code = block.code
        val_status = block.status.value.upper()

        code_id = str(uuid.uuid4())
        fname = _get_filename(block_lang)

        pending_codes.append((code_id, block_code, block_lang, val_status.lower()))

        artifact_resp = CodeArtifactResponse(
            id=code_id,
            language=block_lang,
            filename=fname,
            content=block_code,
            validation_status=val_status,
        )
        code_artifacts.append(artifact_resp)

        if idx == 1:
            primary_code_snippet = block_code
            primary_language = block_lang
            primary_code_block_dict = {
                "id": code_id,
                "language": block_lang,
                "filename": fname,
                "code": block_code,
                "validationStatus": val_status,
            }

    # 10. Persist Assistant Message First (FK parent)
    context_meta = {
        "explanation": explanation_bullets,
        "example": example_text,
        "code_block": primary_code_block_dict,
        "study": study_response.model_dump() if study_response else None,
        "nlp": {
            "language": detected_lang,
            "tone": detected_tone,
            "intent": detected_intent,
        },
    }

    msg_repo.create(
        id=assistant_msg_id,
        session_id=session_id,
        role="assistant",
        content=main_prose,
        detected_language=detected_lang,
        intent=detected_intent,
        tone=detected_tone,
        programming_language=primary_language,
        context_metadata=context_meta,
        commit=True,
    )

    # 11. Persist Generated Code Artifacts (FK child referencing assistant_msg_id)
    for c_id, c_code, c_lang, c_status in pending_codes:
        code_repo.create(
            id=c_id,
            session_id=session_id,
            message_id=assistant_msg_id,
            code=c_code,
            language=c_lang,
            validation_status=c_status,
            commit=True,
        )

    # 11. Update Session Context State
    session_repo.update(
        session_id=session_id,
        current_language=detected_lang,
        programming_language=primary_language,
        current_code=primary_code_snippet,
        commit=True,
    )

    # 12. Build and Return Structured ChatResponse
    return ChatResponse(
        session_id=session_id,
        message_id=assistant_msg_id,
        user_message=ChatUserMessage(
            id=user_msg.id,
            content=user_msg.content,
            detected_language=user_msg.detected_language,
        ),
        assistant_message=ChatAssistantMessage(
            id=assistant_msg_id,
            content=main_prose,
            explanation=explanation_bullets,
            example=example_text,
        ),
        nlp=ChatNLPInfo(
            language=detected_lang,
            tone=detected_tone,
            intent=detected_intent,
        ),
        code=code_artifacts,
        study=study_response,
        execution=None,
    )
