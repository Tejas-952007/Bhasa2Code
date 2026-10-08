"""Prompt Builder for Bhasha2Code.

Orchestrates multi-turn context, NLP classifications, Study Mode policies,
and explicit user formatting constraints into a structured PromptSpecification.
"""

from typing import List, Optional

from backend.app.context.schemas import ContextPackage
from backend.app.nlp.schemas import NLPPipelineResult
from backend.app.prompt.format_rules import (
    ExplicitFormatRequirements,
    detect_explicit_format_requirements,
    select_response_sections,
)
from backend.app.prompt.policies import (
    IntentPolicy,
    LanguagePolicy,
    SecurityPolicy,
    TonePolicy,
)
from backend.app.prompt.schemas import PromptSpecification


class PromptBuilder:
    """Builds structured prompt specifications for local LLM inference."""

    def __init__(self) -> None:
        pass

    def build(
        self,
        user_message: str,
        nlp_result: Optional[NLPPipelineResult] = None,
        context_package: Optional[ContextPackage] = None,
        study_mode: bool = False,
    ) -> PromptSpecification:
        """Construct a PromptSpecification orchestrating all operational and stylistic policies.

        Args:
            user_message: Current user message prompt.
            nlp_result: Optional T14 unified NLP Pipeline classification result.
            context_package: Optional T15 ContextPackage with multi-turn history & code artifacts.
            study_mode: Boolean indicating whether Study Mode is enabled.

        Returns:
            PromptSpecification: Structured prompt object ready for rendering or model dispatch.

        Raises:
            ValueError: If user_message is None.
        """
        if user_message is None:
            raise ValueError("user_message cannot be None.")

        user_text = str(user_message).strip()

        # 1. Resolve Linguistic & Behavioral Attributes from NLP / Context
        detected_lang = "ENGLISH"
        detected_tone = "CASUAL"
        detected_intent = "GENERATE_CODE"

        if nlp_result is not None:
            detected_lang = nlp_result.detected_language
            detected_tone = nlp_result.detected_tone
            detected_intent = nlp_result.detected_intent
        elif context_package is not None and context_package.metadata is not None:
            if context_package.metadata.language:
                detected_lang = context_package.metadata.language
            if context_package.metadata.tone:
                detected_tone = context_package.metadata.tone
            if context_package.metadata.intent:
                detected_intent = context_package.metadata.intent

        # 2. Extract Explicit Format Constraints from User Text
        explicit_req = detect_explicit_format_requirements(user_text)

        # Check follow-up status and previous code presence from context
        is_follow_up = False
        has_previous_code = False
        if context_package is not None:
            if context_package.metadata and context_package.metadata.is_follow_up:
                is_follow_up = True
            if context_package.generated_code or context_package.current_code:
                has_previous_code = True

        # 3. Plan Response Sections Dynamically
        response_sections = select_response_sections(
            intent=detected_intent,
            tone=detected_tone,
            study_mode=study_mode,
            explicit_requirements=explicit_req,
            is_follow_up=is_follow_up,
            has_previous_code=has_previous_code,
        )

        # 4. Formulate Policy Instructions
        system_instruction = (
            f"{SecurityPolicy.SYSTEM_INSTRUCTION}\n\n"
            f"{SecurityPolicy.HIERARCHY_STATEMENT}\n\n"
            f"{SecurityPolicy.INJECTION_DEFENSE}\n\n"
            f"{SecurityPolicy.CODE_PRESERVATION}"
        )
        language_instruction = LanguagePolicy.get_instruction(detected_lang)
        tone_instruction = TonePolicy.get_instruction(detected_tone)
        intent_instruction = IntentPolicy.get_instruction(detected_intent)

        # 5. Extract Explicit Constraints List
        explicit_constraints: List[str] = []
        if explicit_req.code_only:
            explicit_constraints.append(
                "USER DEMAND: Output ONLY raw executable code. Do NOT output any introductory text, explanation, or commentary."
            )
        if explicit_req.algorithm:
            explicit_constraints.append("Include explicit algorithmic logic and steps.")
        if explicit_req.flowchart:
            explicit_constraints.append("Include an ASCII/text-based flowchart illustrating control flow.")
        if explicit_req.viva_questions:
            explicit_constraints.append("Include viva/interview questions testing understanding.")
        if explicit_req.line_by_line:
            explicit_constraints.append("Provide a line-by-line breakdown explaining what each key line accomplishes.")
        if explicit_req.step_by_step:
            explicit_constraints.append("Provide a step-by-step procedure.")
        if explicit_req.example or explicit_req.output:
            explicit_constraints.append("Include concrete sample input and corresponding expected output.")
        if explicit_req.table:
            explicit_constraints.append("Format key comparisons in a clean markdown table.")
        if explicit_req.short:
            explicit_constraints.append("Keep response extremely brief and concise.")
        if explicit_req.detailed:
            explicit_constraints.append("Provide a thorough, comprehensive, and detailed walkthrough.")

        # 6. Assemble Context Text and Code Continuity
        context_parts: List[str] = []
        current_code: Optional[str] = None
        is_follow_up = False

        if context_package is not None:
            if context_package.metadata and context_package.metadata.is_follow_up:
                is_follow_up = True
                context_parts.append(
                    "[FOLLOW-UP DIRECTIVE: The user request modifies or builds on previous turns. "
                    "You MUST modify, update, or reference the active code artifact rather than starting from scratch.]"
                )

            # Historical messages
            if context_package.messages:
                context_parts.append("--- PREVIOUS CONVERSATION TURNS ---")
                for msg in context_package.messages:
                    context_parts.append(f"{msg.role.upper()}: {msg.content}")

            # Generated code artifacts
            if context_package.generated_code:
                context_parts.append("--- PREVIOUSLY GENERATED CODE ARTIFACTS ---")
                for c in context_package.generated_code:
                    c_lang = c.language or "code"
                    context_parts.append(
                        f"[CODE ARTIFACT (id: {c.generated_code_id}, lang: {c_lang})]:\n"
                        f"```{c_lang}\n{c.code}\n```"
                    )

            if context_package.current_code:
                current_code = context_package.current_code

        # Fallback for current code if extracted during text preprocessing
        if not current_code and nlp_result is not None and nlp_result.preprocessed_text.code_segments:
            current_code = "\n\n".join(
                seg.content for seg in nlp_result.preprocessed_text.code_segments if seg.content
            )

        context_text = "\n\n".join(context_parts) if context_parts else "No prior conversation history."

        # 7. Package into PromptSpecification
        return PromptSpecification(
            system_instruction=system_instruction,
            user_instruction=user_text,
            language_instruction=language_instruction,
            tone_instruction=tone_instruction,
            intent_instruction=intent_instruction,
            response_sections=response_sections,
            context_text=context_text,
            current_code=current_code,
            study_mode=study_mode,
            explicit_constraints=explicit_constraints,
            metadata={
                "detected_language": detected_lang,
                "detected_tone": detected_tone,
                "detected_intent": detected_intent,
                "study_mode": study_mode,
                "is_follow_up": is_follow_up,
                "explicit_format_matched": explicit_req.matched_patterns,
            },
        )
