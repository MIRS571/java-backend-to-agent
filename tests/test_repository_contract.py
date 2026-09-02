import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_env_example_contains_only_expected_blank_variables():
    assignments = [
        line.strip()
        for line in (ROOT / ".env.example").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]

    assert assignments == [
        "LLM_MODEL=",
        "LLM_API_KEY=",
        "LLM_BASE_URL=",
    ]


def test_roadmap_defines_exactly_twelve_numbered_chapters():
    roadmap = (ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\|\s*(\d+)\s*\|", roadmap, flags=re.MULTILINE)

    assert rows == [str(number) for number in range(1, 13)]
