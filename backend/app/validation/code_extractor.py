"""Markdown code extractor for Bhasha2Code assistant responses."""

import re
from typing import List, Optional
from backend.app.validation.schemas import CodeBlock


# Regex matching code blocks fenced with ``` or ~~~
# Group 1: fence chars (``` or ~~~)
# Group 2: optional declared language/info string
# Group 3: code content
# Group 4: closing fence matching group 1
FENCED_BLOCK_PATTERN = re.compile(
    r"(?P<fence>```|~~~)[ \t]*(?P<lang>[a-zA-Z0-9_+#.-]*)[^\n]*\n"
    r"(?P<code>[\s\S]*?)"
    r"(?P=fence)",
    re.MULTILINE,
)

# Pattern for unclosed fence at the very end of response (e.g. truncated streaming)
UNCLOSED_FENCE_PATTERN = re.compile(
    r"(?P<fence>```|~~~)[ \t]*(?P<lang>[a-zA-Z0-9_+#.-]*)[^\n]*\n"
    r"(?P<code>[\s\S]+)$",
    re.MULTILINE,
)


class CodeExtractor:
    """Extracts fenced and structured code blocks from Markdown responses."""

    def extract_blocks(self, text: str) -> List[CodeBlock]:
        """Extract all fenced code blocks from a Markdown text response.

        Args:
            text: Markdown response string.

        Returns:
            List of CodeBlock objects in order of appearance.
        """
        if not text or not text.strip():
            return []

        blocks: List[CodeBlock] = []
        block_id = 1
        last_end = 0

        # 1. Match fully closed fences
        for match in FENCED_BLOCK_PATTERN.finditer(text):
            lang_str = match.group("lang")
            code_str = match.group("code")
            declared_lang = self._normalize_declared_lang(lang_str)

            blocks.append(
                CodeBlock(
                    block_id=block_id,
                    declared_language=declared_lang,
                    code=code_str.strip("\r\n"),
                    start_char=match.start(),
                    end_char=match.end(),
                    is_fenced=True,
                )
            )
            block_id += 1
            last_end = match.end()

        # 2. Check for an unclosed fence at the end of the text (e.g. truncated streaming or token limit cutoff)
        remaining_text = text[last_end:]
        if "```" in remaining_text or "~~~" in remaining_text:
            unclosed_match = UNCLOSED_FENCE_PATTERN.search(remaining_text)
            if unclosed_match:
                lang_str = unclosed_match.group("lang")
                code_str = unclosed_match.group("code")
                declared_lang = self._normalize_declared_lang(lang_str)
                start_offset = last_end + unclosed_match.start()
                end_offset = last_end + unclosed_match.end()

                blocks.append(
                    CodeBlock(
                        block_id=block_id,
                        declared_language=declared_lang,
                        code=code_str.strip("\r\n"),
                        start_char=start_offset,
                        end_char=end_offset,
                        is_fenced=False,
                    )
                )

        return blocks

    def _normalize_declared_lang(self, raw_lang: Optional[str]) -> Optional[str]:
        """Clean raw language identifier string from code fence."""
        if not raw_lang:
            return None
        lang = raw_lang.strip().lower()
        if not lang:
            return None
        # Extract first token if contains colon or spaces (e.g. python:calc.py)
        token = re.split(r"[:\s]", lang)[0].strip()
        return token if token else None
