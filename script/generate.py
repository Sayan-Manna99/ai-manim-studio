import argparse


def main():
    parser = argparse.ArgumentParser(
        description="AI Manim Studio - Generate educational animations"
    )

    parser.add_argument(
        "prompt",
        help="Description of the animation to generate"
    )

    args = parser.parse_args()

    print("AI Manim Studio")
    print("=" * 40)
    print(f"Prompt received: {args.prompt}")


if __name__ == "__main__":
    main()