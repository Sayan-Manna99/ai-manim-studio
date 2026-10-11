from pathlib import Path

from app.ai.client import GeminiClient


def main():
    client = GeminiClient()

    code = client.generate_manim_code(
        "Create a simple animation explaining binary search."
    )

    output_dir = Path("backend/generated")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "scene.py"
    output_file.write_text(code, encoding="utf-8")

    print("\n✓ Manim code generated")
    print(f"✓ Code saved to: {output_file}")


if __name__ == "__main__":
    main()