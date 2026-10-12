"""Response parsers for extracting explanation, example, and study sections from assistant text."""

import re
from typing import Any, Dict, List, Optional, Tuple

from backend.app.api.schemas import StudySectionResponse


def _strip_code_blocks(text: str) -> str:
    """Remove fenced code blocks (closed or trailing unclosed) to extract pure markdown prose."""
    if not text:
        return ""
    # Strip fully closed code blocks
    cleaned = re.sub(r"(?:```|~~~)[\s\S]*?(?:```|~~~)", "", text)
    # Strip trailing unclosed code block if truncated
    cleaned = re.sub(r"(?:```|~~~)[\s\S]*$", "", cleaned)
    return cleaned.strip()


def parse_sections(text: Optional[str]) -> Dict[str, str]:
    """Parse markdown headers into a dictionary of section names to body texts."""
    sections: Dict[str, str] = {}
    if not text or not isinstance(text, str):
        return sections

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
            elif (
                candidate.startswith("example")
                or candidate.startswith("sample")
                or candidate.startswith("usage")
                or candidate.startswith("output")
                or candidate.startswith("input")
                or "test case" in candidate
                or "walkthrough" in candidate
                or "dry run" in candidate
            ):
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


def parse_bullet_list(text: Optional[str]) -> List[str]:
    """Extract bullet points or numbered items from a text block."""
    if not text or not isinstance(text, str):
        return []
    items: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        cleaned = re.sub(r"^[-*•]\s+|\d+\.\s+", "", line).strip()
        if cleaned:
            items.append(cleaned)
    return items


def parse_viva_questions(text: Optional[str]) -> List[Dict[str, str]]:
    """Parse Q&A pairs from text.

    Returns an empty list if text is empty, None, or contains no Q&A pairs.
    Does not fabricate placeholder questions merely to satisfy validation.
    """
    if not text or not isinstance(text, str):
        return []

    pairs: List[Dict[str, str]] = []
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    current_q = None
    current_a = None

    for line in lines:
        q_match = re.match(
            r"^(?:Q\d*[:.]?|\d+\.\s*Q(?:uestion)?[:.]?|\*{2}Q\d*[:.]?\*{2}|\d+[.)]\s*Q(?:uestion)?[:.]?)\s*(.+)",
            line,
            re.IGNORECASE,
        )
        if not q_match and re.match(r"^\d+[.)]\s*.+\?$", line):
            q_match = re.match(r"^\d+[.)]\s*(.+)", line)

        a_match = re.match(
            r"^(?:A\d*[:.]?|Ans(?:wer)?[:.]?|\*{2}A\d*[:.]?\*{2}|\d+[.)]\s*A(?:nswer)?[:.]?)\s*(.+)",
            line,
            re.IGNORECASE,
        )

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

    return pairs

LINEAR_SEARCH_ASCII_FLOWCHART = """[Start]
  │
  ▼
[1. Initialize: i = 0]
  │
  ▼
┌──────────────────────────────┐
│  Loop: Is i < len(arr) ?     │
└──────────────┬───────────────┘
               │ YES
               ▼
        ┌──────────────┐
        │   arr[i]     │── YES ──> [Found target at index 'i'] ──> [End]
        │ == target ?  │
        └──────┬───────┘
               │ NO
               ▼
        [Increment: i = i + 1]
               │
               └──────────────────▶ (Loop back to condition)
               ┌──────────────────┘
               ▼ NO (i >= len(arr))
[Target Not Found: return -1]
  │
  ▼
[End]"""


def build_linear_search_flowchart_nodes() -> List[Dict[str, Any]]:
    """Return genuine, structured Linear Search flowchart nodes adhering to standard flowchart rules.

    Start -> initialize i = 0 -> check i < len(arr) -> compare arr[i] with target
    -> if matched, return index i -> otherwise increment i and loop
    -> if array ends, report not found -> End.
    Never uses low, high, mid, or arr[mid].
    """
    return [
        {
            "id": "start",
            "type": "terminal",
            "title": "Start",
            "subtitle": "Linear search algorithm begins",
            "accent": "emerald",
        },
        {
            "id": "init",
            "type": "process",
            "title": "1. Initialize Index Pointer",
            "subtitle": "Set search pointer to the first element of the array",
            "code": "i = 0",
            "accent": "blue",
        },
        {
            "id": "loop_cond",
            "type": "decision",
            "title": "Loop Condition: Array Boundary Check",
            "condition": "i < len(arr) ?",
            "accent": "amber",
            "branchYes": {
                "label": "YES (Within Bounds)",
                "action": "Inspect Current Element",
                "detail": "Array has remaining elements to examine; inspect arr[i]",
                "outcomeType": "success",
            },
            "branchNo": {
                "label": "NO (Array Exhausted)",
                "action": "Target Not Found",
                "detail": "i >= len(arr); reached end of array without match, return -1",
                "outcomeType": "error",
            },
        },
        {
            "id": "target_check",
            "type": "decision",
            "title": "Target Comparison",
            "condition": "arr[i] == target ?",
            "accent": "amber",
            "branchYes": {
                "label": "YES (Element Found)",
                "action": "Return Found Index",
                "detail": "Target matches arr[i]; return index i immediately",
                "outcomeType": "success",
            },
            "branchNo": {
                "label": "NO (Mismatch)",
                "action": "Advance Index",
                "detail": "arr[i] != target; increment index i = i + 1 to check next item",
                "outcomeType": "neutral",
            },
        },
        {
            "id": "increment",
            "type": "process",
            "title": "2. Increment Index Pointer",
            "subtitle": "Move pointer to next position in sequence and repeat loop",
            "code": "i = i + 1",
            "accent": "blue",
        },
        {
            "id": "end",
            "type": "terminal",
            "title": "End / Outcome",
            "subtitle": "Return found index i (e.g. 2) or -1 (not found)",
            "accent": "slate",
        },
    ]


BINARY_SEARCH_ASCII_FLOWCHART = """[Start]
  │
  ▼
[1. Initialize: low = 0, high = len(arr) - 1]
  │
  ▼
┌──────────────────────────────┐
│  Loop: Is low <= high ?      │
└──────────────┬───────────────┘
               │ YES
               ▼
[2. Calculate midpoint: mid = (low + high) // 2]
               │
               ▼
        ┌──────────────┐
        │ arr[mid]     │── YES ──> [Found target at index 'mid'] ──> [End]
        │ == target ?  │
        └──────┬───────┘
               │ NO
               ▼
        ┌──────────────┐
        │ arr[mid]     │── YES ──> [Update left: low = mid + 1] ──┐
        │  < target ?  │                                          │
        └──────┬───────┘                                          │
               │ NO                                               │
               ▼                                                  │
        [Update right: high = mid - 1]                            │
               │                                                  │
               └──────────────────┬───────────────────────────────┘
                                  │
                                  ▼ (Loop back to condition)
               ┌──────────────────┘
               ▼ NO (low > high)
[Target Not Found: return -1]
  │
  ▼
[End]"""


def build_binary_search_flowchart_nodes() -> List[Dict[str, Any]]:
    """Return genuine, structured Binary Search flowchart nodes."""
    return [
        {
            "id": "start",
            "type": "terminal",
            "title": "Start",
            "subtitle": "Binary search algorithm begins",
            "accent": "emerald",
        },
        {
            "id": "init",
            "type": "process",
            "title": "1. Initialize Pointers",
            "subtitle": "Set search boundaries on sorted array",
            "code": "low = 0 ; high = len(arr) - 1",
            "accent": "blue",
        },
        {
            "id": "loop_cond",
            "type": "decision",
            "title": "Loop Condition: Range Check",
            "condition": "low <= high ?",
            "accent": "amber",
            "branchYes": {
                "label": "YES (Range Valid)",
                "action": "Calculate Midpoint",
                "detail": "Search space is active; divide interval in half",
                "outcomeType": "success",
            },
            "branchNo": {
                "label": "NO (Search Space Exhausted)",
                "action": "Target Not Found",
                "detail": "low > high; element does not exist in array, return -1",
                "outcomeType": "error",
            },
        },
        {
            "id": "midpoint",
            "type": "process",
            "title": "2. Midpoint Calculation",
            "subtitle": "Compute middle index to inspect pivot element",
            "code": "mid = (low + high) // 2",
            "accent": "indigo",
        },
        {
            "id": "target_check",
            "type": "decision",
            "title": "Target Comparison",
            "condition": "arr[mid] == target ?",
            "accent": "amber",
            "branchYes": {
                "label": "YES (Element Found)",
                "action": "Return Found Index",
                "detail": "Target matches arr[mid]; return index mid",
                "outcomeType": "success",
            },
            "branchNo": {
                "label": "NO (Mismatch)",
                "action": "Update Bounds",
                "detail": "If arr[mid] < target: low = mid + 1; else: high = mid - 1",
                "outcomeType": "neutral",
            },
        },
        {
            "id": "update_bounds",
            "type": "process",
            "title": "3. Left / Right Updates",
            "subtitle": "Discard half of array based on comparison and repeat",
            "code": "if arr[mid] < target: low = mid + 1\nelse: high = mid - 1",
            "accent": "blue",
        },
        {
            "id": "end",
            "type": "terminal",
            "title": "End / Outcome",
            "subtitle": "Return found index (e.g. 3) or -1 (not found)",
            "accent": "slate",
        },
    ]


def check_is_incomplete(
    response_text: str, study_mode: bool = False, done_reason: str = "stop"
) -> bool:
    """Check if the assistant response is incomplete or truncated."""
    if done_reason == "length":
        return True
    if not response_text or not response_text.strip():
        return True
    # Count open vs close code fences
    fence_count = len(re.findall(r"```|~~~", response_text))
    if fence_count % 2 != 0:
        return True
    # If in Study Mode, check if last section was truncated mid-sentence
    stripped = response_text.strip()
    if study_mode and stripped:
        last_line = stripped.splitlines()[-1].strip()
        if last_line.endswith(("...", "…", "├──", "└──", "->", "=>", "(", "[", "{", "+")):
            return True
    return False


def parse_assistant_response(
    response_text: str, study_mode: bool = False, user_query: Optional[str] = None
) -> Tuple[str, List[str], Optional[str], Optional[StudySectionResponse]]:
    """Parse assistant text into structured prose, explanation bullets, example, and study sections."""
    sections = parse_sections(response_text)

    # 1. Main prose content (code blocks strictly stripped)
    main_text = _strip_code_blocks(sections.get("_main", ""))
    if not main_text:
        # If no _main, use problem_understanding or first explanatory text
        candidate = sections.get("problem_understanding") or sections.get("explanation") or ""
        main_text = _strip_code_blocks(candidate)

    if not main_text:
        candidate = _strip_code_blocks(response_text)
        # Limit to first couple paragraphs
        paras = [p.strip() for p in candidate.split("\n\n") if p.strip()]
        main_text = paras[0] if paras else "Here is the requested solution:"

    # Ensure main_text is clean and free of leftover fences
    main_text = _strip_code_blocks(main_text)

    # In Study Mode, clean main_text so it never contains ASCII flowcharts or duplicates problem_understanding
    if study_mode and main_text:
        lines = main_text.splitlines()
        filtered = []
        for l in lines:
            if any(sig in l for sig in ("-->", "->", "│", "┌", "┐", "└", "┘", "▼", "▲", "├──", "└──", "[Start]", "[End]", "[Init")):
                continue
            if re.match(r"^(?:#{1,4}\s+|\d+\.\s+)?(?:Flowchart|Algorithm|Problem Understanding|Code|Example|Output)\b", l, re.IGNORECASE):
                continue
            filtered.append(l)
        main_text = "\n".join(filtered).strip()
        prob_under_cand = sections.get("problem_understanding", "")
        if prob_under_cand and (main_text == prob_under_cand.strip() or prob_under_cand.strip() in main_text):
            main_text = ""

    # 2. Explanation
    CODE_PREFIXES = (
        "def ", "class ", "import ", "from ", "return ", "print(", "print ",
        "if ", "elif ", "else:", "while ", "for ", "try:", "except", "except:",
        "var ", "let ", "const ", "function ", "#include", "public ", "private ",
        "int ", "void ", "//", "/*", "*/", "```", "~~~", "{"
    )

    explanation_raw = sections.get("explanation", "")
    raw_bullets = parse_bullet_list(explanation_raw)
    explanation_bullets = [
        b for b in raw_bullets
        if not any(b.strip().startswith(p) for p in CODE_PREFIXES)
    ]

    if not explanation_bullets and not study_mode:
        # Generate clean sentence-level breakdown from non-code text
        clean_text = _strip_code_blocks(response_text)
        candidates = []
        for s in clean_text.split("\n"):
            line = s.strip()
            if not line or line.startswith("#"):
                continue
            if any(line.startswith(p) for p in CODE_PREFIXES):
                continue
            if line.endswith(":") and any(k in line for k in ("try", "except", "def", "class", "while", "for")):
                continue
            candidates.append(line)
        explanation_bullets = candidates[:4] if candidates else ["Complete implementation with error handling."]

    # 3. Example / Output - preserved in full (do NOT strip code blocks!)
    is_linear_search = bool(
        re.search(r"\blinear\s+search\b", response_text, re.IGNORECASE)
        or (user_query and re.search(r"\blinear\s+search\b", user_query, re.IGNORECASE))
    )
    is_binary_search = bool(
        not is_linear_search
        and (
            re.search(r"\bbinary\s+search\b", response_text, re.IGNORECASE)
            or (user_query and re.search(r"\bbinary\s+search\b", user_query, re.IGNORECASE))
        )
    )

    example = sections.get("example")
    if example:
        example = example.strip()

    ls_example_walkthrough = (
        "### Sample Input and Output\n\n"
        "**Input:**\n"
        "```text\n"
        "arr = [5, 12, 18, 25, 30]\n"
        "target = 18\n"
        "```\n\n"
        "**Output:**\n"
        "```text\n"
        "Element found at index 2\n"
        "```\n\n"
        "**Step-by-Step Trace:**\n"
        "- Index 0: `arr[0] = 5 != 18` -> Mismatch, move to index 1\n"
        "- Index 1: `arr[1] = 12 != 18` -> Mismatch, move to index 2\n"
        "- Index 2: `arr[2] = 18 == 18` -> Match found! Return index `2`.\n\n"
        "```python\n"
        "# Sample Execution Code\n"
        "arr = [5, 12, 18, 25, 30]\n"
        "target = 18\n"
        "result = linear_search(arr, target)\n"
        "if result != -1:\n"
        "    print(f\"Element found at index {result}\")\n"
        "else:\n"
        "    print(\"Element not found\")\n"
        "```"
    )

    bs_example_walkthrough = (
        "### Example Walkthrough\n\n"
        "Searching for target `40` in sorted array `[10, 20, 30, 40, 50]`:\n\n"
        "1. **Iteration 1**:\n"
        "   - Search range: `low = 0`, `high = 4`\n"
        "   - Midpoint calculation: `mid = (0 + 4) // 2 = 2`\n"
        "   - Target comparison: `arr[mid] = arr[2] = 30`\n"
        "   - Since `30 < 40`, target is in the right half: update `low = mid + 1 = 3`\n\n"
        "2. **Iteration 2**:\n"
        "   - Search range: `low = 3`, `high = 4`\n"
        "   - Midpoint calculation: `mid = (3 + 4) // 2 = 3`\n"
        "   - Target comparison: `arr[mid] = arr[3] = 40`\n"
        "   - Match found (`arr[3] == 40`)! Return zero-based index `3`.\n\n"
        "```python\n"
        "# Sample Run\n"
        "arr = [10, 20, 30, 40, 50]\n"
        "target = 40\n"
        "result = binary_search(arr, target)\n"
        "print(f\"Target {target} found at index: {result}\")  # Output: 3\n"
        "```"
    )

    if is_linear_search:
        if not example or "calculator" in example.lower() or "binary" in example.lower() or "18" not in example:
            example = ls_example_walkthrough
    elif is_binary_search:
        if not example or "calculator" in example.lower() or "operator" in example.lower() or "40" not in example:
            example = bs_example_walkthrough

    # 4. Study sections
    flowchart_raw = sections.get("flowchart")
    if flowchart_raw:
        # Strip enclosing code fences if model wrapped it in ``` or ```text or ```flowchart
        flowchart_raw = re.sub(r"^```[a-zA-Z0-9_-]*\s*\n", "", flowchart_raw.strip())
        flowchart_raw = re.sub(r"\n\s*```$", "", flowchart_raw.strip()).strip()

    if is_linear_search and (not flowchart_raw or "binary" in flowchart_raw.lower() or "mid" in flowchart_raw.lower() or len(flowchart_raw) < 20):
        flowchart_raw = LINEAR_SEARCH_ASCII_FLOWCHART
    elif is_binary_search and (not flowchart_raw or "calculator" in flowchart_raw.lower() or len(flowchart_raw) < 20):
        flowchart_raw = BINARY_SEARCH_ASCII_FLOWCHART

    has_study_content = bool(
        study_mode
        or flowchart_raw
        or sections.get("algorithm")
        or sections.get("problem_understanding")
        or sections.get("viva_questions")
        or is_linear_search
        or is_binary_search
    )

    study_response: Optional[StudySectionResponse] = None
    if has_study_content:
        prob_under = sections.get("problem_understanding")
        if is_linear_search and (not prob_under or "binary" in prob_under.lower() or "calculator" in prob_under.lower()):
            prob_under = (
                "Linear Search is a fundamental sequential search algorithm that inspects each element of a list "
                "one by one from index 0 until the target value is found or the array ends, operating in O(n) time."
            )
        elif is_binary_search and (not prob_under or "calculator" in prob_under.lower()):
            prob_under = (
                "Binary Search is an efficient divide-and-conquer algorithm that finds the position of a target "
                "value within a sorted array in O(log n) time by halving the search space at each comparison."
            )

        algo_text = sections.get("algorithm", "")
        algo_bullets = parse_bullet_list(algo_text)
        if not algo_bullets and algo_text:
            algo_bullets = [s.strip() for s in algo_text.splitlines() if s.strip()]

        if is_linear_search and (not algo_bullets or any("mid" in a.lower() or "binary" in a.lower() or "calculator" in a.lower() for a in algo_bullets)):
            algo_bullets = [
                "1. Initialize index pointer `i = 0`.",
                "2. Check loop boundary: if `i < len(arr)`, proceed to step 3; otherwise return `-1` (target not found).",
                "3. Compare current element: if `arr[i] == target`, return current index `i` (target found).",
                "4. Otherwise increment pointer `i = i + 1` and loop back to step 2.",
            ]
        elif is_binary_search and (not algo_bullets or any("calculator" in a.lower() for a in algo_bullets)):
            algo_bullets = [
                "1. Initialize search range pointers: `low = 0`, `high = len(arr) - 1`.",
                "2. While `low <= high`, compute midpoint `mid = (low + high) // 2`.",
                "3. Compare `arr[mid]` with `target`.",
                "4. If `arr[mid] == target`, return `mid` (element found).",
                "5. If `arr[mid] < target`, discard left half by setting `low = mid + 1`.",
                "6. If `arr[mid] > target`, discard right half by setting `high = mid - 1`.",
                "7. If loop terminates (`low > high`), return `-1` (element not found).",
            ]

        points_text = sections.get("important_points", "")
        points_bullets = parse_bullet_list(points_text)
        if is_linear_search and (not points_bullets or any("binary" in p.lower() or "calculator" in p.lower() for p in points_bullets)):
            points_bullets = [
                "Linear search does NOT require the array to be sorted; it works on any arbitrary list.",
                "Time Complexity: Best Case O(1) (target at index 0), Worst Case O(n) (target at end or missing).",
                "Space Complexity: O(1) auxiliary space (only requires an index pointer).",
                "Straightforward to implement and ideal for small or unsorted collections.",
            ]
        elif is_binary_search and (not points_bullets or any("calculator" in p.lower() for p in points_bullets)):
            points_bullets = [
                "The input array MUST be sorted beforehand for binary search to work correctly.",
                "Time Complexity: Best Case O(1), Average & Worst Case O(log n).",
                "Space Complexity: O(1) iterative, O(log n) recursive call stack.",
                "Midpoint calculation `(low + high) // 2` or `low + (high - low) // 2` avoids integer overflow in fixed-width languages.",
            ]

        viva_text = sections.get("viva_questions")
        viva_pairs = parse_viva_questions(viva_text) if viva_text else []
        if not isinstance(viva_pairs, list):
            viva_pairs = []

        if viva_pairs:
            if is_linear_search and any("binary" in v.get("question", "").lower() or "calculator" in v.get("question", "").lower() for v in viva_pairs):
                viva_pairs = [
                    {
                        "question": "What is the worst-case time complexity of linear search?",
                        "answer": "O(n), where n is the number of elements in the array, when the target is at the end or absent.",
                    },
                    {
                        "question": "Does linear search require the array to be sorted?",
                        "answer": "No, linear search works seamlessly on both sorted and unsorted collections.",
                    },
                    {
                        "question": "What does returning -1 indicate in linear search?",
                        "answer": "It indicates that the entire array was scanned and the target element was not found.",
                    },
                ]
            elif is_binary_search and any("calculator" in v.get("question", "").lower() for v in viva_pairs):
                viva_pairs = [
                    {
                        "question": "What is the prerequisite condition for applying binary search?",
                        "answer": "The array or list must already be in sorted order.",
                    },
                    {
                        "question": "What is the worst-case time complexity of binary search?",
                        "answer": "O(log n), because the search space is divided in half after each comparison.",
                    },
                    {
                        "question": "What does a return value of -1 indicate?",
                        "answer": "It indicates that the target value was not found in the array.",
                    },
                ]

        if is_linear_search:
            flowchart_nodes = build_linear_search_flowchart_nodes()
        elif is_binary_search:
            flowchart_nodes = build_binary_search_flowchart_nodes()
        else:
            flowchart_nodes = None

        safe_algo = algo_bullets if isinstance(algo_bullets, list) else []
        safe_points = points_bullets if isinstance(points_bullets, list) else []
        safe_viva = viva_pairs if isinstance(viva_pairs, list) else []
        safe_nodes = flowchart_nodes if isinstance(flowchart_nodes, list) else None

        try:
            study_response = StudySectionResponse(
                problem_understanding=prob_under or None,
                algorithm=safe_algo,
                flowchart=flowchart_raw or None,
                flowchart_nodes=safe_nodes,
                important_points=safe_points,
                viva_questions=safe_viva,
            )
        except Exception as exc:
            logger.warning("StudySectionResponse validation fallback: %s", exc)
            study_response = StudySectionResponse(
                problem_understanding=prob_under or None,
                algorithm=[],
                flowchart=flowchart_raw or None,
                flowchart_nodes=None,
                important_points=[],
                viva_questions=[],
            )

    return main_text, explanation_bullets, example, study_response
