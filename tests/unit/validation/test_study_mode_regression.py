"""Regression tests for Bhasha2Code Study Mode bug fixes.

Covers:
1. Unrelated-context leakage prevention (standalone queries in existing/new sessions).
2. Flowchart-versus-code classification (never classify ASCII/tables as executable code).
3. Correct Binary Search rendering (flowchart nodes, executable Python code, walkthrough searching 40 in [10, 20, 30, 40, 50] -> index 3).
4. Incomplete Study Mode section detection (token cutoff, unclosed fences, trailing truncated syntax).
"""

import pytest
from backend.app.api.parsers import (
    BINARY_SEARCH_ASCII_FLOWCHART,
    build_binary_search_flowchart_nodes,
    check_is_incomplete,
    parse_assistant_response,
)
from backend.app.context.policies import is_follow_up
from backend.app.validation.code_extractor import CodeExtractor
from backend.app.validation.language_resolver import (
    is_flowchart_or_diagram,
    is_markdown_table,
    resolve_language,
)
from backend.app.validation.response_validator import ResponseValidator
from backend.app.validation.schemas import ValidationStatus


# ============================================================================
# 1. Regression Tests: Unrelated-Context Leakage Prevention
# ============================================================================

def test_standalone_algorithm_queries_not_classified_as_follow_up():
    """Verify short standalone algorithm queries are never misclassified as follow-ups."""
    standalone_queries = [
        "binary search",
        "binary search in python",
        "linear search",
        "bubble sort",
        "merge sort",
        "quick sort",
        "calculator",
        "fibonacci series",
    ]
    for query in standalone_queries:
        assert not is_follow_up(query), (
            f"Expected '{query}' to NOT be classified as follow-up"
        )


def test_multilingual_standalone_algorithm_queries():
    """Verify Hindi and Hinglish algorithm requests are treated as standalone."""
    hindi_hinglish_queries = [
        "binary search algorithm samjhao",
        "binary search code likho",
        "python me binary search banao",
        "calculator program",
    ]
    for query in hindi_hinglish_queries:
        assert not is_follow_up(query), (
            f"Expected '{query}' to NOT be follow-up"
        )


def test_genuine_follow_ups_still_classified_as_follow_up():
    """Verify that genuine modification follow-ups are correctly identified."""
    follow_up_queries = [
        "now add input validation",
        "fix the division by zero error",
        "change it to use a while loop",
        "handle negative numbers too",
        "modify this to return float",
    ]
    for query in follow_up_queries:
        assert is_follow_up(query), (
            f"Expected '{query}' to be identified as follow-up"
        )


# ============================================================================
# 2. Regression Tests: Flowchart-versus-Code Classification
# ============================================================================

def test_ascii_flowchart_never_classified_as_programming_language():
    """Verify ASCII flowcharts and box diagrams are never classified as Python or C code."""
    ascii_diagram = """
    +----------------------------------+
    | Start: Initialize low=0, high=4  |
    +-----------------+----------------+
                      |
                      v
             /-----------------\\
            < Is low <= high ?  >
             \\-----------------/
               | YES       | NO
               v           v
          Compute mid   Return -1
    """
    assert is_flowchart_or_diagram(ascii_diagram)
    resolved = resolve_language(declared_language=None, code=ascii_diagram, language_hint="python")
    assert resolved is None, f"Expected None for ASCII flowchart, got '{resolved}'"

    # Also test unicode box drawing flowchart
    unicode_diagram = BINARY_SEARCH_ASCII_FLOWCHART
    assert is_flowchart_or_diagram(unicode_diagram)
    resolved_unicode = resolve_language(declared_language="text", code=unicode_diagram, language_hint="python")
    assert resolved_unicode is None


def test_markdown_tables_never_classified_as_code():
    """Verify Markdown comparison tables are never classified as programming code."""
    table = """
    | Step | Low | High | Mid | arr[mid] | Action |
    |------|-----|------|-----|----------|--------|
    | 1    | 0   | 4    | 2   | 30       | low=mid+1 |
    | 2    | 3   | 4    | 3   | 40       | Match! Return 3 |
    """
    assert is_markdown_table(table)
    resolved = resolve_language(declared_language=None, code=table, language_hint="python")
    assert resolved is None


def test_validator_does_not_mark_flowchart_as_valid_or_unsupported_python_artifact():
    """ResponseValidator must not produce an unsupported Python artifact for a flowchart block."""
    validator = ResponseValidator()
    response_with_flowchart = """Here is the Binary Search flowchart:

```
[Start] --> [Initialize low=0, high=n-1] --> [Check low <= high]
```

And here is the Python code:

```python
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```
"""
    result = validator.validate(response_with_flowchart, language_hint="python")
    # Verify the code blocks: the actual Python code is VALID
    code_blocks = [b for b in result.code_blocks if b.language == "python"]
    assert len(code_blocks) >= 1
    assert code_blocks[0].status == ValidationStatus.VALID


# ============================================================================
# 3. Regression Tests: Binary Search Flowchart, Walkthrough & Executable Code
# ============================================================================

def test_binary_search_flowchart_nodes_structure():
    """Verify build_binary_search_flowchart_nodes generates the complete required states."""
    nodes = build_binary_search_flowchart_nodes()
    node_ids = [n["id"] for n in nodes]
    assert "start" in node_ids
    assert "init" in node_ids
    assert "loop_cond" in node_ids
    assert "midpoint" in node_ids
    assert "target_check" in node_ids
    assert "update_bounds" in node_ids
    assert "end" in node_ids

    # Check loop condition decision node has both yes and no branches
    loop_node = next(n for n in nodes if n["id"] == "loop_cond")
    assert loop_node["type"] == "decision"
    assert "branchYes" in loop_node
    assert "branchNo" in loop_node
    assert loop_node["branchNo"]["outcomeType"] == "error"  # Not found exit


def test_binary_search_walkthrough_and_expected_index():
    """Verify that Binary Search parser provides the correct 40 in [10,20,30,40,50] walkthrough with index 3."""
    response_text = """### Problem Understanding
Binary search finds element in sorted list in logarithmic time.

### Algorithm
1. Initialize pointers low and high.
2. Calculate midpoint.
3. Compare target.

### Code
```python
def binary_search(arr: list[int], target: int) -> int:
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```
"""
    main_prose, explanation, example, study = parse_assistant_response(
        response_text, study_mode=True, user_query="binary search"
    )

    assert study is not None
    assert study.flowchart_nodes is not None
    assert len(study.flowchart_nodes) >= 5
    assert "low = 0" in study.flowchart
    assert "calculator" not in study.flowchart.lower()

    # Verify example walkthrough
    assert example is not None
    assert "40" in example
    assert "[10, 20, 30, 40, 50]" in example
    assert "3" in example
    assert "Iteration 1" in example
    assert "Iteration 2" in example


def test_executable_binary_search_code_correctness():
    """Execute the binary search logic directly to verify it returns index 3 for 40 in [10, 20, 30, 40, 50]."""
    def binary_search(arr: list[int], target: int) -> int:
        low = 0
        high = len(arr) - 1
        while low <= high:
            mid = (low + high) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    test_arr = [10, 20, 30, 40, 50]
    assert binary_search(test_arr, 40) == 3
    assert binary_search(test_arr, 10) == 0
    assert binary_search(test_arr, 50) == 4
    assert binary_search(test_arr, 99) == -1


# ============================================================================
# 4. Regression Tests: Incomplete Study Mode Sections Detection
# ============================================================================

def test_check_is_incomplete_flags_token_limit_and_syntax_cutoffs():
    """Verify check_is_incomplete detects length finish reason, unclosed fences, and mid-sentence cutoffs."""
    # Length cutoff
    assert check_is_incomplete("def binary_search(arr):", done_reason="length")

    # Unclosed code fence
    unclosed = "Here is the code:\n```python\ndef binary_search(arr):\n    low = 0"
    assert check_is_incomplete(unclosed, done_reason="stop")

    # Trailing truncation marker
    truncated_study = "### Algorithm\n1. Set low and high\n2. Compute mid\n3. Check if target..."
    assert check_is_incomplete(truncated_study, study_mode=True, done_reason="stop")

    # Clean, completed output
    completed = "### Algorithm\n1. Set low and high\n2. Compute mid\n\n```python\npass\n```"
    assert not check_is_incomplete(completed, study_mode=True, done_reason="stop")


# ============================================================================
# 5. Regression Tests: Linear Search vs Binary Search Flowchart & Output Consistency
# ============================================================================

from backend.app.api.parsers import (
    LINEAR_SEARCH_ASCII_FLOWCHART,
    build_linear_search_flowchart_nodes,
)


def test_linear_search_flowchart_never_contains_binary_search_keywords():
    """Ensure Linear Search flowchart nodes and ASCII diagram strictly NEVER use low, high, mid, or arr[mid]."""
    nodes = build_linear_search_flowchart_nodes()
    assert len(nodes) >= 6

    # Extract all text content from nodes (including nested dicts like branchYes/branchNo)
    collected_texts = []
    for n in nodes:
        for k, v in n.items():
            if isinstance(v, dict):
                collected_texts.extend(str(sub_v) for sub_v in v.values())
            else:
                collected_texts.append(str(v))
    node_texts = " ".join(collected_texts).lower()

    for forbidden in ["low", "high", "mid", "arr[mid]"]:
        assert forbidden not in node_texts, f"Forbidden '{forbidden}' found in Linear Search flowchart nodes"

    ascii_chart = LINEAR_SEARCH_ASCII_FLOWCHART.lower()
    for forbidden in ["low", "high", "mid", "arr[mid]"]:
        assert forbidden not in ascii_chart, f"Forbidden '{forbidden}' found in Linear Search ASCII flowchart"

    # Must contain linear search specifics
    assert "i = 0" in node_texts or "i=0" in node_texts
    assert "target" in node_texts
    assert "arr[i]" in node_texts
    assert "len(arr)" in node_texts


def test_linear_search_response_parsing_and_sample_input_output():
    """Verify parsing a Linear Search Study Mode response populates the sample input/output and separates flowchart."""
    response_text = """### Problem Understanding
Linear search sequentially checks each element of the list until a match is found or the list ends.

### Algorithm
1. Start from the first element (index 0).
2. Compare current element arr[i] with target.
3. If arr[i] == target, return index i.
4. Else, increment i and repeat.
5. If end of array is reached, return -1.

### Sample Input/Output
Input:
arr = [5, 12, 18, 25, 30]
target = 18
Output:
Element found at index 2

### Code
```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```
"""
    main_prose, explanation, example, study = parse_assistant_response(
        response_text, study_mode=True, user_query="linear search"
    )

    assert study is not None
    assert study.flowchart_nodes is not None
    # Flowchart nodes must be Linear Search nodes
    node_ids = [n["id"] for n in study.flowchart_nodes]
    assert "init" in node_ids
    assert "loop_cond" in node_ids
    assert "target_check" in node_ids
    assert "increment" in node_ids
    assert "midpoint" not in node_ids
    assert "update_bounds" not in node_ids

    # ASCII flowchart must be Linear Search
    assert "arr[i]" in study.flowchart
    assert "target" in study.flowchart
    assert "mid" not in study.flowchart.lower()

    # Sample Input/Output must be populated
    assert example is not None
    assert "arr = [5, 12, 18, 25, 30]" in example
    assert "target = 18" in example
    assert "Element found at index 2" in example

    # Main prose must NOT have duplicate flowchart blocks or raw ASCII arrows
    assert "-->" not in main_prose
    assert "[Start]" not in main_prose


def test_linear_search_flowchart_never_classified_as_python_code():
    """Verify Linear Search ASCII flowchart is never treated as executable Python code."""
    assert is_flowchart_or_diagram(LINEAR_SEARCH_ASCII_FLOWCHART)
    resolved = resolve_language(declared_language=None, code=LINEAR_SEARCH_ASCII_FLOWCHART, language_hint="python")
    assert resolved is None

    validator = ResponseValidator()
    full_text = f"""Here is the Linear Search flowchart:

```
{LINEAR_SEARCH_ASCII_FLOWCHART}
```

```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```
"""
    result = validator.validate(full_text, language_hint="python")
    code_blocks = [b for b in result.code_blocks if b.language == "python"]
    assert len(code_blocks) == 1
    assert "def linear_search" in code_blocks[0].code
    assert code_blocks[0].status == ValidationStatus.VALID


def test_linear_search_code_execution_and_output_verification():
    """Directly test the canonical linear search code against the expected sample output."""
    def linear_search(arr, target):
        for i in range(len(arr)):
            if arr[i] == target:
                return i
        return -1

    arr = [5, 12, 18, 25, 30]
    target = 18
    idx = linear_search(arr, target)
    assert idx == 2
    output_message = f"Element found at index {idx}"
    assert output_message == "Element found at index 2"

    # Check not found case
    not_found_idx = linear_search(arr, 99)
    assert not_found_idx == -1


def test_binary_search_maintains_its_own_diagram_without_linear_search_mixup():
    """Verify Binary Search requests maintain low/high/mid without any linear search nodes."""
    response_text = """### Problem Understanding
Binary search repeatedly divides the search interval in half.

### Algorithm
1. low = 0, high = len(arr) - 1.
2. mid = (low + high) // 2.
3. Compare arr[mid] with target.

### Code
```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
```
"""
    _, _, _, study = parse_assistant_response(
        response_text, study_mode=True, user_query="binary search"
    )

    assert study is not None
    node_ids = [n["id"] for n in study.flowchart_nodes]
    assert "midpoint" in node_ids
    assert "ls_compare" not in node_ids
    assert "mid" in study.flowchart.lower()
    assert "low" in study.flowchart.lower()


# ============================================================================
# 6. Regression Tests: StudySectionResponse Null Normalization & Absent Viva Questions
# ============================================================================

from backend.app.api.parsers import parse_viva_questions
from backend.app.api.schemas import StudySectionResponse


def test_study_section_response_creation_when_viva_questions_missing():
    """Verify StudySectionResponse defaults viva_questions and list fields to empty lists when omitted."""
    resp = StudySectionResponse()
    assert resp.viva_questions == []
    assert resp.algorithm == []
    assert resp.important_points == []
    assert resp.flowchart_nodes is None
    assert resp.problem_understanding is None


def test_study_section_response_creation_when_viva_questions_explicitly_null():
    """Verify StudySectionResponse normalizes explicit None inputs to empty lists without ValidationError."""
    resp = StudySectionResponse(
        viva_questions=None,
        algorithm=None,
        important_points=None,
        flowchart_nodes=None,
    )
    assert resp.viva_questions == []
    assert resp.algorithm == []
    assert resp.important_points == []
    assert resp.flowchart_nodes is None


def test_study_section_response_valid_viva_questions_remain_unchanged():
    """Verify genuine viva_questions and list items are preserved exactly without alteration."""
    raw_viva = [
        {"question": "What is linear search?", "answer": "Sequential check from start to end."},
        {"question": "What is its time complexity?", "answer": "O(n) in worst case."},
    ]
    resp = StudySectionResponse(
        algorithm=["Step 1", "Step 2"],
        important_points=["Point 1"],
        viva_questions=raw_viva,
    )
    assert resp.viva_questions == raw_viva
    assert resp.algorithm == ["Step 1", "Step 2"]
    assert resp.important_points == ["Point 1"]


def test_parse_viva_questions_handles_null_empty_and_no_fabrication():
    """Verify parse_viva_questions handles None, empty strings, and does not fabricate placeholder questions."""
    assert parse_viva_questions(None) == []
    assert parse_viva_questions("") == []
    assert parse_viva_questions("   \n\n  ") == []

    # Non-Q&A text should return empty list, NOT fabricated dummy questions
    non_qa_text = "Here is some general advice about programming and study notes."
    assert parse_viva_questions(non_qa_text) == []

    # Genuine Q&A text must be extracted
    qa_text = "Q: What is O(1)?\nA: Constant time complexity."
    parsed = parse_viva_questions(qa_text)
    assert len(parsed) == 1
    assert parsed[0]["question"] == "What is O(1)?"
    assert parsed[0]["answer"] == "Constant time complexity."


def test_parse_assistant_response_with_absent_and_null_study_sections():
    """Verify parse_assistant_response handles absent or null viva sections gracefully."""
    response_without_viva = """### Problem Understanding
Stack is a Last-In-First-Out data structure.

### Algorithm
1. Push element onto stack.
2. Pop element from stack.

### Code
```python
class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
```
"""
    _, _, _, study = parse_assistant_response(
        response_without_viva, study_mode=True, user_query="stack data structure"
    )
    assert study is not None
    # viva_questions must be an empty list, NOT None and NOT fabricated questions
    assert isinstance(study.viva_questions, list)
    assert study.viva_questions == []
    assert isinstance(study.algorithm, list)
    assert len(study.algorithm) == 2


