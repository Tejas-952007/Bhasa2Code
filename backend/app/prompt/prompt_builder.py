"""Prompt Builder for Bhasha2Code.

Orchestrates multi-turn context, NLP classifications, Study Mode policies,
and explicit user formatting constraints into a structured PromptSpecification.
"""

import re
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
    MLPolicy,
    SecurityPolicy,
    TonePolicy,
)
from backend.app.prompt.schemas import PromptSpecification


def extract_concept_subject(query: str) -> Optional[str]:
    """Isolate the target library/concept name from conversational request phrasing."""
    cleaned = query.strip()
    # Remove conversational polite prefixes and question openers
    cleaned = re.sub(r'^(?:please\s+|bhai\s+|bhau\s+|dada\s+|mala\s+|mujhe\s+)+', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'^(?:what\s+is\s+(?:a\s+|an\s+|the\s+)?|what\s+are\s+(?:the\s+)?|explain\s+(?:about\s+|the\s+)?|define\s+|meaning\s+of\s+)', '', cleaned, flags=re.IGNORECASE)
    # Remove conversational verbs and Marathi/Hindi imperative suffixes
    cleaned = re.sub(r'\s+(?:explain\s+)?(?:karr*|kr|kara|karo|sang|sangg|sanga|batao|samjhao|samjha|dakhva|dakhav|liha|de)\s*(?:mala|mujhe|na|re)?\??$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+(?:mhanje\s+kay|mhnje\s+kay|म्हणजे\s*काय|काय\s*आहे|kay\s+ahe|kaay\s+aahe|kya\s+hai|kya\s+hota\s+hai|arth\s+kay)\s*(?:ahe|aahe)?\??$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+(?:badal|baddal|vishayi)\s*(?:sang|sanga|bol|mahiti\s+de)?\??$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+(?:library|package|module|framework|concept)\s*(?:explain\s+)?(?:karr*|kr|kara|karo|sang|sanga|batao)?\??$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[\?\.\!]+$', '', cleaned).strip()
    if cleaned and len(cleaned) >= 2 and cleaned.lower() not in {"code", "python", "script", "program"}:
        return cleaned
    return None


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

        # 2. Extract Explicit Format Constraints & Continuation Detection
        import re

        # Continuation detection: only match requests to resume/continue unfinished code,
        # not standalone demands for complete code.
        is_exact_continuation_phrase = bool(
            re.match(r"^\s*(?:please\s+)?(?:complete|continue|finish)\s+(?:the\s+)?code\s*[\.!]?$", user_text, re.IGNORECASE)
        )
        CONTINUATION_PATTERNS = [
            re.compile(
                r"\b((?:continue|finish)\s+(?:the\s+)?code|"
                r"(?:continue|complete|finish)\s+(?:the\s+)?(?:code\s+)?from\s+where\s+it\s+stopped|"
                r"complete\s+(?:the\s+)?(?:unfinished|truncated)\s+code)\b",
                re.IGNORECASE,
            ),
            re.compile(r"\b(code\s+purna\s+kar|code\s+continue\s+kar|aage\s+ka\s+code)\b", re.IGNORECASE),
        ]
        is_continuation = is_exact_continuation_phrase or any(p.search(user_text) for p in CONTINUATION_PATTERNS)

        # In continuation mode, discover original task to preserve user constraints
        original_user_task: Optional[str] = None
        if is_continuation and context_package is not None and context_package.messages:
            for msg in context_package.messages:
                if msg.role == "user" and not any(p.search(msg.content) for p in CONTINUATION_PATTERNS):
                    original_user_task = msg.content
                    break

        explicit_req = detect_explicit_format_requirements(user_text)
        if is_continuation and original_user_task:
            orig_req = detect_explicit_format_requirements(original_user_task)
            if orig_req.code_and_tests_only:
                explicit_req.code_and_tests_only = True
                explicit_req.num_test_cases = orig_req.num_test_cases
            if orig_req.code_only:
                explicit_req.code_only = True

        # Check follow-up status and previous code presence from context
        is_follow_up = False
        has_previous_code = False
        if context_package is not None:
            if context_package.metadata and context_package.metadata.is_follow_up:
                is_follow_up = True
            if context_package.generated_code or context_package.current_code:
                has_previous_code = True

        # 3. Plan Response Sections Dynamically
        if is_continuation:
            response_sections = ["Code with Test Cases"] if explicit_req.code_and_tests_only else ["Code only"]
        else:
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
        if is_continuation:
            explicit_constraints.append(
                "CONTINUATION TASK: The previous code generation was truncated. "
                "Output ONLY the complete, syntactically valid code including the requested test cases. "
                "Do NOT output any conversation summaries, history recaps, or explanations."
            )
        elif explicit_req.code_and_tests_only:
            tc_count = explicit_req.num_test_cases or 2
            explicit_constraints.append(
                f"USER DEMAND: Output ONLY complete working code and exactly {tc_count} simple test cases. "
                "Do NOT output lengthy testing strategies, algorithm breakdowns, flowcharts, viva questions, or conversational text. "
                "Include the test cases directly in an executable `if __name__ == '__main__':` block or assertions."
            )
        elif explicit_req.code_only:
            explicit_constraints.append(
                "USER DEMAND: Output ONLY raw executable code. Do NOT output any introductory text, explanation, or commentary."
            )

        if explicit_req.algorithm and not is_continuation:
            explicit_constraints.append("Include explicit algorithmic logic and steps.")
        if explicit_req.flowchart and not is_continuation:
            explicit_constraints.append("Include an ASCII/text-based flowchart illustrating control flow.")
        if explicit_req.viva_questions and not is_continuation:
            explicit_constraints.append("Include viva/interview questions testing understanding.")
        if explicit_req.line_by_line and not is_continuation:
            explicit_constraints.append("Provide a line-by-line breakdown explaining what each key line accomplishes.")
        if explicit_req.step_by_step and not is_continuation:
            explicit_constraints.append("Provide a step-by-step procedure.")
        if (explicit_req.example or explicit_req.output) and not is_continuation:
            explicit_constraints.append("Include concrete sample input and corresponding expected output.")
        if explicit_req.table and not is_continuation:
            explicit_constraints.append("Format key comparisons in a clean markdown table.")
        if explicit_req.short:
            explicit_constraints.append("Keep response extremely brief and concise.")
        if explicit_req.detailed and not is_continuation:
            explicit_constraints.append("Provide a thorough, comprehensive, and detailed walkthrough.")

        # Mathematical accuracy directive for prime numbers
        check_text = (original_user_task or user_text).lower()
        if "prime" in check_text:
            explicit_constraints.append(
                "MATHEMATICAL ACCURACY: For prime testing, non-positive numbers (<= 1), 0, and 1 are NOT prime. "
                "Do NOT claim 2**64 - 1 is prime (it is composite; divisible by 3). "
                "Provide simple, valid test cases (e.g., 7 is prime, 4 is composite)."
            )

        # Concept subject disambiguation directive
        if detected_intent == "CONCEPT":
            concept_subject = extract_concept_subject(user_text)
            if concept_subject:
                explicit_constraints.append(
                    f"CONCEPT DEFINITION DIRECTIVE:\n"
                    f"- The specific topic to explain is: '{concept_subject}'.\n"
                    f"- Focus entirely on explaining '{concept_subject}' accurately with relevant Python examples and clear definitions."
                )

        # Machine Learning task directives: feature/label separation, pipeline inputs, dataset counts
        ML_PATTERNS = [
            r"\b(scikit-learn|sklearn|logistic\s+regression|linear\s+regression|random\s+forest|svm|support\s+vector)\b",
            r"\b(tfidf|tf-idf|vectorizer|countvectorizer|feature_extraction)\b",
            r"\b(sentiment\s+(?:analysis|classification)|text\s+classification|binary\s+classification)\b",
            r"\b(machine\s+learning|ml\s+model|train\s+(?:a\s+)?model|fit\s+(?:a\s+)?model|predict\s+labels?)\b",
            r"\b(pipeline\s+with\s+tfidf|classifier|classification\s+model)\b",
        ]
        is_ml_task = any(re.search(pat, check_text, re.IGNORECASE) for pat in ML_PATTERNS)
        ml_instruction: Optional[str] = None
        if is_ml_task:
            ml_instruction = MLPolicy.get_instruction(explicit_req=explicit_req, user_text=check_text)
            explicit_constraints.append(
                "MACHINE LEARNING SPECIFICATION & PIPELINE RULES:\n"
                "- Input features (X) and target labels (y) MUST be strictly separated. "
                "Train the model to predict the target labels (y), NEVER train it to predict the input features or text (X).\n"
                "- When using a scikit-learn Pipeline with a text vectorizer (such as TfidfVectorizer) and a classifier, "
                "pass a 1D list of raw text strings directly to pipeline.fit(X, y). "
                "NEVER pre-transform X with TF-IDF before passing to the Pipeline.\n"
                "- Model predictions pipeline.predict() MUST take a 1D list of raw strings (e.g., ['sample text']), NOT nested lists like [['sample text']]."
            )
            sample_count = explicit_req.num_samples
            if sample_count:
                explicit_constraints.append(
                    f"EXACT DATASET SIZE & LABELS: You MUST provide exactly {sample_count} training samples in X and exactly {sample_count} matching target labels in y. "
                    f"Ensure len(X) == len(y) == {sample_count}. Explicitly specify ground-truth labels for all {sample_count} samples."
                )

        # 6. Assemble Context Text and Code Continuity
        context_parts: List[str] = []
        current_code: Optional[str] = None

        if context_package is not None:
            if is_continuation:
                # In continuation mode: DO NOT inject previous assistant summaries or conversation turns
                context_parts.append(
                    f"[CONTINUATION DIRECTIVE: Continue and complete the unfinished code adhering to original task: '{original_user_task or user_text}'.\n"
                    "Output ONLY the complete Python code starting from or including the function and requested test cases.\n"
                    "Do NOT provide conversation summaries or explanations.]"
                )
                if context_package.current_code:
                    current_code = context_package.current_code
                elif context_package.generated_code:
                    current_code = context_package.generated_code[-1].code

                if current_code:
                    context_parts.append(
                        f"[INCOMPLETE CODE TO COMPLETE]:\n```python\n{current_code}\n```"
                    )
            else:
                if context_package.metadata and context_package.metadata.is_follow_up:
                    is_follow_up = True
                    context_parts.append(
                        "[FOLLOW-UP DIRECTIVE: The user request modifies or builds on previous turns. "
                        "You MUST modify, update, or reference the active code artifact rather than starting from scratch. "
                        "You MUST provide the COMPLETE, FULL working replacement program containing all modifications. "
                        "Never output partial diffs, isolated fragments, or incomplete snippets. "
                        "The code must be fully standalone, complete, and syntactically valid from start to finish.]"
                    )
                    explicit_constraints.append(
                        "COMPLETE WORKING REPLACEMENT: Output the complete, full replacement program including all changes and existing working logic. Do not output incomplete snippets."
                    )

                # Historical messages (only for non-continuation requests)
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
            ml_instruction=ml_instruction,
            metadata={
                "detected_language": detected_lang,
                "detected_tone": detected_tone,
                "detected_intent": detected_intent,
                "study_mode": study_mode,
                "is_follow_up": is_follow_up,
                "explicit_format_matched": explicit_req.matched_patterns,
            },
        )
