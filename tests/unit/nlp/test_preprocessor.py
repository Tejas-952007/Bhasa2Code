import pytest
from backend.app.nlp.preprocessing.text_preprocessor import TextPreprocessor
from backend.app.nlp.schemas import CodeSegment, PreprocessedText


@pytest.fixture
def preprocessor() -> TextPreprocessor:
    return TextPreprocessor()


def test_basic_english(preprocessor: TextPreprocessor):
    res = preprocessor.preprocess("hello world")
    assert res.original_text == "hello world"
    assert res.normalized_text == "hello world"
    assert res.text_segments == ["hello world"]
    assert res.code_segments == []
    assert res.is_empty is False
    assert res.has_code is False


def test_marathi_preservation(preprocessor: TextPreprocessor):
    raw = "Python मध्ये calculator तयार कर"
    res = preprocessor.preprocess(raw)
    assert res.original_text == raw
    assert res.normalized_text == raw
    assert "मध्ये" in res.normalized_text
    assert "तयार" in res.normalized_text
    assert "Python" in res.normalized_text
    assert "calculator" in res.normalized_text


def test_hindi_preservation(preprocessor: TextPreprocessor):
    raw = "Python में calculator बनाओ"
    res = preprocessor.preprocess(raw)
    assert res.original_text == raw
    assert res.normalized_text == raw
    assert "में" in res.normalized_text
    assert "बनाओ" in res.normalized_text


def test_hinglish_preservation(preprocessor: TextPreprocessor):
    raw = "Python me calculator bana"
    res = preprocessor.preprocess(raw)
    assert res.normalized_text == "Python me calculator bana"
    assert res.text_segments == ["Python me calculator bana"]


def test_marathi_english_code_mixed(preprocessor: TextPreprocessor):
    raw = "हा Python code explain कर"
    res = preprocessor.preprocess(raw)
    assert res.normalized_text == "हा Python code explain कर"
    assert "हा" in res.normalized_text
    assert "code" in res.normalized_text
    assert "explain" in res.normalized_text


def test_hindi_english_code_mixed(preprocessor: TextPreprocessor):
    raw = "ye Python code explain karo"
    res = preprocessor.preprocess(raw)
    assert res.normalized_text == "ye Python code explain karo"


def test_whitespace_normalization(preprocessor: TextPreprocessor):
    raw = "   Python   madhe   calculator   bana  "
    res = preprocessor.preprocess(raw)
    assert res.original_text == raw
    assert res.normalized_text == "Python madhe calculator bana"


def test_unicode_nfc_normalization(preprocessor: TextPreprocessor):
    # Combining characters normalized canonically
    raw = "हा code optimize कसा करायचा?"
    res = preprocessor.preprocess(raw)
    assert res.normalized_text == raw
    assert res.text_segments == [raw]


def test_code_fence_extraction(preprocessor: TextPreprocessor):
    raw = '```python\nprint("Hello")\n```'
    res = preprocessor.preprocess(raw)
    assert len(res.code_segments) == 1
    assert res.code_segments[0].content == 'print("Hello")'
    assert res.code_segments[0].language_hint == "python"
    assert res.has_code is True


def test_code_plus_multilingual_text(preprocessor: TextPreprocessor):
    raw = 'हा code slow का आहे?\n\n```python\nfor i in range(1000000):\n    print(i)\n```'
    res = preprocessor.preprocess(raw)
    assert len(res.text_segments) == 1
    assert res.text_segments[0] == "हा code slow का आहे?"
    assert len(res.code_segments) == 1
    assert res.code_segments[0].language_hint == "python"
    assert res.code_segments[0].content == "for i in range(1000000):\n    print(i)"
    assert res.classifier_text == "हा code slow का आहे?"
    assert res.has_code is True


def test_code_indentation_preserved(preprocessor: TextPreprocessor):
    raw = 'if x:\n    if y:\n        print("yes")'
    res = preprocessor.preprocess(raw)
    # Indentation preserved exactly
    assert "    if y:" in res.normalized_text
    assert '        print("yes")' in res.normalized_text


def test_multiline_raw_code(preprocessor: TextPreprocessor):
    code = "def add(a, b):\n    return a + b"
    res = preprocessor.preprocess(code)
    assert len(res.code_segments) == 1
    assert res.code_segments[0].content == code
    assert res.normalized_text == code


def test_stack_trace_preserved(preprocessor: TextPreprocessor):
    trace = (
        'Traceback (most recent call last):\n'
        '  File "main.py", line 12, in <module>\n'
        '    solve()\n'
        "NameError: name 'solve' is not defined"
    )
    res = preprocessor.preprocess(trace)
    assert len(res.code_segments) == 1
    assert res.code_segments[0].content == trace
    assert res.normalized_text == trace


def test_punctuation_and_symbols_preserved(preprocessor: TextPreprocessor):
    raw = "Why is this code slow??? x += 1; arr[0] = {'a': 10} /* comment */"
    res = preprocessor.preprocess(raw)
    assert "???" in res.normalized_text
    assert "+=" in res.normalized_text
    assert "{'a': 10}" in res.normalized_text


def test_urls_preserved(preprocessor: TextPreprocessor):
    raw = "API endpoint https://example.com/api/v1?token=xyz#docs check kar"
    res = preprocessor.preprocess(raw)
    assert "https://example.com/api/v1?token=xyz#docs" in res.normalized_text


def test_file_paths_preserved(preprocessor: TextPreprocessor):
    raw = "file /home/user/project/data.txt and ./config.json read kar"
    res = preprocessor.preprocess(raw)
    assert "/home/user/project/data.txt" in res.normalized_text
    assert "./config.json" in res.normalized_text


def test_error_messages_preserved(preprocessor: TextPreprocessor):
    err = "NameError: name 'x' is not defined"
    res = preprocessor.preprocess(err)
    assert err in res.normalized_text


def test_empty_input(preprocessor: TextPreprocessor):
    res = preprocessor.preprocess("")
    assert res.original_text == ""
    assert res.normalized_text == ""
    assert res.text_segments == []
    assert res.code_segments == []
    assert res.is_empty is True
    assert res.has_code is False


def test_whitespace_only_input(preprocessor: TextPreprocessor):
    res = preprocessor.preprocess("    \n\t  \n  ")
    assert res.normalized_text == ""
    assert res.is_empty is True
    assert res.text_segments == []


def test_numbers_only_input(preprocessor: TextPreprocessor):
    res = preprocessor.preprocess("123456")
    assert res.normalized_text == "123456"
    assert res.is_empty is False


def test_emoji_preservation(preprocessor: TextPreprocessor):
    raw = "हा code 😭 slow आहे"
    res = preprocessor.preprocess(raw)
    assert "😭" in res.normalized_text
    assert "slow" in res.normalized_text
    assert "आहे" in res.normalized_text


def test_quotes_and_apostrophes(preprocessor: TextPreprocessor):
    raw = "Don't break 'single quotes' or \"double quotes\" in print(\"hello\")"
    res = preprocessor.preprocess(raw)
    assert "Don't" in res.normalized_text
    assert "'single quotes'" in res.normalized_text
    assert '"double quotes"' in res.normalized_text


def test_snake_and_kebab_case(preprocessor: TextPreprocessor):
    raw = "my_custom_var and kebab-case-name and camelCaseFunction"
    res = preprocessor.preprocess(raw)
    assert "my_custom_var" in res.normalized_text
    assert "kebab-case-name" in res.normalized_text
    assert "camelCaseFunction" in res.normalized_text


def test_idempotency(preprocessor: TextPreprocessor):
    inputs = [
        "hello world",
        "   Python   madhe   calculator   bana  ",
        "हा Python code explain कर",
        "हा code slow का आहे?\n\n```python\nfor i in range(10):\n    print(i)\n```",
        "def add(a, b):\n    return a + b",
        "हा code 😭 slow आहे",
    ]
    for inp in inputs:
        first = preprocessor.preprocess(inp)
        second = preprocessor.preprocess(first.normalized_text)
        assert first.normalized_text == second.normalized_text


def test_determinism(preprocessor: TextPreprocessor):
    raw = "Python मध्ये calculator तयार कर"
    res1 = preprocessor.preprocess(raw)
    res2 = preprocessor.preprocess(raw)
    assert res1.model_dump() == res2.model_dump()


def test_none_input_handled_safely(preprocessor: TextPreprocessor):
    res = preprocessor.preprocess(None)
    assert res.is_empty is True
    assert res.normalized_text == ""


def test_non_string_input_handled_safely(preprocessor: TextPreprocessor):
    res = preprocessor.preprocess(42)  # type: ignore
    assert res.normalized_text == "42"
    assert res.is_empty is False


def test_dict_access_and_serialization(preprocessor: TextPreprocessor):
    res = preprocessor.preprocess("python test")
    assert res["normalized_text"] == "python test"
    d = res.to_dict()
    assert isinstance(d, dict)
    assert d["normalized_text"] == "python test"
