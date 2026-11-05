
import pytest

from backend.app.ai.validator import (
    validate_code,
    CodeValidationError,
)


def test_accepts_valid_manim_code():
    code = """
from manim import *

class Demo(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
"""
    validate_code(code)


@pytest.mark.parametrize(
    "code",
    [
        "import os",
        "import subprocess",
        "from socket import socket",
    ],
)
def test_rejects_dangerous_imports(code):
    with pytest.raises(CodeValidationError):
        validate_code(code)


@pytest.mark.parametrize(
    "code",
    [
        'eval("2 + 2")',
        'exec("print(1)")',
        'open("secret.txt")',
        'compile("1 + 1", "<string>", "eval")',
        'input("Enter value")',
        'breakpoint()',
    ],
)
def test_rejects_dangerous_calls(code):
    with pytest.raises(CodeValidationError):
        validate_code(code)


@pytest.mark.parametrize(
    "code",
    [
        "x.__class__",
        "x.__subclasses__()",
        "func.__globals__",
        "x.__builtins__",
    ],
)
def test_rejects_sensitive_attributes(code):
    with pytest.raises(CodeValidationError):
        validate_code(code)


def test_rejects_invalid_python():
    with pytest.raises(CodeValidationError):
        validate_code("def broken(:")


def test_rejects_empty_code():
    with pytest.raises(CodeValidationError):
        validate_code("   ")


def test_accepts_normal_manim_attributes():
    code = """
from manim import *

class Demo(Scene):
    def construct(self):
        circle = Circle()
        circle.set_color(BLUE)
        self.play(Create(circle))
"""
    validate_code(code)


@pytest.mark.parametrize(
    "code",
    [
        "import manim.scene",
        "x.__dict__",
        "x.__getattribute__('name')",
        "getattr(x, 'name')",
        "globals()",
        "locals()",
    ],
)
def test_rejects_additional_unsafe_patterns(code):
    with pytest.raises(CodeValidationError):
        validate_code(code)


def test_allows_nested_import_from_manim():
    validate_code("from manim.scene import Scene")


def test_rejects_relative_import():
    with pytest.raises(CodeValidationError):
        validate_code("from . import something")
