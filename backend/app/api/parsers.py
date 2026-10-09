"""Response parsers for extracting explanation, example, and study sections from assistant text."""

import re
from typing import Dict, List, Optional, Tuple

from backend.app.api.schemas import StudySectionResponse


def _strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks to extract pure markdown prose."""
    return re.sub(r"```[\s\S]*?```", "", text).strip()


def parse_sections(text: str) -> Dict[str, str]:
    """Parse markdown headers into a dictionary of section names to body texts."""
    sections: Dict[str, str] = {}
    lines = text.splitlines()

    current_section = "_main"
    current_lines: List[str] = []

    header_pattern = re.compile(
        r"^(?:#{1,4}\s+|\d+\.\s+\*{0,2}|\*{2})?([A-Za-z0-9\s/_-]+?)(?:\*{2})?:?\s*$"
    )

    for line in lines:
        stripped = line.strip()
        match = header_pattern.match(stripped)
        if match:
            candidate = match.group(1).strip().lower()
            # Normalize common section names
            key = None
            if "problem" in candidate and ("understanding" in candidate or candidate == "problem"):
                key = "problem_understanding"
            elif candidate.startswith("algorithm") or candidate.startswith("logic"):
                key = "algorithm"
            elif candidate.startswith("flowchart") or "diagram" in candidate:
                key = "flowchart"
            elif "viva" in candidate or "interview" in candidate or "question" in candidate:
                key = "viva_questions"
            elif "point" in candidate or "important" in candidate or "key note" in candidate:
                key = "important_points"
            elif candidate.startswith("explanation") or "how it works" in candidate:
                key = "explanation"
            elif candidate.startswith("example") or candidate.startswith("usage") or candidate.startswith("output"):
                key = "example"
            elif candidate.startswith("code"):
                key = "code"

            if key:
                if current_lines:
                    sections[current_section] = "\n".join(current_lines).strip()
                current_section = key
                current_lines = []
                continue

        current_lines.append(line)

    if current_lines:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


def parse_bullet_list(text: str) -> List[str]:
    """Extract bullet points or numbered items from a text block."""
    items: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        cleaned = re.sub(r"^[-*•]\s+|\d+\.\s+", "", line).strip()
        if cleaned:
            items.append(cleaned)
    return items


def parse_viva_questions(text: str) -> List[Dict[str, str]]:
    """Parse Q&A pairs from text."""
    pairs: List[Dict[str, str]] = []
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    current_q = None
    current_a = None

    for line in lines:
        q_match = re.match(r"^(?:Q\d*[:.]?|\d+\.\s*Q(?:uestion)?[:.]?|\*{2}Q\d*[:.]?\*{2})\s*(.+)", line, re.IGNORECASE)
        a_match = re.match(r"^(?:A\d*[:.]?|Ans(?:wer)?[:.]?|\*{2}A\d*[:.]?\*{2})\s*(.+)", line, re.IGNORECASE)

        if q_match:
            if current_q:
                pairs.append({"question": current_q, "answer": current_a or ""})
            current_q = q_match.group(1).strip()
            current_a = None
        elif a_match and current_q:
            current_a = a_match.group(1).strip()
        elif current_q and not current_a:
            current_q += " " + line
        elif current_q and current_a:
            current_a += " " + line

    if current_q:
        pairs.append({"question": current_q, "answer": current_a or ""})

    # Fallback if no explicit Q/A pattern
    if not pairs and lines:
        for idx, line in enumerate(lines[:5], 1):
            clean = re.sub(r"^[-*•\d.]+\s*", "", line)
            pairs.append({"question": clean, "answer": "Refer to concept explanation above."})

    return pairs


def parse_assistant_response(
    response_text: str, study_mode: bool = False
) -> Tuple[str, List[str], Optional[str], Optional[StudySectionResponse]]:
    """Parse assistant text into structured prose, explanation bullets, example, and study sections."""
    sections = parse_sections(response_text)

    # 1. Main prose content
    main_text = sections.get("_main", "").strip()
    if not main_text:
        # If no _main, use problem_understanding or first explanatory text
        main_text = sections.get("problem_understanding") or sections.get("explanation") or ""
        # Strip code blocks from main text so it looks clean
        main_text = _strip_code_blocks(main_text)

    if not main_text:
        main_text = _strip_code_blocks(response_text)
        # Limit to first couple paragraphs
        paras = [p.strip() for p in main_text.split("\n\n") if p.strip()]
        main_text = paras[0] if paras else "Here is the requested solution:"

    # 2. Explanation
    explanation_raw = sections.get("explanation", "")
    explanation_bullets = parse_bullet_list(explanation_raw)
    if not explanation_bullets and not study_mode:
        # Generate clean sentence-level breakdown from non-code text
        clean_text = _strip_code_blocks(response_text)
        candidates = [s.strip() for s in clean_text.split("\n") if s.strip() and not s.startswith("#")]
        explanation_bullets = candidates[:4] if candidates else ["Complete implementation with error handling."]

    # 3. Example / Output
    example = sections.get("example")
    if example:
        example = _strip_code_blocks(example).strip()

    # 4. Study sections
    flowchart_raw = sections.get("flowchart")
    if flowchart_raw:
        # Strip enclosing code fences if model wrapped it in ``` or ```text or ```flowchart
        flowchart_raw = re.sub(r"^```[a-zA-Z0-9_-]*\s*\n", "", flowchart_raw.strip())
        flowchart_raw = re.sub(r"\n\s*```$", "", flowchart_raw.strip()).strip()

    has_study_content = bool(
        study_mode
        or flowchart_raw
        or sections.get("algorithm")
        or sections.get("problem_understanding")
        or sections.get("viva_questions")
    )

    study_response: Optional[StudySectionResponse] = None
    if has_study_content:
        prob_under = sections.get("problem_understanding")
        algo_text = sections.get("algorithm", "")
        algo_bullets = parse_bullet_list(algo_text)
        if not algo_bullets and algo_text:
            algo_bullets = [s.strip() for s in algo_text.splitlines() if s.strip()]

        points_text = sections.get("important_points", "")
        points_bullets = parse_bullet_list(points_text)
        viva_text = sections.get("viva_questions", "")
        viva_pairs = parse_viva_questions(viva_text)

        study_response = StudySectionResponse(
            problem_understanding=prob_under,
            algorithm=algo_bullets,
            flowchart=flowchart_raw,
            important_points=points_bullets,
            viva_questions=viva_pairs,
        )

    return main_text, explanation_bullets, example, study_response
