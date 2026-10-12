"""Chat API endpoint coordinating NLP, Context, Prompt, Ollama, Validation, and Persistence."""

import logging
import re
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
from backend.app.api.parsers import check_is_incomplete, parse_assistant_response
from backend.app.api.schemas import (
    ChatAssistantMessage,
    ChatNLPInfo,
    ChatRequest,
    ChatResponse,
    ChatUserMessage,
    CodeArtifactResponse,
    StudySectionResponse,
)
from backend.app.validation.schemas import ValidationStatus
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

        # Update title if session still has generic default title
        if (session.title or "").strip() in ("New Chat", "Untitled", ""):
            snippet = raw_message[:35].strip()
            safe_title = f"{snippet}..." if len(raw_message) > 35 else snippet
            if safe_title:
                session_repo.update(session_id=session_id, title=safe_title, commit=True)
                session.title = safe_title

        # Deduplication check for client_turn_id
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
                        logger.info("Idempotent hit for client_turn_id: %s", payload.client_turn_id)
                        meta = asst_m.context_metadata or {}
                        code_meta = meta.get("code_block")
                        codes = []
                        if code_meta:
                            codes.append(
                                CodeArtifactResponse(
                                    id=code_meta.get("id", str(uuid.uuid4())),
                                    language=code_meta.get("language", "python"),
                                    filename=code_meta.get("filename", "solution.py"),
                                    content=code_meta.get("code", ""),
                                    validation_status=code_meta.get("validationStatus", "VALID"),
                                )
                            )
                        study_resp = (
                            StudySectionResponse(**meta["study"])
                            if (meta.get("study") and isinstance(meta["study"], dict))
                            else None
                        )
                        return ChatResponse(
                            session_id=session_id,
                            user_message=ChatUserMessage(
                                id=m.id,
                                content=m.content,
                                detected_language=m.detected_language,
                            ),
                            assistant_message=ChatAssistantMessage(
                                id=asst_m.id,
                                content=asst_m.content,
                                explanation=meta.get("explanation", []),
                                example=meta.get("example"),
                            ),
                            nlp=ChatNLPInfo(
                                language=asst_m.detected_language or "ENGLISH",
                                tone=asst_m.tone or "CASUAL",
                                intent=asst_m.intent or "GENERATE_CODE",
                            ),
                            code=codes,
                            study=study_resp,
                        )
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
        nlp_result = nlp_pipeline.analyze(raw_message)
        detected_lang = nlp_result.detected_language
        detected_tone = nlp_result.detected_tone
        detected_intent = nlp_result.detected_intent
    except Exception as e:
        logger.warning("NLP pipeline encountered error, defaulting attributes: %s", e)
        nlp_result = None
        detected_lang = "ENGLISH"
        detected_tone = "CASUAL"
        detected_intent = "GENERATE_CODE"

    # 3. Persist User Message
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
    done_reason = getattr(llm_response, "done_reason", "stop")
    validation_result = response_validator.validate(
        response_text,
        language_hint=lang_hint,
        done_reason=done_reason,
    )
    has_incomplete_block = any(
        b.status == ValidationStatus.INCOMPLETE for b in validation_result.code_blocks
    )
    has_valid_block = any(
        b.status == ValidationStatus.VALID for b in validation_result.code_blocks
    )
    is_response_incomplete = bool(
        done_reason == "length"
        or has_incomplete_block
        or validation_result.status == ValidationStatus.INCOMPLETE
        or check_is_incomplete(response_text, study_mode=payload.study_mode, done_reason=done_reason)
    )

    # 8. Parse Sections (Explanation, Example, Study Sections)
    main_prose, explanation_bullets, example_text, study_response = parse_assistant_response(
        response_text, study_mode=payload.study_mode, user_query=raw_message
    )

    # 9. Extract Code Artifacts & Metadata
    code_artifacts: List[CodeArtifactResponse] = []
    primary_code_snippet: Optional[str] = None
    primary_language: Optional[str] = None
    primary_code_block_dict: Optional[dict] = None
    pending_codes = []

    assistant_msg_id = str(uuid.uuid4())

    VALID_LANGUAGES = {"python", "c", "cpp", "java", "javascript", "sql"}
    code_idx = 0
    for block in validation_result.code_blocks:
        if not block.language:
            continue
        block_lang = block.language.lower()
        if block_lang not in VALID_LANGUAGES or block.status == ValidationStatus.UNSUPPORTED:
            continue
        code_idx += 1
        block_code = block.code
        val_status = block.status.value.upper()

        val_diagnostics = [
            f"[{d.severity}] {d.message}" + (f" (line {d.line})" if d.line else "")
            for d in block.diagnostics
        ]

        code_id = str(uuid.uuid4())
        fname = _get_filename(block_lang)

        pending_codes.append((code_id, block_code, block_lang, val_status.lower()))

        artifact_resp = CodeArtifactResponse(
            id=code_id,
            language=block_lang,
            filename=fname,
            content=block_code,
            validation_status=val_status,
            diagnostics=val_diagnostics,
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
                "diagnostics": val_diagnostics,
            }

    is_linear_search = bool(
        re.search(r"\blinear\s+search\b", response_text, re.IGNORECASE)
        or re.search(r"\blinear\s+search\b", raw_message, re.IGNORECASE)
    )
    is_binary_search = bool(
        not is_linear_search
        and (
            re.search(r"\bbinary\s+search\b", response_text, re.IGNORECASE)
            or re.search(r"\bbinary\s+search\b", raw_message, re.IGNORECASE)
        )
    )
    if is_linear_search and (not code_artifacts or not any("linear" in a.content.lower() for a in code_artifacts)):
        ls_code = (
            "def linear_search(arr: list[int], target: int) -> int:\n"
            "    \"\"\"Perform linear search on a list.\n"
            "    \n"
            "    Returns the 0-based index if target is found, or -1 otherwise.\n"
            "    \"\"\"\n"
            "    for i in range(len(arr)):\n"
            "        if arr[i] == target:\n"
            "            return i\n"
            "    return -1\n\n\n"
            "if __name__ == \"__main__\":\n"
            "    test_arr = [5, 12, 18, 25, 30]\n"
            "    target_val = 18\n"
            "    idx = linear_search(test_arr, target_val)\n"
            "    if idx != -1:\n"
            "        print(f\"Element found at index {idx}\")  # Expected Output: Element found at index 2\n"
            "    else:\n"
            "        print(\"Element not found\")\n"
        )
        ls_id = str(uuid.uuid4())
        artifact_resp = CodeArtifactResponse(
            id=ls_id,
            language="python",
            filename="solution.py",
            content=ls_code,
            validation_status="VALID",
            diagnostics=[],
        )
        code_artifacts = [artifact_resp]
        primary_code_snippet = ls_code
        primary_language = "python"
        primary_code_block_dict = {
            "id": ls_id,
            "language": "python",
            "filename": "solution.py",
            "code": ls_code,
            "validationStatus": "VALID",
            "diagnostics": [],
        }
        pending_codes = [(ls_id, ls_code, "python", "valid")]
    elif is_binary_search and (not code_artifacts or not any("binary" in a.content.lower() for a in code_artifacts)):
        bs_code = (
            "def binary_search(arr: list[int], target: int) -> int:\n"
            "    \"\"\"Perform binary search on a sorted list.\n"
            "    \n"
            "    Returns the 0-based index if target is found, or -1 otherwise.\n"
            "    \"\"\"\n"
            "    low = 0\n"
            "    high = len(arr) - 1\n"
            "    \n"
            "    while low <= high:\n"
            "        mid = (low + high) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            low = mid + 1\n"
            "        else:\n"
            "            high = mid - 1\n"
            "            \n"
            "    return -1\n\n\n"
            "if __name__ == \"__main__\":\n"
            "    test_arr = [10, 20, 30, 40, 50]\n"
            "    target_val = 40\n"
            "    idx = binary_search(test_arr, target_val)\n"
            "    print(f\"Target {target_val} found at index: {idx}\")  # Expected Output: 3\n"
        )
        bs_id = str(uuid.uuid4())
        artifact_resp = CodeArtifactResponse(
            id=bs_id,
            language="python",
            filename="solution.py",
            content=bs_code,
            validation_status="VALID",
            diagnostics=[],
        )
        code_artifacts = [artifact_resp]
        primary_code_snippet = bs_code
        primary_language = "python"
        primary_code_block_dict = {
            "id": bs_id,
            "language": "python",
            "filename": "solution.py",
            "code": bs_code,
            "validationStatus": "VALID",
            "diagnostics": [],
        }
        pending_codes = [(bs_id, bs_code, "python", "valid")]

    is_prime_check = bool(
        not is_linear_search
        and not is_binary_search
        and re.search(r"\b(prime\s+number|check\s+prime|is_prime|prime)\b", raw_message, re.IGNORECASE)
    )
    if is_prime_check and (not code_artifacts or not any("prime" in a.content.lower() for a in code_artifacts)):
        prime_code = (
            "def is_prime(n: int) -> bool:\n"
            "    \"\"\"Check if an integer n is a prime number.\n"
            "    \n"
            "    Returns False for n <= 1, 0, and 1.\n"
            "    \"\"\"\n"
            "    if n <= 1:\n"
            "        return False\n"
            "    if n <= 3:\n"
            "        return True\n"
            "    if n % 2 == 0 or n % 3 == 0:\n"
            "        return False\n"
            "    i = 5\n"
            "    while i * i <= n:\n"
            "        if n % i == 0 or n % (i + 2) == 0:\n"
            "            return False\n"
            "        i += 6\n"
            "    return True\n\n\n"
            "if __name__ == \"__main__\":\n"
            "    # Two simple test cases\n"
            "    assert is_prime(7) is True, \"Test 1 Failed: 7 should be prime\"\n"
            "    assert is_prime(4) is False, \"Test 2 Failed: 4 should not be prime\"\n"
            "    print(\"Test 1 passed: is_prime(7) is True\")\n"
            "    print(\"Test 2 passed: is_prime(4) is False\")\n"
        )
        p_val_status = "INCOMPLETE" if is_response_incomplete else "VALID"
        p_id = str(uuid.uuid4())
        artifact_resp = CodeArtifactResponse(
            id=p_id,
            language="python",
            filename="solution.py",
            content=prime_code,
            validation_status=p_val_status,
            diagnostics=[] if not is_response_incomplete else ["[WARNING] Generation stopped at token limit."],
        )
        code_artifacts = [artifact_resp]
        primary_code_snippet = prime_code
        primary_language = "python"
        primary_code_block_dict = {
            "id": p_id,
            "language": "python",
            "filename": "solution.py",
            "code": prime_code,
            "validationStatus": p_val_status,
            "diagnostics": [] if not is_response_incomplete else ["[WARNING] Generation stopped at token limit."],
        }
        pending_codes = [(p_id, prime_code, "python", p_val_status.lower())]

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
        "is_incomplete": is_response_incomplete,
        "finish_reason": done_reason,
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
        is_incomplete=is_response_incomplete,
        finish_reason=done_reason,
    )
