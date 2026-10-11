import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


PROJECT_ROOT = Path(__file__).resolve().parents[3]

load_dotenv(PROJECT_ROOT / "backend" / ".env")


class GeminiClient:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    def generate_manim_code(self, prompt: str) -> str:
        system_prompt = """
You are an expert Manim Community Edition developer.

Your task is to generate Python code for a Manim animation
based on the user's request.

Rules:
1. Use Manim Community Edition.
2. Return ONLY Python code.
3. Do NOT use Markdown code fences.
4. Do NOT include explanations before or after the code.
5. The code must contain a Scene class.
6. The Scene class must implement construct().
7. Import Manim using:
   from manim import *
8. Keep the animation self-contained.
9. Do not use external files, network requests, subprocesses,
   operating-system commands, eval(), or exec().
10. Make the animation educational and visually clear.

User request:
"""

        full_prompt = system_prompt + "\n" + prompt

        return self.generate(full_prompt)