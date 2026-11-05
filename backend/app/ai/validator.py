
import ast
from platform import node


class CodeValidationError(ValueError):
    """Raised when generated Manim code violates safety rules."""


ALLOWED_IMPORTS = {
    "manim",
    "math",
    "random",
    "numpy",
    "scipy",
    "itertools",
    "functools",
    "collections",
}

BLOCKED_CALLS = {
    "eval",
    "exec",
    "compile",
    "open",
    "__import__",
    "input",
    "breakpoint",
    "getattr",
    "setattr",
    "delattr",
    "vars",
    "globals",
    "locals",
}

BLOCKED_ATTRIBUTES = {
    "__class__",
    "__bases__",
    "__subclasses__",
    "__globals__",
    "__code__",
    "__builtins__",
    "__mro__",
    "__dict__",
    "__getattribute__",
    "__reduce__",
    "__reduce_ex__",
}


class ImportValidator(ast.NodeVisitor):

   
    def visit_Import(self, node):
        """Validate direct import statements."""

        for alias in node.names:
            module = alias.name

            if module not in ALLOWED_IMPORTS:
                raise CodeValidationError(
                    f"Import of '{module}' is not allowed"
             )

        self.generic_visit(node)


    def visit_ImportFrom(self, node):
        """Validate from-import statements."""
        if node.level != 0 or node.module is None:
            raise CodeValidationError(
                "Relative imports are not allowed"
            )

        module = node.module.split(".")[0]

        if module not in ALLOWED_IMPORTS:
            raise CodeValidationError(
                f"Import from '{node.module}' is not allowed"
            )

        self.generic_visit(node)

    def visit_Call(self, node):
        """Block dangerous function calls."""

        if isinstance(node.func, ast.Name):
            if node.func.id in BLOCKED_CALLS:
                raise CodeValidationError(
                    f"Call to '{node.func.id}()' is not allowed"
                )

        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Block access to sensitive attributes."""

        if node.attr in BLOCKED_ATTRIBUTES:
            raise CodeValidationError(
                f"Access to attribute '{node.attr}' is not allowed"
            )

        self.generic_visit(node)


def validate_code(code: str) -> None:
    """Parse and validate generated Python code."""

    if not code or not code.strip():
        raise CodeValidationError("Generated code is empty")

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        raise CodeValidationError(
            f"Invalid Python syntax: {exc}"
        ) from exc

    validator = ImportValidator()
    validator.visit(tree)


    
