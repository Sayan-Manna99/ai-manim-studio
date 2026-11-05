import ast
import re


class CodeParserError(ValueError):
    """Raised when an LLM response cannot be parsed into usable Python."""


def extract_python(response: str) -> str:
    if not response or not response.strip():
        raise CodeParserError("LLM returned an empty response")

    text = response.strip()

    # Extract Python from a Markdown code fence, if present.
    fenced_blocks = re.findall(
        r"```(?:python|py)?\s*\n(.*?)```",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if fenced_blocks:
        text = max(fenced_blocks, key=len).strip()

    if not text:
        raise CodeParserError("No Python code found in the response")

    # Confirm that the extracted text is syntactically valid Python.
    try:
        ast.parse(text)
    except SyntaxError as exc:
        raise CodeParserError(
            f"Generated response is not valid Python: {exc}"
        ) from exc

    return text + "\n"