import re
from pathlib import Path
from urllib.parse import unquote

from mkdocs.config import load_config

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


def test_every_document_has_exactly_one_h1():
    for path in sorted((ROOT / "docs").rglob("*.md")):
        content = path.read_text(encoding="utf-8")
        prose = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        headings = re.findall(r"^# .+$", prose, re.MULTILINE)
        assert len(headings) == 1, f"{path.relative_to(ROOT)} 应且仅应有一个 H1"


def test_all_chapters_keep_the_teaching_contract():
    required_sections = [f"## {number}." for number in range(1, 13)]
    chapter_paths = sorted((ROOT / "docs").glob("chapter*/*.md"))

    assert len(chapter_paths) == 12
    for path in chapter_paths:
        content = path.read_text(encoding="utf-8")
        for section in required_sections:
            assert section in content, f"{path.relative_to(ROOT)} 缺少 {section}"


def test_relative_markdown_links_resolve():
    markdown_paths = [ROOT / "README.md", ROOT / "ROADMAP.md"]
    markdown_paths.extend(sorted((ROOT / "docs").rglob("*.md")))
    markdown_paths.extend(sorted((ROOT / "examples").rglob("README.md")))
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

    for path in markdown_paths:
        content = path.read_text(encoding="utf-8")
        for raw_target in link_pattern.findall(content):
            target = raw_target.strip().strip("<>").split("#", maxsplit=1)[0]
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            resolved = (path.parent / unquote(target)).resolve()
            assert resolved.exists(), (
                f"{path.relative_to(ROOT)} 包含失效链接：{raw_target}"
            )


def test_mkdocs_navigation_targets_exist():
    config = load_config(config_file=str(ROOT / "mkdocs.yml"))

    def collect_targets(items: list[object]) -> list[str]:
        targets: list[str] = []
        for item in items:
            if isinstance(item, str):
                targets.append(item)
            elif isinstance(item, dict):
                value = next(iter(item.values()))
                if isinstance(value, str):
                    targets.append(value)
                elif isinstance(value, list):
                    targets.extend(collect_targets(value))
        return targets

    targets = collect_targets(config["nav"])
    for target in targets:
        assert (ROOT / "docs" / target).is_file(), f"MkDocs 导航失效：{target}"
