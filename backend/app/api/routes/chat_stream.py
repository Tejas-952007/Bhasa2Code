"""T23 — SSE Streaming Chat endpoint for Bhasha2Code.

Provides `POST /chat/stream` which runs the full pipeline and streams
Ollama token events to the frontend as Server-Sent Events.

Event protocol:
  data: {"type": "start",    "session_id": str, "user_message_id": str}
  data: {"type": "token",    "token": str}
  data: {"type": "complete", "session_id": str, "message_id": str,
          "user_message": {...}, "assistant_message": {...},
          "nlp": {...}, "code": [...], "study": {...} | null}
  data: {"type": "error",    "code": str, "message": str}
"""

import json
import logging
import uuid
from typing import AsyncIterator, List, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.app.api.deps import (
    get_current_user_id,
    get_llm_service,
    get_nlp_pipeline,
    get_prompt_builder,
    get_response_validator,
)
from backend.app.api.exceptions import (
    BadRequestAPIError,
    SessionNotFoundAPIError,
    UnauthorizedSessionAPIError,
)
from backend.app.api.parsers import parse_assistant_response
from backend.app.api.schemas import (
    ChatRequest,
    CodeArtifactResponse,
)
from backend.app.context.context_manager import ContextManager
from backend.app.database.engine import get_db
from backend.app.database.repositories.generated_code_repository import GeneratedCodeRepository
from backend.app.database.repositories.message_repository import MessageRepository
from backend.app.database.repositories.session_repository import SessionRepository
from backend.app.llm.exceptions import (
    OllamaModelNotFoundError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)
from backend.app.llm.llm_service import LLMService
from backend.app.nlp.pipeline.nlp_pipeline import NLPPipeline
from backend.app.prompt.prompt_builder import PromptBuilder
from backend.app.validation.response_validator import ResponseValidator

logger = logging.getLogger("bhasha2code.api.chat_stream")

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


def _sse(data: dict, event: Optional[str] = None) -> str:
    """Encode a dict as an SSE event and data line."""
    evt_name = event or data.get("type", "message")
    return f"event: {evt_name}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.post("/stream", summary="Stream chat response via Server-Sent Events")
async def stream_chat_message(
    payload: ChatRequest,
    request: Request,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
    nlp_pipeline: NLPPipeline = Depends(get_nlp_pipeline),
    prompt_builder: PromptBuilder = Depends(get_prompt_builder),
    llm_service: LLMService = Depends(get_llm_service),
    response_validator: ResponseValidator = Depends(get_response_validator),
) -> StreamingResponse:
    """Execute the full Bhasha2Code pipeline and stream tokens back to the client.

    Returns a `text/event-stream` response. Each SSE event has a `data` field
    containing a JSON object with `type` = start | token | complete | error.
    """
    raw_message = (payload.message or "").strip()
    if not raw_message:
        raise BadRequestAPIError("Message content cannot be empty.")

    session_repo = SessionRepository(db)
    msg_repo = MessageRepository(db)
    code_repo = GeneratedCodeRepository(db)

    # 1. Session resolution
    session_id = payload.session_id
    if session_id:
        existing_session = session_repo.get_by_id(session_id=session_id)
        if existing_session is None:
            raise SessionNotFoundAPIError()
        if existing_session.user_id != user_id:
            raise UnauthorizedSessionAPIError()
        session = existing_session

        # Deduplication check: if client_turn_id was already processed, return existing turn
        if payload.client_turn_id:
            existing_msgs = msg_repo.list_by_session(session_id=session_id)
            for m in existing_msgs:
                if (
                    m.role == "user"
                    and m.context_metadata
                    and m.context_metadata.get("client_turn_id") == payload.client_turn_id
                ):
                    asst_m = next(
                        (am for am in existing_msgs if am.role == "assistant" and am.created_at >= m.created_at),
                        None,
                    )
                    if asst_m:
                        logger.info("Idempotent stream hit for client_turn_id: %s", payload.client_turn_id)
                        meta = asst_m.context_metadata or {}
                        code_meta = meta.get("code_block")
                        codes = []
                        if code_meta:
                            codes.append({
                                "id": code_meta.get("id", str(uuid.uuid4())),
                                "language": code_meta.get("language", "python"),
                                "filename": code_meta.get("filename", "solution.py"),
                                "content": code_meta.get("code", ""),
                                "validation_status": code_meta.get("validationStatus", "VALID"),
                            })

                        async def dup_generator() -> AsyncIterator[str]:
                            yield _sse({
                                "type": "start",
                                "session_id": session_id,
                                "user_message_id": m.id,
                            })
                            yield _sse({
                                "type": "complete",
                                "session_id": session_id,
                                "message_id": asst_m.id,
                                "user_message": {
                                    "id": m.id,
                                    "content": m.content,
                                    "detected_language": m.detected_language,
                                },
                                "assistant_message": {
                                    "id": asst_m.id,
                                    "content": asst_m.content,
                                    "explanation": meta.get("explanation", []),
                                    "example": meta.get("example"),
                                },
                                "nlp": meta.get(
                                    "nlp",
                                    {
                                        "language": asst_m.detected_language or "ENGLISH",
                                        "tone": asst_m.tone or "CASUAL",
                                        "intent": asst_m.intent or "GENERATE_CODE",
                                    },
                                ),
                                "code": codes,
                                "study": meta.get("study"),
                            })

                        return StreamingResponse(
                            dup_generator(),
                            media_type="text/event-stream",
                            headers={
                                "Cache-Control": "no-cache",
                                "X-Accel-Buffering": "no",
                                "Connection": "keep-alive",
                            },
                        )
    else:
        snippet = raw_message[:35].strip()
        safe_title = f"{snippet}..." if len(raw_message) > 35 else snippet
        session = session_repo.create(
            user_id=user_id,
            title=safe_title or "New Chat",
            status="active",
            commit=True,
        )
        session_id = session.id

    # 2. NLP analysis
    try:
        nlp_result = nlp_pipeline.analyze(raw_message)
        detected_lang = nlp_result.detected_language
        detected_tone = nlp_result.detected_tone
        detected_intent = nlp_result.detected_intent
    except Exception as e:
        logger.warning("NLP pipeline error, using defaults: %s", e)
        nlp_result = None
        detected_lang = "ENGLISH"
        detected_tone = "CASUAL"
        detected_intent = "GENERATE_CODE"

    # 3. Persist user message
    user_msg_id = str(uuid.uuid4())
    user_context_meta = {"client_turn_id": payload.client_turn_id} if payload.client_turn_id else None
    user_msg = msg_repo.create(
        id=user_msg_id,
        session_id=session_id,
        role="user",
        content=raw_message,
        detected_language=detected_lang,
        intent=detected_intent,
        tone=detected_tone,
        context_metadata=user_context_meta,
        commit=True,
    )

    # 4. Context & Prompt
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
    prompt_spec = prompt_builder.build(
        user_message=raw_message,
        nlp_result=nlp_result,
        context_package=context_package,
        study_mode=payload.study_mode,
    )

    async def event_generator() -> AsyncIterator[str]:
        """Core SSE generator — yields string chunks directly."""
        # Emit start event immediately so the frontend shows activity
        yield _sse({
            "type": "start",
            "session_id": session_id,
            "user_message_id": user_msg_id,
        })

        full_text = ""

        try:
            async for chunk in llm_service.generate_stream(prompt_spec):
                # Check if client disconnected
                if await request.is_disconnected():
                    logger.info("Stream: client disconnected early for session %s", session_id)
                    return

                token = chunk.get("token", "")
                is_done = chunk.get("done", False)

                if token:
                    full_text += token
                    yield _sse({"type": "token", "token": token})

                if is_done:
                    break  # Fall through to post-processing

        except OllamaUnavailableError as exc:
            logger.error("Ollama unavailable during stream: %s", exc)
            yield _sse({
                "type": "error",
                "code": "OLLAMA_UNAVAILABLE",
                "message": "Local AI service is unavailable. Please check Ollama.",
            })
            return
        except OllamaModelNotFoundError as exc:
            logger.error("Model not found during stream: %s", exc)
            yield _sse({
                "type": "error",
                "code": "MODEL_NOT_FOUND",
                "message": f"Model '{exc.model_name}' is not installed in Ollama.",
            })
            return
        except OllamaTimeoutError as exc:
            logger.error("Ollama stream timed out: %s", exc)
            yield _sse({
                "type": "error",
                "code": "EXECUTION_TIMEOUT",
                "message": "Generation timed out. The model may be overloaded.",
            })
            return
        except Exception as exc:
            logger.error("Unexpected streaming error: %s", exc, exc_info=True)
            yield _sse({
                "type": "error",
                "code": "STREAM_ERROR",
                "message": "An unexpected error occurred during generation.",
            })
            return

        if not full_text.strip():
            yield _sse({
                "type": "error",
                "code": "EMPTY_RESPONSE",
                "message": "The model returned an empty response.",
            })
            return

        # 7. Post-process the accumulated full response
        lang_hint = None
        if context_package.generated_code:
            lang_hint = context_package.generated_code[0].language
        elif context_package.session_metadata:
            lang_hint = context_package.session_metadata.get("programming_language")

        validation_result = response_validator.validate(full_text, language_hint=lang_hint)
        main_prose, explanation_bullets, example_text, study_response = parse_assistant_response(
            full_text, study_mode=payload.study_mode
        )

        # 8. Build code artifacts
        code_artifacts: List[CodeArtifactResponse] = []
        primary_code_snippet: Optional[str] = None
        primary_language: Optional[str] = None
        primary_code_block_dict: Optional[dict] = None
        pending_codes = []

        assistant_msg_id = str(uuid.uuid4())

        VALID_LANGUAGES = {"python", "c", "cpp", "java", "javascript", "sql"}
        code_idx = 0
        for block in validation_result.code_blocks:
            block_lang = (block.language or lang_hint or "python").lower()
            if block_lang not in VALID_LANGUAGES:
                continue
            code_idx += 1
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

            if code_idx == 1:
                primary_code_snippet = block_code
                primary_language = block_lang
                primary_code_block_dict = {
                    "id": code_id,
                    "language": block_lang,
                    "filename": fname,
                    "code": block_code,
                    "validationStatus": val_status,
                }

        # 9. Persist assistant message
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

        session_repo.update(
            session_id=session_id,
            current_language=detected_lang,
            programming_language=primary_language,
            current_code=primary_code_snippet,
            commit=True,
        )

        # 10. Emit complete event with full structured payload
        study_dict = study_response.model_dump() if study_response else None
        code_list = [
            {
                "id": a.id,
                "language": a.language,
                "filename": a.filename,
                "content": a.content,
                "validation_status": a.validation_status,
            }
            for a in code_artifacts
        ]

        yield _sse({
            "type": "complete",
            "session_id": session_id,
            "message_id": assistant_msg_id,
            "user_message": {
                "id": user_msg.id,
                "content": user_msg.content,
                "detected_language": user_msg.detected_language,
            },
            "assistant_message": {
                "id": assistant_msg_id,
                "content": main_prose,
                "explanation": explanation_bullets,
                "example": example_text,
            },
            "nlp": {
                "language": detected_lang,
                "tone": detected_tone,
                "intent": detected_intent,
            },
            "code": code_list,
            "study": study_dict,
        })

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
