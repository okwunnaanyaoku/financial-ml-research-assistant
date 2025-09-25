from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"


def load_prompt(name: str, **variables) -> str:
    template_path = PROMPTS_DIR / f"{name}.txt"
    if not template_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {template_path}")

    text = template_path.read_text(encoding="utf-8")
    return text.format(**variables) if variables else text

