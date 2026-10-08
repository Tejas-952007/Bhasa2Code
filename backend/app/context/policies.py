"""Context window policies and follow-up heuristic detection for Bhasha2Code."""

import re
from typing import Optional, Set
from pydantic import BaseModel, Field

from backend.app.nlp.schemas import NLPPipelineResult


class ContextPolicy(BaseModel):
    """Configuration governing conversational context window sizes and truncation budgets."""

    max_messages: int = Field(default=12, ge=1, description="Maximum number of historical turns to retain.")
    max_characters: int = Field(default=16000, ge=100, description="Maximum total character budget for messages.")
    max_code_characters: int = Field(default=12000, ge=100, description="Maximum character budget for generated code.")
    max_generated_code_items: int = Field(default=3, ge=1, description="Maximum number of generated code artifacts.")
    standalone_max_messages: int = Field(
        default=4, ge=0, description="Historical turn budget for standalone (non-follow-up) queries."
    )


# ---------------------------------------------------------------------------
# Follow-Up Heuristic Vocabulary
# ---------------------------------------------------------------------------

# Pronouns and deictic references in English, Marathi, Hindi (Latin and native script)
DEICTIC_TOKENS: Set[str] = {
    # English
    "it", "this", "that", "these", "those", "same", "again", "above", "previous", "here", "its",
    # Marathi (Latin script)
    "ha", "hi", "he", "ya", "yat", "hyat", "tyat", "tyacha", "yacha", "tyala", "yala",
    "to", "ti", "te", "tya", "parat", "punha", "tasa", "asa",
    # Marathi (Devanagari script)
    "हा", "ही", "हे", "या", "यात", "ह्यात", "त्यात", "त्याचा", "याचा", "त्याला", "याला",
    "तो", "ती", "ते", "त्या", "पुन्हा", "परत", "तसा", "असा",
    # Hindi (Latin script)
    "yeh", "ye", "woh", "wo", "iska", "uska", "isko", "usko", "isme", "usme",
    "isse", "usse", "ise", "use", "wahi", "dobara", "phir", "aisa", "waisa",
    # Hindi (Devanagari script)
    "यह", "वह", "ये", "वो", "इसका", "उसका", "इसको", "उसको", "इसमें", "उसमें",
    "इससे", "उससे", "इसे", "उसे", "वही", "दोबारा", "फिर", "ऐसा", "वैसा",
}

# Modification verbs indicating alteration of existing code/conversation
MODIFICATION_VERBS: Set[str] = {
    # English
    "add", "remove", "change", "convert", "optimize", "fix", "debug", "refactor",
    "improve", "modify", "update", "rewrite", "explain", "shorten", "simplify",
    # Marathi
    "सुधार", "बदल", "काढ", "जोड", "समजाव", "वाढव", "कमी",
    # Hindi
    "हटाओ", "बदलो", "सुधारो", "जोड़ो", "समझाओ", "छोटा",
}

# Common follow-up phrases (regex-based)
FOLLOW_UP_PHRASES: list[re.Pattern] = [
    re.compile(r"\b(error\s+handling|edge\s+cases?|validation|unit\s+tests?|comments?|type\s+hints?|logging|docstring)\b", re.IGNORECASE),
    re.compile(r"\b(make\s+it\s+(shorter|faster|cleaner|simpler|better|longer))\b", re.IGNORECASE),
    re.compile(r"\b(what\s+about|how\s+about|what\s+if|same\s+(for|with|in))\b", re.IGNORECASE),
    re.compile(r"\b(step\s+by\s+step|line\s+by\s+line)\b", re.IGNORECASE),
    re.compile(r"\b(yat|tyat|hyat|isme|usme|isko|usko)\s+(.*)\s*(kar|karo|lava|kara|dya)\b", re.IGNORECASE),
]

# Explicit standalone topic creation patterns (indicating a brand-new task)
STANDALONE_PATTERNS: list[re.Pattern] = [
    re.compile(
        r"^(write|create|implement|build|develop|generate)\s+(a|an|the)?\s*([a-zA-Z0-9_-]+\s+){0,3}(calculator|api|program|app|function|class|script|service|system|algorithm|scraper|crawler|bot|game|server|client|database|crud)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"^what\s+(is|are)\s+(a|an|the)?\s*([a-zA-Z0-9_-]+\s+){0,2}(polymorphism|inheritance|encapsulation|abstraction|recursion|concurrency|threading|asynchronous|docker|kubernetes|git|sql|nosql|decorator|generator|interface|pointer|garbage\s+collection)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r".*\b(madhe|mein|me)\s+(calculator|api|program|algorithm|app|script)\s+(bana|banao|banva|tayyar kar)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r".*\b(calculator|api|program|algorithm|app)\s+(liha|likho|bana|banao|banva)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"^(बाइनरी|मर्ज|क्विक|लिनियर)\s+.*(अल्गोरिदम|शोध)\s+(लिहा|करा|दाखवा)",
        re.IGNORECASE,
    ),
]


def is_follow_up(message: str, nlp_result: Optional[NLPPipelineResult] = None) -> bool:
    """Deterministically detect if the user's message is a follow-up to prior conversation context.

    Heuristics:
    1. Presence of deictic references/pronouns (it, this, that, yat, isko, etc.).
    2. Explicit follow-up phrases (error handling, edge cases, make it shorter, what about).
    3. Modification verbs without standalone creation subjects.
    4. Short length with continuation or debugging intent.
    5. Exclusion of standalone new program generation or definition queries.
    """
    if not message or not message.strip():
        return False

    raw = message.strip()
    norm = raw.lower()
    tokens = re.findall(r"\w+", norm, re.UNICODE)
    word_count = len(tokens)
    char_len = len(raw)

    # 1. Check for deictic reference tokens
    has_deictic = any(token in DEICTIC_TOKENS for token in tokens)

    # 2. Check for standalone new task creation patterns (if NO explicit deictic reference)
    if not has_deictic:
        for pat in STANDALONE_PATTERNS:
            if pat.search(norm):
                return False

    # If deictic pronoun is explicitly used, it is almost certainly referring to prior context
    if has_deictic:
        return True

    # 3. Check follow-up phrases
    for pat in FOLLOW_UP_PHRASES:
        if pat.search(norm):
            return True

    # 4. Modification verbs in concise messages
    has_mod_verb = any(token in MODIFICATION_VERBS for token in tokens)
    if has_mod_verb and (word_count <= 8 or char_len <= 60):
        return True

    # 5. Very short utterances (< 5 words, < 35 chars) that are not simple greetings
    if word_count <= 5 and char_len <= 35:
        if not re.search(r"^(hi|hello|hey|namaste|namaskar|good\s+morning)\b", norm):
            return True

    # 6. Intent-assisted check from T14 NLP pipeline
    if nlp_result is not None:
        intent = nlp_result.detected_intent
        continuation_intents = {
            "DEBUG_CODE",
            "OPTIMIZE_CODE",
            "CONVERT_CODE",
            "CODE_SUGGESTION",
            "ERROR_EXPLANATION",
            "TEST_CASE_GENERATION",
        }
        if intent in continuation_intents and char_len <= 80:
            return True

    return False
