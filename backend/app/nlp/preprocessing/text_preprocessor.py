import logging
import re
import unicodedata
from typing import List, Optional, Tuple

from backend.app.nlp.schemas import CodeSegment, PreprocessedText

logger = logging.getLogger("bhasha2code.nlp.preprocessing")

# Regex to match Markdown fenced code blocks (``` or ~~~) with optional language tag
FENCE_PATTERN = re.compile(
    r"(?P<fence>```|~~~)(?P<lang>[a-zA-Z0-9_+-]*)[ \t]*\n?(?P<code>.*?)(?:\n(?P=fence)|(?P=fence)|\Z)",
    re.DOTALL,
)

# Structural patterns indicating unfenced raw code blocks
PYTHON_DEF_CLASS = re.compile(r"^\s*(def|class)\s+[a-zA-Z_][a-zA-Z0-9_]*\s*[\(:].*", re.MULTILINE)
TRACEBACK_PATTERN = re.compile(r"Traceback \(most recent call last\):")

TRAIL_INLINE_INST_PATTERN = re.compile(
    r"^(?P<code>.+?)\s{1,}(?P<inst>(?:please\s+|can\s+you\s+)?(?:explain|samjhav|samjav|check|debug|fix|run|test|batao|sang|what\s+does|how\s+does|is\s+there)\b.+)$",
    re.IGNORECASE,
)

STANDALONE_INST_PATTERN = re.compile(
    r"^\s*(?:please\s+|can\s+you\s+)?(?:explain|samjhav|samjav|check|debug|fix|run|test|batao|sang|what\s+does|how\s+does|is\s+there|help\s+me)\b",
    re.IGNORECASE,
)

CODE_LINE_PATTERN = re.compile(
    r"^\s*(?:#|//|/\*|\*|import\s+|from\s+|def\s+|class\s+|async\s+def\s+|function\s+|"
    r"[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*|public\s+|private\s+|protected\s+|void\s+|int\s+|float\s+|"
    r"const\s+|let\s+|var\s+|#include\s+|if\s+|while\s+|for\s+|try:|except|return\b|print\s*\(|console\.log)",
    re.IGNORECASE,
)


class TextPreprocessor:
    """Safe multilingual and code-aware text preprocessor for Bhasha2Code.
    
    Normalizes input text for NLP analysis while strictly preserving:
    - Multilingual and mixed-language semantics (Marathi, Hindi, English, Hinglish)
    - Code blocks, indentation, newlines, and technical syntax
    - Technical expressions (URLs, file paths, error messages, stack traces)
    - Punctuation, symbols, quotes, and emoji
    """

    def preprocess(self, text: Optional[str]) -> PreprocessedText:
        """Process raw input into a safe, structured PreprocessedText result."""
        # 1. Null and type safety
        if text is None:
            return PreprocessedText(
                original_text="",
                normalized_text="",
                text_segments=[],
                code_segments=[],
                classifier_text="",
                is_empty=True,
            )

        if not isinstance(text, str):
            text = str(text)

        # 2. Empty or whitespace-only detection
        raw_stripped = text.strip()
        if not raw_stripped:
            return PreprocessedText(
                original_text=text,
                normalized_text="",
                text_segments=[],
                code_segments=[],
                classifier_text="",
                is_empty=True,
            )

        try:
            # 3. Canonical line endings and Unicode NFC normalization
            clean_input = text.replace("\r\n", "\n").replace("\r", "\n")
            clean_input = unicodedata.normalize("NFC", clean_input)

            # 4. Check for Markdown fenced code blocks
            fenced_matches = list(FENCE_PATTERN.finditer(clean_input))
            if fenced_matches:
                return self._process_fenced_input(text, clean_input, fenced_matches)

            # 5. Check for unfenced raw code or stack trace
            if self._is_raw_code_or_trace(clean_input):
                return self._process_raw_code_input(text, clean_input)

            # 6. Process standard natural language input (multilingual safe)
            return self._process_natural_language_input(text, clean_input)

        except Exception as exc:
            logger.warning("Error during text preprocessing: %s; falling back to safe pass-through", exc)
            fallback_norm = unicodedata.normalize("NFC", text.strip())
            return PreprocessedText(
                original_text=text,
                normalized_text=fallback_norm,
                text_segments=[fallback_norm] if fallback_norm else [],
                code_segments=[],
                classifier_text=fallback_norm,
                is_empty=not bool(fallback_norm),
            )

    def _process_fenced_input(
        self,
        original_text: str,
        clean_input: str,
        matches: list,
    ) -> PreprocessedText:
        """Handle input containing Markdown fenced code blocks."""
        text_segments: List[str] = []
        code_segments: List[CodeSegment] = []
        normalized_parts: List[str] = []
        classifier_parts: List[str] = []

        last_idx = 0
        for match in matches:
            start, end = match.span()
            # Natural language text preceding this fence
            pre_text = clean_input[last_idx:start]
            norm_pre = self._normalize_whitespace(pre_text)
            if norm_pre:
                text_segments.append(norm_pre)
                normalized_parts.append(norm_pre)
                classifier_parts.append(norm_pre)

            # Code inside fence: strictly preserve indentation and newlines
            raw_code = match.group("code")
            # If code ends with trailing newline, strip at most one trailing newline for clean encapsulation
            code_content = raw_code.rstrip("\r\n") if raw_code.endswith("\n") else raw_code
            raw_lang = match.group("lang").strip().lower()
            lang_hint = raw_lang if raw_lang else None

            code_segments.append(CodeSegment(content=code_content, language_hint=lang_hint))

            fence_str = match.group("fence")
            lang_str = lang_hint or ""
            normalized_parts.append(f"{fence_str}{lang_str}\n{code_content}\n{fence_str}")

            last_idx = end

        # Trailing text after final code block
        post_text = clean_input[last_idx:]
        norm_post = self._normalize_whitespace(post_text)
        if norm_post:
            text_segments.append(norm_post)
            normalized_parts.append(norm_post)
            classifier_parts.append(norm_post)

        normalized_text = "\n\n".join(part for part in normalized_parts if part)
        classifier_text = " ".join(classifier_parts).strip()

        # If classifier_text is empty (input was code only), provide code content as classifier hint
        if not classifier_text and code_segments:
            classifier_text = code_segments[0].content

        return PreprocessedText(
            original_text=original_text,
            normalized_text=normalized_text,
            text_segments=text_segments,
            code_segments=code_segments,
            classifier_text=classifier_text,
            is_empty=False,
        )

    def _is_raw_code_or_trace(self, text: str) -> bool:
        """Check if unfenced text represents a stack trace or code block."""
        if TRACEBACK_PATTERN.search(text):
            return True
        if PYTHON_DEF_CLASS.search(text):
            lines = [line for line in text.split("\n") if line.strip()]
            # If multi-line with def/class and indented body, treat as code
            if len(lines) >= 2 and any(line.startswith(("  ", "\t")) for line in lines[1:]):
                return True
        return False

    def _process_raw_code_input(
        self,
        original_text: str,
        clean_input: str,
    ) -> PreprocessedText:
        """Handle unfenced code or stack trace input, separating preceding and trailing natural language if present."""
        stripped = clean_input.strip()
        lines = stripped.split("\n")
        post_lines: List[str] = []

        # 1. Extract inline trailing natural language instruction from last line if present
        if lines:
            last_line = lines[-1]
            m = TRAIL_INLINE_INST_PATTERN.match(last_line)
            if m and not last_line.strip().startswith("#"):
                lines[-1] = m.group("code").rstrip()
                post_lines.append(m.group("inst").strip())

        # 2. Extract standalone trailing natural language instruction lines
        while lines:
            last = lines[-1].strip()
            if not last:
                lines.pop()
                continue
            if STANDALONE_INST_PATTERN.search(last) and not CODE_LINE_PATTERN.search(last):
                post_lines.insert(0, lines.pop().strip())
            else:
                break

        # 3. Handle stack traces or code block preamble
        code_start_idx = 0
        if TRACEBACK_PATTERN.search(stripped):
            for i, line in enumerate(lines):
                if TRACEBACK_PATTERN.search(line):
                    code_start_idx = i
                    break
        else:
            # Find the true start of code (first code syntax line or indented body)
            for i, line in enumerate(lines):
                if not line.strip():
                    continue
                if CODE_LINE_PATTERN.search(line) or line.startswith(("  ", "\t")):
                    code_start_idx = i
                    break

        pre_lines = lines[:code_start_idx]
        code_lines = lines[code_start_idx:]

        norm_pre = self._normalize_whitespace("\n".join(pre_lines)) if pre_lines else ""
        norm_post = self._normalize_whitespace(" ".join(post_lines)) if post_lines else ""
        code_content = "\n".join(code_lines).strip()

        text_segments: List[str] = []
        if norm_pre:
            text_segments.append(norm_pre)
        if norm_post:
            text_segments.append(norm_post)

        code_segments = [CodeSegment(content=code_content, language_hint=None)] if code_content else []

        normalized_parts: List[str] = []
        if norm_pre:
            normalized_parts.append(norm_pre)
        if code_content:
            normalized_parts.append(code_content)
        if norm_post:
            normalized_parts.append(norm_post)
        normalized_text = "\n\n".join(normalized_parts) if normalized_parts else stripped

        classifier_text = " ".join(text_segments).strip() if text_segments else (norm_pre or code_content or stripped)

        return PreprocessedText(
            original_text=original_text,
            normalized_text=normalized_text,
            text_segments=text_segments,
            code_segments=code_segments,
            classifier_text=classifier_text,
            is_empty=False,
        )

    def _process_natural_language_input(
        self,
        original_text: str,
        clean_input: str,
    ) -> PreprocessedText:
        """Handle standard multilingual text, collapsing unnecessary whitespace while preserving tokens."""
        norm_text = self._normalize_whitespace(clean_input)
        return PreprocessedText(
            original_text=original_text,
            normalized_text=norm_text,
            text_segments=[norm_text] if norm_text else [],
            code_segments=[],
            classifier_text=norm_text,
            is_empty=not bool(norm_text),
        )

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize harmless spaces and newlines while keeping indentation and Devanagari intact."""
        stripped = text.strip()
        if not stripped:
            return ""

        lines = stripped.split("\n")
        cleaned_lines: List[str] = []

        for line in lines:
            if not line.strip():
                cleaned_lines.append("")
                continue

            # Check for intentional leading indentation
            leading_len = len(line) - len(line.lstrip(" "))
            if leading_len >= 2:
                indent = line[:leading_len]
                rest = re.sub(r"[ \t]+", " ", line[leading_len:].rstrip())
                cleaned_lines.append(f"{indent}{rest}")
            else:
                cleaned_lines.append(re.sub(r"[ \t]+", " ", line.strip()))

        rejoined = "\n".join(cleaned_lines)
        # Collapse excessive blank lines (3+ newlines -> 2 newlines)
        return re.sub(r"\n{3,}", "\n\n", rejoined).strip()
