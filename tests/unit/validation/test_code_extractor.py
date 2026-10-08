"""Unit tests for CodeExtractor."""

from backend.app.validation.code_extractor import CodeExtractor


def test_extract_single_python_block():
    extractor = CodeExtractor()
    text = (
        "Here is the function:\n\n"
        "```python\n"
        "def add(a, b):\n"
        "    return a + b\n"
        "```\n\n"
        "Hope this helps!"
    )
    blocks = extractor.extract_blocks(text)
    assert len(blocks) == 1
    assert blocks[0].block_id == 1
    assert blocks[0].declared_language == "python"
    assert blocks[0].code == "def add(a, b):\n    return a + b"
    assert blocks[0].is_fenced is True


def test_extract_multiple_blocks_different_languages():
    extractor = CodeExtractor()
    text = (
        "Here is Python:\n"
        "```py\n"
        "x = 10\n"
        "```\n\n"
        "And here is C++:\n"
        "```cpp\n"
        "int x = 10;\n"
        "```\n"
    )
    blocks = extractor.extract_blocks(text)
    assert len(blocks) == 2
    assert blocks[0].block_id == 1
    assert blocks[0].declared_language == "py"
    assert blocks[0].code == "x = 10"

    assert blocks[1].block_id == 2
    assert blocks[1].declared_language == "cpp"
    assert blocks[1].code == "int x = 10;"


def test_extract_tilde_fences():
    extractor = CodeExtractor()
    text = (
        "~~~c\n"
        "int a = 5;\n"
        "~~~\n"
    )
    blocks = extractor.extract_blocks(text)
    assert len(blocks) == 1
    assert blocks[0].declared_language == "c"
    assert blocks[0].code == "int a = 5;"


def test_extract_unlabeled_fence():
    extractor = CodeExtractor()
    text = (
        "```\n"
        "SELECT * FROM users;\n"
        "```\n"
    )
    blocks = extractor.extract_blocks(text)
    assert len(blocks) == 1
    assert blocks[0].declared_language is None
    assert blocks[0].code == "SELECT * FROM users;"


def test_extract_empty_and_whitespace_block():
    extractor = CodeExtractor()
    text = (
        "```python\n"
        "\n"
        "```\n"
    )
    blocks = extractor.extract_blocks(text)
    assert len(blocks) == 1
    assert blocks[0].code == ""


def test_extract_no_code_text():
    extractor = CodeExtractor()
    text = "Just a friendly explanation without any code block."
    blocks = extractor.extract_blocks(text)
    assert len(blocks) == 0


def test_extract_unclosed_fence_at_end():
    extractor = CodeExtractor()
    text = (
        "Here is the incomplete code:\n"
        "```javascript\n"
        "const msg = 'hello';"
    )
    blocks = extractor.extract_blocks(text)
    assert len(blocks) == 1
    assert blocks[0].declared_language == "javascript"
    assert blocks[0].code == "const msg = 'hello';"
    assert blocks[0].is_fenced is False


def test_extract_empty_input():
    extractor = CodeExtractor()
    assert extractor.extract_blocks("") == []
    assert extractor.extract_blocks("   ") == []
