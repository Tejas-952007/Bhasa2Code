"""Context Manager for Bhasha2Code.

Provides multi-turn conversational memory for the coding assistant by retrieving
and organizing relevant previous session messages, generated code, and current context.
"""

import logging
from typing import List, Optional, Union

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
from backend.app.database.models import GeneratedCode, Message, Session
from backend.app.database.repositories import (
    GeneratedCodeRepository,
    MessageRepository,
    SessionRepository,
)
from backend.app.nlp.schemas import NLPPipelineResult

logger = logging.getLogger(__name__)


class ContextManager:
    """Manages conversational context retrieval, isolation, windowing, and packaging."""

    def __init__(
        self,
        session_repository: SessionRepository,
        message_repository: MessageRepository,
        generated_code_repository: GeneratedCodeRepository,
        default_policy: Optional[ContextPolicy] = None,
    ) -> None:
        self.session_repo = session_repository
        self.message_repo = message_repository
        self.code_repo = generated_code_repository
        self.default_policy = default_policy or ContextPolicy()

    def build_context(
        self,
        user_id: Union[str, int],
        session_id: Union[str, int],
        current_message: str,
        nlp_result: Optional[NLPPipelineResult] = None,
        policy: Optional[ContextPolicy] = None,
    ) -> ContextPackage:
        """Retrieve, filter, and package session context for the current turn.

        Args:
            user_id: The ID of the authenticated user requesting context.
            session_id: The ID of the conversation session.
            current_message: The raw or normalized user message for the current turn.
            nlp_result: Optional T14 unified NLP Pipeline analysis result.
            policy: Optional custom ContextPolicy overriding default window budgets.

        Returns:
            ContextPackage: Structured context object containing chronological messages,
                relevant generated code, metadata, and truncation flags.

        Raises:
            ValueError: If user_id, session_id, or current_message is missing or invalid.
            SessionNotFoundError: If the session does not exist.
            UnauthorizedSessionError: If the user does not own the session.
            ContextError: For other domain-specific failures.
        """
        # 1. Parameter Validation
        if user_id is None or (isinstance(user_id, str) and not user_id.strip()):
            raise ValueError("user_id is required and cannot be empty.")
        if session_id is None or (isinstance(session_id, str) and not session_id.strip()):
            raise ValueError("session_id is required and cannot be empty.")
        if current_message is None:
            raise ValueError("current_message is required and cannot be None.")

        user_id_str = str(user_id).strip()
        session_id_str = str(session_id).strip()
        active_policy = policy or self.default_policy

        logger.debug(
            "Initiating context build for user_id=%s, session_id=%s",
            user_id_str,
            session_id_str,
        )

        # 2. Strict Session Ownership Verification
        session = self.session_repo.get_by_id(session_id_str)
        if session is None:
            raise SessionNotFoundError(f"Session '{session_id_str}' not found.")
        if str(session.user_id) != user_id_str:
            raise UnauthorizedSessionError(
                f"User '{user_id_str}' is not authorized to access session '{session_id_str}'."
            )

        # 3. Follow-Up Detection
        follow_up = is_follow_up(current_message, nlp_result)
        budget_max_messages = (
            active_policy.max_messages
            if follow_up
            else min(active_policy.standalone_max_messages, active_policy.max_messages)
        )

        truncated = False

        # 4. Message Retrieval & Chronological Windowing
        total_messages_count = self.message_repo.count_by_session(session_id_str)
        context_messages: List[ContextMessage] = []

        if total_messages_count > 0:
            if total_messages_count > budget_max_messages:
                offset = total_messages_count - budget_max_messages
                db_messages = self.message_repo.list_by_session(
                    session_id=session_id_str,
                    limit=budget_max_messages,
                    offset=offset,
                )
                if total_messages_count > active_policy.max_messages:
                    truncated = True
            else:
                db_messages = self.message_repo.list_by_session(
                    session_id=session_id_str,
                    limit=budget_max_messages,
                    offset=0,
                )

            # Convert to schema instances
            for msg in db_messages:
                context_messages.append(
                    ContextMessage(
                        message_id=str(msg.id),
                        role=msg.role,
                        content=msg.content,
                        created_at=msg.created_at.isoformat() if msg.created_at else None,
                        relevance="recent",
                    )
                )

            # Filter out the active user message if it was already persisted to DB before build_context
            if context_messages and context_messages[-1].content == current_message and context_messages[-1].role == "user":
                context_messages.pop()

            # Character budget enforcement (drop oldest low-priority messages first)
            total_msg_chars = sum(len(m.content) for m in context_messages)
            while total_msg_chars > active_policy.max_characters and len(context_messages) > 1:
                dropped = context_messages.pop(0)
                total_msg_chars -= len(dropped.content)
                truncated = True

        # 5. Generated Code Retrieval (Only retained when request is a follow-up to prior code)
        context_codes: List[ContextCode] = []
        if follow_up:
            raw_code_list = self.code_repo.list_code_by_session(
                session_id=session_id_str,
                limit=active_policy.max_generated_code_items + 1,
            )

            if len(raw_code_list) > active_policy.max_generated_code_items:
                truncated = True
                raw_code_list = raw_code_list[: active_policy.max_generated_code_items]

            # Enforce code character budget
            total_code_chars = sum(len(c.code or "") for c in raw_code_list)
            while total_code_chars > active_policy.max_code_characters and len(raw_code_list) > 1:
                dropped_code = raw_code_list.pop()
                total_code_chars -= len(dropped_code.code or "")
                truncated = True

            for code_record in raw_code_list:
                try:
                    code_text = code_record.code or ""
                    # Single artifact truncation if individual snippet exceeds budget
                    if len(code_text) > active_policy.max_code_characters:
                        code_text = (
                            code_text[: active_policy.max_code_characters]
                            + "\n# ... [truncated to fit context budget] ..."
                        )
                        truncated = True

                    context_codes.append(
                        ContextCode(
                            generated_code_id=str(code_record.id),
                            message_id=str(code_record.message_id) if code_record.message_id else None,
                            language=code_record.language,
                            code=code_text,
                            validation_status=code_record.validation_status,
                        )
                    )
                except Exception as ex:
                    logger.warning(
                        "Skipping malformed generated code record %s: %s",
                        getattr(code_record, "id", "unknown"),
                        ex,
                    )

        # 6. Current Code Segment Extraction
        current_code: Optional[str] = None
        if nlp_result is not None and nlp_result.preprocessed_text.code_segments:
            current_code = "\n\n".join(
                seg.content for seg in nlp_result.preprocessed_text.code_segments if seg.content
            )
        elif follow_up and session.current_code:
            current_code = session.current_code

        # 7. Metadata Assembly
        metadata: Optional[ContextMetadata] = None
        if nlp_result is not None:
            metadata = ContextMetadata(
                language=nlp_result.detected_language,
                tone=nlp_result.detected_tone,
                intent=nlp_result.detected_intent,
                is_follow_up=follow_up,
                confidence_scores={
                    "language": round(nlp_result.language.confidence, 4),
                    "tone": round(nlp_result.tone.confidence, 4),
                    "intent": round(nlp_result.intent.confidence, 4),
                },
            )
        else:
            metadata = ContextMetadata(
                language=None,
                tone=None,
                intent=None,
                is_follow_up=follow_up,
                confidence_scores={},
            )

        # 8. Session Metadata
        session_metadata = {
            "session_id": str(session.id),
            "title": session.title,
            "status": session.status,
            "programming_language": session.programming_language,
            "current_language": session.current_language,
            "created_at": session.created_at.isoformat() if session.created_at else None,
            "updated_at": session.updated_at.isoformat() if session.updated_at else None,
        }

        # 9. Final Context Package
        package = ContextPackage(
            session_id=session_id_str,
            user_id=user_id_str,
            current_message=current_message,
            current_code=current_code,
            messages=context_messages,
            generated_code=context_codes,
            metadata=metadata,
            session_metadata=session_metadata,
            total_messages=total_messages_count,
            truncated=truncated,
        )

        logger.debug(
            "ContextPackage created: session_id=%s, messages_retained=%d, codes_retained=%d, truncated=%s",
            session_id_str,
            len(context_messages),
            len(context_codes),
            truncated,
        )

        return package
