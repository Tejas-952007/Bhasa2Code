"""Explicit format detection and dynamic response section planning for Bhasha2Code."""

import re
from typing import List, Optional, Set
from pydantic import BaseModel, Field


class ExplicitFormatRequirements(BaseModel):
    """Encapsulates formatting structures explicitly requested by the user."""

    code_only: bool = False
    code_and_tests_only: bool = False
    num_test_cases: Optional[int] = None
    num_samples: Optional[int] = None
    algorithm: bool = False
    flowchart: bool = False
    viva_questions: bool = False
    line_by_line: bool = False
    step_by_step: bool = False
    example: bool = False
    output: bool = False
    table: bool = False
    notes: bool = False
    summary: bool = False
    short: bool = False
    detailed: bool = False
    matched_patterns: List[str] = Field(default_factory=list)

    @property
    def has_explicit_format(self) -> bool:
        """Return True if any specific format structure was requested."""
        return any(
            [
                self.code_only,
                self.code_and_tests_only,
                self.algorithm,
                self.flowchart,
                self.viva_questions,
                self.line_by_line,
                self.step_by_step,
                self.example,
                self.output,
                self.table,
                self.notes,
                self.summary,
                self.short,
                self.detailed,
            ]
        )


# ---------------------------------------------------------------------------
# Multilingual Explicit Format Regex Patterns
# ---------------------------------------------------------------------------

PATTERNS_CODE_ONLY: list[re.Pattern] = [
    re.compile(r"\b(only\s+code|code\s+only|just\s+code|just\s+the\s+code|pure\s+code)\b", re.IGNORECASE),
    re.compile(r"\b(only|just|pure)\s+(?:complete\s+|full\s+|raw\s+)?(?:python|c\+\+|cpp|c|java|javascript|js|sql)?\s*code\b", re.IGNORECASE),
    re.compile(r"\b(no\s+explanation|without\s+explanation|without\s+any\s+text)\b", re.IGNORECASE),
    # Marathi: fakt code de, fakt code, fakta code, etc.
    re.compile(r"\b(fakt|fakta|fakth|faktach|फक्त|केवळ)\s+(?:complete\s+|purna\s+)?code\b", re.IGNORECASE),
    re.compile(r"\bcode\s+(fakt|fakta|fakth|ch|फक्त|केवळ)\b", re.IGNORECASE),
    # Hindi: sirf code do, bas code, keval code
    re.compile(r"\b(sirf|bas|keval|सिर्फ|बस|केवल)\s+(?:complete\s+|pura\s+)?code\b", re.IGNORECASE),
    re.compile(r"\bcode\s+(sirf|bas|hi|केवळ)\b", re.IGNORECASE),
]

PATTERNS_CODE_AND_TESTS: list[re.Pattern] = [
    re.compile(
        r"\b(?:only|just|pure|give\s+only)\s+(?:complete\s+|full\s+|raw\s+)?(?:python|c\+\+|cpp|c|java|javascript|js|sql)?\s*code\s+(?:and|\+|along\s+with)\s+(?:(?P<count>one|two|three|four|five|\d+|do|don|ek|teen)\s+)?(?:simple\s+)?test\s*cases?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bcode\s+(?:and|\+|along\s+with)\s+(?:(?P<count>one|two|three|four|five|\d+|do|don|ek|teen)\s+)?(?:simple\s+)?test\s*cases?\s+(?:only|just)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:sirf|fakt)\s+(?:complete\s+)?code\s+(?:aur|ani|\+)\s+(?:(?P<count>\d+|do|don|ek|two)\s+)?(?:simple\s+)?test\s*cases?\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:only|just)\s+(?:complete\s+)?(?:python\s+)?code\s+and\s+(?:(?P<count>one|two|three|\d+)\s+)?(?:simple\s+)?tests?\b",
        re.IGNORECASE,
    ),
]

PATTERNS_ALGORITHM: list[re.Pattern] = [
    re.compile(r"\b(algorithm|alko|algoridham|अल्गोरिदम|अल्गोरिथम)\b", re.IGNORECASE),
]

PATTERNS_FLOWCHART: list[re.Pattern] = [
    re.compile(r"\b(flowchart|flow\s+chart|diagram|फ्लोचार्ट|डायग्राम)\b", re.IGNORECASE),
]

PATTERNS_VIVA: list[re.Pattern] = [
    re.compile(r"\b(viva|viva\s+questions?|viva\s+che\s+prashna|interview\s+questions?|विवा|प्रश्नोत्तरे)\b", re.IGNORECASE),
]

PATTERNS_LINE_BY_LINE: list[re.Pattern] = [
    re.compile(r"\b(line\s+by\s+line|line\s+to\s+line|each\s+line|प्रत्येक\s+ओळ)\b", re.IGNORECASE),
]

PATTERNS_STEP_BY_STEP: list[re.Pattern] = [
    re.compile(r"\b(step\s+by\s+step|step\s+wise|steps|पायरीने|स्टेप\s+बाय\s+स्टेप)\b", re.IGNORECASE),
]

PATTERNS_EXAMPLE: list[re.Pattern] = [
    re.compile(r"\b(example|sample|sample\s+input|test\s+case|उदाहरण)\b", re.IGNORECASE),
]

PATTERNS_OUTPUT: list[re.Pattern] = [
    re.compile(r"\b(sample\s+output|output|आऊटपुट|रिजल्ट)\b", re.IGNORECASE),
]

PATTERNS_TABLE: list[re.Pattern] = [
    re.compile(r"\b(table|comparison|tabular|तक्ता|तुलना)\b", re.IGNORECASE),
]

PATTERNS_NOTES: list[re.Pattern] = [
    re.compile(r"\b(notes|summary|takeaways|सारांश|नोट्स)\b", re.IGNORECASE),
]

PATTERNS_SHORT: list[re.Pattern] = [
    re.compile(r"\b(short\s+answer|in\s+short|briefly|short\s+madhe|chhota\s+karo|संक्षिप्त|थोडक्यात)\b", re.IGNORECASE),
]

PATTERNS_DETAILED: list[re.Pattern] = [
    re.compile(r"\b(in\s+detail|detailed\s+answer|detailed|savistar|vistrut|सविस्तर|विस्तृत)\b", re.IGNORECASE),
]


def detect_explicit_format_requirements(user_message: str) -> ExplicitFormatRequirements:
    """Deterministically extract user-requested structural formats from the message."""
    req = ExplicitFormatRequirements()
    if not user_message or not user_message.strip():
        return req

    norm = user_message.strip()

    WORD_TO_NUM = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
        "ek": 1, "do": 2, "don": 2, "teen": 3, "char": 4, "chaar": 4,
        "paanch": 5, "panch": 5, "saha": 6, "chhe": 6, "saat": 7,
        "aath": 8, "nau": 9, "das": 10, "dah": 10, "akra": 11, "gyarah": 11,
        "barah": 12, "bara": 12,
    }

    # Explicit sample dataset count detection
    sample_match = re.search(
        r"\b(?P<count>\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|do|don|teen|char|paanch|saha|saat|aath|nau|das|dah|akra|barah|bara)\s+(?:samples|examples|records|data\s*points|sentences|reviews)\b",
        norm,
        re.IGNORECASE,
    )
    if sample_match:
        c_str = sample_match.group("count").lower()
        num_val = WORD_TO_NUM.get(c_str, int(c_str) if c_str.isdigit() else None)
        if num_val:
            req.num_samples = num_val
            req.matched_patterns.append(f"samples_{num_val}")

    # Code and Tests Only (prioritized over pure code_only)
    for pat in PATTERNS_CODE_AND_TESTS:
        m = pat.search(norm)
        if m:
            req.code_and_tests_only = True
            count_str = m.groupdict().get("count")
            if count_str:
                count_lower = count_str.lower()
                req.num_test_cases = WORD_TO_NUM.get(count_lower, int(count_lower) if count_lower.isdigit() else 2)
            else:
                req.num_test_cases = 2
            req.matched_patterns.append("code_and_tests_only")
            break

    # Code Only (only if code_and_tests_only not triggered)
    if not req.code_and_tests_only:
        for pat in PATTERNS_CODE_ONLY:
            if pat.search(norm):
                req.code_only = True
                req.matched_patterns.append("code_only")
                break

    # Algorithm
    for pat in PATTERNS_ALGORITHM:
        if pat.search(norm):
            req.algorithm = True
            req.matched_patterns.append("algorithm")
            break

    # Flowchart
    for pat in PATTERNS_FLOWCHART:
        if pat.search(norm):
            req.flowchart = True
            req.matched_patterns.append("flowchart")
            break

    # Viva Questions
    for pat in PATTERNS_VIVA:
        if pat.search(norm):
            req.viva_questions = True
            req.matched_patterns.append("viva_questions")
            break

    # Line by line
    for pat in PATTERNS_LINE_BY_LINE:
        if pat.search(norm):
            req.line_by_line = True
            req.matched_patterns.append("line_by_line")
            break

    # Step by step
    for pat in PATTERNS_STEP_BY_STEP:
        if pat.search(norm):
            req.step_by_step = True
            req.matched_patterns.append("step_by_step")
            break

    # Example
    for pat in PATTERNS_EXAMPLE:
        if pat.search(norm):
            req.example = True
            req.matched_patterns.append("example")
            break

    # Output
    for pat in PATTERNS_OUTPUT:
        if pat.search(norm):
            req.output = True
            req.matched_patterns.append("output")
            break

    # Table
    for pat in PATTERNS_TABLE:
        if pat.search(norm):
            req.table = True
            req.matched_patterns.append("table")
            break

    # Notes / Summary
    for pat in PATTERNS_NOTES:
        if pat.search(norm):
            req.notes = True
            req.matched_patterns.append("notes")
            break

    # Short
    for pat in PATTERNS_SHORT:
        if pat.search(norm):
            req.short = True
            req.matched_patterns.append("short")
            break

    # Detailed
    for pat in PATTERNS_DETAILED:
        if pat.search(norm):
            req.detailed = True
            req.matched_patterns.append("detailed")
            break

    return req


# ---------------------------------------------------------------------------
# Intent-to-Section Mapping Tables (18 Supported Intents)
# ---------------------------------------------------------------------------

NORMAL_MODE_SECTIONS: dict[str, list[str]] = {
    "GENERATE_CODE": [
        "Code",
        "Brief Explanation",
        "Usage / Example",
    ],
    "DEBUG_CODE": [
        "Problem",
        "Likely Cause",
        "Fix",
        "Corrected Code",
        "Validation / Expected Result",
    ],
    "EXPLAIN_CODE": [
        "What the code does",
        "Key Sections",
        "Brief Explanation",
        "Example",
    ],
    "OPTIMIZE_CODE": [
        "Current Issue",
        "Optimization Strategy",
        "Improved Code",
        "Performance Impact",
    ],
    "CONVERT_CODE": [
        "Source Language",
        "Target Language",
        "Converted Code",
        "Important Differences",
    ],
    "ALGORITHM": [
        "Algorithm",
        "How it works",
        "Complexity",
        "Example",
    ],
    "CONCEPT": [
        "Definition",
        "Simple Explanation",
        "Example",
    ],
    "CODE_REVIEW": [
        "Overall Assessment",
        "Issues",
        "Suggestions",
        "Improved Snippets",
    ],
    "CODE_SUGGESTION": [
        "Suggestions",
        "Recommended Changes",
        "Example Snippet",
    ],
    "PERFORMANCE_ANALYSIS": [
        "Observed Issue",
        "Likely Bottleneck",
        "Performance Analysis",
        "Recommendation",
    ],
    "ERROR_EXPLANATION": [
        "Error Meaning",
        "Cause",
        "How to Prevent It",
    ],
    "APPROACH_SUGGESTION": [
        "Recommended Approach",
        "Steps",
        "Why this approach",
    ],
    "BEST_PRACTICE": [
        "Recommended Practice",
        "Why",
        "Example",
    ],
    "ARCHITECTURE_SUGGESTION": [
        "Recommended Architecture",
        "Components",
        "Data Flow",
        "Technology Roles",
    ],
    "FEATURE_SUGGESTION": [
        "Feature Ideas",
        "Priority",
        "Short Reason",
    ],
    "TEST_CASE_GENERATION": [
        "Test Cases",
        "Expected Results",
        "Unit Test Code",
    ],
    "SECURITY_ANALYSIS": [
        "Security Issue",
        "Risk",
        "Recommendation",
        "Secure Example",
    ],
    "SEARCH": [
        "Search Result",
        "Relevant Context",
        "Requested Item",
    ],
}

STUDY_MODE_SECTIONS: dict[str, list[str]] = {
    "GENERATE_CODE": [
        "Problem Understanding",
        "Algorithm",
        "Flowchart",
        "Code",
        "Detailed Explanation",
        "Example Input/Output",
        "Important Points",
        "Viva Questions",
    ],
    "DEBUG_CODE": [
        "Problem",
        "Cause",
        "Why the error happened",
        "Debugging Approach",
        "Corrected Code",
        "Line-by-line relevant explanation",
        "Test Case",
        "Expected Output",
        "Common Mistakes",
        "Viva Questions",
    ],
    "EXPLAIN_CODE": [
        "Purpose",
        "Algorithm / Logic",
        "Flowchart",
        "Code",
        "Line-by-line Explanation",
        "Example",
        "Output",
        "Key Concepts",
        "Viva Questions",
    ],
    "OPTIMIZE_CODE": [
        "Current Approach",
        "Bottleneck",
        "Optimization Strategy",
        "Before/After Comparison",
        "Optimized Code",
        "Time Complexity",
        "Space Complexity",
        "Trade-offs",
    ],
    "CONVERT_CODE": [
        "Approach",
        "Source Code",
        "Target Code",
        "Syntax Differences",
        "Conceptual Differences",
        "Example",
        "Important Notes",
    ],
    "ALGORITHM": [
        "Definition",
        "Algorithm Steps",
        "Flowchart",
        "Pseudo-code",
        "Detailed Working",
        "Example",
        "Time Complexity",
        "Space Complexity",
        "Advantages",
        "Limitations",
        "Viva Questions",
    ],
    "CONCEPT": [
        "Definition",
        "Simple Explanation",
        "Real-world Analogy",
        "Technical Explanation",
        "Example",
        "Common Misconceptions",
        "Key Points",
        "Viva Questions",
    ],
    "CODE_REVIEW": [
        "Code Quality",
        "Correctness",
        "Readability",
        "Maintainability",
        "Performance",
        "Security",
        "Issues",
        "Recommendations",
        "Improved Version",
    ],
    "CODE_SUGGESTION": [
        "Current Approach",
        "Suggestions",
        "Reason for Each Suggestion",
        "Example Improvements",
        "Best Choice",
    ],
    "PERFORMANCE_ANALYSIS": [
        "Performance Goal",
        "Current Complexity",
        "Likely Bottleneck",
        "Measurement Approach",
        "Optimization Opportunities",
        "Trade-offs",
    ],
    "ERROR_EXPLANATION": [
        "Error",
        "Meaning",
        "Root Cause",
        "Example",
        "How to Diagnose",
        "How to Prevent",
        "Viva Questions",
    ],
    "APPROACH_SUGGESTION": [
        "Problem Understanding",
        "Possible Approaches",
        "Recommended Approach",
        "Step-by-step Strategy",
        "Complexity",
        "Implementation Plan",
        "Common Mistakes",
    ],
    "BEST_PRACTICE": [
        "Problem",
        "Recommended Practice",
        "Reason",
        "Good vs Bad Example",
        "Practical Checklist",
        "Key Takeaways",
    ],
    "ARCHITECTURE_SUGGESTION": [
        "Requirements",
        "Architecture",
        "Component Diagram",
        "Data Flow",
        "Responsibilities",
        "Technology Choices",
        "Trade-offs",
        "Scalability",
        "Security Considerations",
    ],
    "FEATURE_SUGGESTION": [
        "Current Problem",
        "Feature",
        "Purpose",
        "Priority",
        "User Value",
        "Implementation Idea",
        "Future Expansion",
    ],
    "TEST_CASE_GENERATION": [
        "Testing Strategy",
        "Normal Cases",
        "Boundary Cases",
        "Edge Cases",
        "Negative Cases",
        "Expected Results",
        "Unit Tests",
        "Coverage Considerations",
    ],
    "SECURITY_ANALYSIS": [
        "Threat",
        "Vulnerability",
        "Impact",
        "Attack Scenario (safe educational)",
        "Mitigation",
        "Secure Implementation",
        "Best Practices",
        "Security Checklist",
    ],
    "SEARCH": [
        "Search Result",
        "Relevant Context",
        "Requested Item",
    ],
}

DEFAULT_NORMAL_SECTIONS = ["Overview", "Solution / Code", "Explanation", "Example"]
DEFAULT_STUDY_SECTIONS = [
    "Problem Understanding",
    "Algorithm",
    "Solution",
    "Detailed Explanation",
    "Example & Output",
    "Viva Questions",
]


def select_response_sections(
    intent: str,
    tone: str,
    study_mode: bool,
    explicit_requirements: ExplicitFormatRequirements,
    is_follow_up: bool = False,
    has_previous_code: bool = False,
) -> list[str]:
    """Deterministically select response sections adhering to priority hierarchy:
    1. Explicit user constraints (code_only trumps Study Mode, Tone, and Intent).
    2. Follow-up code modification turns.
    3. Study Mode defaults vs. Normal Mode defaults.
    4. Explicit additions (algorithm, flowchart, viva, etc.).
    5. Tone adjustments (SHORT vs. DETAILED vs. SIMPLE).
    """
    # 1. Highest Priority: Explicit User Constraints (code_only or code_and_tests_only trump Study Mode)
    if explicit_requirements.code_and_tests_only:
        return ["Code with Test Cases"]

    if explicit_requirements.code_only:
        return ["Code only"]

    # 2. Follow-Up Code Modification turn
    if is_follow_up and has_previous_code and not study_mode and not explicit_requirements.has_explicit_format:
        return [
            "Previous Code Reference",
            "Updated Code",
            "Explanation of Changes",
            "Example / Verification",
        ]

    intent_key = intent.upper() if intent else "GENERATE_CODE"

    # 3. Base Sections Selection
    if study_mode:
        base_sections = list(STUDY_MODE_SECTIONS.get(intent_key, DEFAULT_STUDY_SECTIONS))
    else:
        base_sections = list(NORMAL_MODE_SECTIONS.get(intent_key, DEFAULT_NORMAL_SECTIONS))

    sections: list[str] = list(base_sections)

    # 4. Explicit User Format Inclusions
    if explicit_requirements.algorithm and not any("algorithm" in s.lower() for s in sections):
        code_idx = next((i for i, s in enumerate(sections) if "code" in s.lower()), len(sections))
        sections.insert(code_idx, "Algorithm")

    if explicit_requirements.flowchart and not any("flowchart" in s.lower() for s in sections):
        algo_idx = next((i for i, s in enumerate(sections) if "algorithm" in s.lower()), -1)
        if algo_idx != -1:
            sections.insert(algo_idx + 1, "Flowchart")
        else:
            code_idx = next((i for i, s in enumerate(sections) if "code" in s.lower()), len(sections))
            sections.insert(code_idx, "Flowchart")

    if explicit_requirements.viva_questions and not any("viva" in s.lower() for s in sections):
        sections.append("Viva Questions")

    if explicit_requirements.line_by_line:
        new_sections = []
        replaced = False
        for s in sections:
            if "explanation" in s.lower() and not replaced:
                new_sections.append("Line-by-line Explanation")
                replaced = True
            else:
                new_sections.append(s)
        if not replaced:
            new_sections.append("Line-by-line Explanation")
        sections = new_sections

    if explicit_requirements.step_by_step and not any("step" in s.lower() for s in sections):
        sections.append("Step-by-step Guide")

    if (explicit_requirements.example or explicit_requirements.output) and not any(
        "example" in s.lower() or "output" in s.lower() for s in sections
    ):
        sections.append("Example Input/Output")

    if explicit_requirements.table and not any("table" in s.lower() for s in sections):
        sections.append("Comparison Table")

    if (explicit_requirements.notes or explicit_requirements.summary) and not any(
        "notes" in s.lower() or "summary" in s.lower() for s in sections
    ):
        sections.append("Important Notes & Summary")

    # 5. Tone Adjustments (Only in Normal Mode or when explicitly requesting brevity)
    tone_key = tone.upper() if tone else "CASUAL"

    if explicit_requirements.short and not study_mode and not explicit_requirements.detailed:
        essential = []
        for s in sections:
            s_lower = s.lower()
            if any(k in s_lower for k in ["code", "fix", "solution", "result", "algorithm", "direct"]):
                essential.append(s)
        if not essential:
            essential = ["Direct Answer"]
        sections = essential

    elif tone_key == "SHORT" and not study_mode and not explicit_requirements.detailed and not explicit_requirements.has_explicit_format:
        if intent_key == "GENERATE_CODE":
            sections = ["Code", "Brief Explanation", "Usage / Example"]
        else:
            essential = [s for s in sections if any(k in s.lower() for k in ["code", "fix", "solution", "result", "algorithm", "direct", "brief"])]
            sections = essential if essential else ["Direct Answer"]

    elif tone_key == "SIMPLE":
        if intent_key == "EXPLAIN_CODE":
            sections = ["Simple Explanation", "Example where useful"]
        else:
            sections = [
                s.replace("Detailed Explanation", "Simple Explanation")
                .replace("Technical Explanation", "Simple Explanation")
                .replace("Brief Explanation", "Simple Explanation")
                for s in sections
            ]

    elif tone_key == "DETAILED" and not study_mode:
        sections = [
            s.replace("Short Explanation", "Detailed Explanation").replace(
                "Brief Explanation", "Detailed Explanation"
            )
            for s in sections
        ]
        if not any("edge cases" in s.lower() for s in sections):
            sections.append("Edge Cases & Considerations")

    # Deduplicate while preserving deterministic order
    seen: Set[str] = set()
    deduped_sections: list[str] = []
    for s in sections:
        if s not in seen:
            seen.add(s)
            deduped_sections.append(s)

    return deduped_sections

