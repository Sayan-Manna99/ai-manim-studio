import pytest

from backend.app.ai.parser import CodeParserError, extract_python


def test_extracts_raw_python():
    code = "from manim import *\nclass Demo(Scene):\n    pass"

    assert "class Demo(Scene)" in extract_python(code)


def test_extracts_fenced_python():
    response = (
        "Here is the code:\n"
        "```python\n"
        "from manim import *\n"
        "class Demo(Scene):\n"
        "    pass\n"
        "```\n"
    )

    result = extract_python(response)

    assert result.startswith("from manim import *")
    assert "```" not in result


def test_rejects_empty_response():
    with pytest.raises(CodeParserError):
        extract_python("   ")


def test_rejects_invalid_python():
    with pytest.raises(CodeParserError):
        extract_python("def broken(:")