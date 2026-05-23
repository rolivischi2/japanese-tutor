#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "markdown>=3.6",
#     "pyyaml>=6.0",
# ]
# ///
"""Build the deployed site under public/ from the curriculum sources.

Reads INDEX.md for module status, walks modules/, renders each .md file to
HTML using tools/templates/page.html, and writes the home page using
tools/templates/landing.html.

Run with --self-test to exercise the pure helper functions.
"""

from __future__ import annotations

import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml
import markdown as md_lib

ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = ROOT / "modules"
TEMPLATES_DIR = ROOT / "tools" / "templates"
OUT_DIR = ROOT / "public"
GITHUB_BLOB = "https://github.com/rolivischi2/japanese-tutor/blob/main"


@dataclass
class ModuleMeta:
    slug: str           # e.g. "01-copula-basics"
    number: str         # e.g. "01"
    title: str          # e.g. "Copula Basics"
    status: str         # "done" | "active" | "locked"
    key_grammar: str    # e.g. "です、じゃない、は、か、の"


_INDEX_ROW_RE = re.compile(
    r"^\|\s*M(?P<num>\d{2})\s*[—-]\s*(?P<title>[^|]+?)\s*\|"
    r"\s*(?P<status>[a-z]+)\s*\|"
    r"\s*[^|]*\|"           # est weeks (ignored)
    r"\s*(?P<key>[^|]+?)\s*\|"
)


def parse_index_md(path: Path, modules_dir: Path) -> dict[str, ModuleMeta]:
    """Parse INDEX.md's module status table.

    Returns dict keyed by module directory slug (e.g. "01-copula-basics").
    Modules present on disk but missing from INDEX.md default to "locked"
    with a warning. Unknown status strings default to "locked" with a
    warning.
    """
    text = path.read_text(encoding="utf-8")
    by_slug: dict[str, ModuleMeta] = {}
    for line in text.splitlines():
        m = _INDEX_ROW_RE.match(line)
        if not m:
            continue
        num = m.group("num")
        title = m.group("title").strip()
        status = m.group("status").strip().lower()
        key = m.group("key").strip()
        if status not in {"done", "active", "locked"}:
            print(f"WARN: unknown status {status!r} for module {num}, "
                  f"defaulting to locked", file=sys.stderr)
            status = "locked"
        dir_match = next(modules_dir.glob(f"{num}-*"), None)
        if dir_match is None:
            print(f"WARN: INDEX row 'M{num}' has no matching modules/ "
                  f"directory; skipping", file=sys.stderr)
            continue
        by_slug[dir_match.name] = ModuleMeta(
            slug=dir_match.name,
            number=num,
            title=title,
            status=status,
            key_grammar=key,
        )
    for d in sorted(modules_dir.iterdir()):
        if not d.is_dir():
            continue
        if d.name in by_slug:
            continue
        print(f"WARN: module {d.name} has no INDEX.md row; defaulting "
              f"to locked", file=sys.stderr)
        num = d.name.split("-", 1)[0]
        rest = d.name.split("-", 1)[1] if "-" in d.name else d.name
        title = rest.replace("-", " ").title()
        by_slug[d.name] = ModuleMeta(
            slug=d.name,
            number=num,
            title=title,
            status="locked",
            key_grammar="",
        )
    return by_slug


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_tests()
    # Full build implemented in later tasks.
    print("build_site.py: skeleton only — full build not yet implemented")
    return 0


def run_self_tests() -> int:
    failures: list[str] = []

    # parse_index_md against the real INDEX.md
    result = parse_index_md(ROOT / "INDEX.md", MODULES_DIR)
    if "01-copula-basics" not in result:
        failures.append("parse_index_md: '01-copula-basics' missing")
    if result.get("01-copula-basics") and result["01-copula-basics"].status != "active":
        failures.append(
            f"parse_index_md: M01 status expected 'active', got "
            f"{result['01-copula-basics'].status!r}"
        )
    if result.get("00-writing-systems") and result["00-writing-systems"].status != "done":
        failures.append(
            f"parse_index_md: M00 status expected 'done', got "
            f"{result['00-writing-systems'].status!r}"
        )
    if result.get("05-te-form") and result["05-te-form"].status != "locked":
        failures.append(
            f"parse_index_md: M05 status expected 'locked', got "
            f"{result['05-te-form'].status!r}"
        )

    n = 1
    if failures:
        print(f"build_site.py self-tests: FAIL ({len(failures)} failures, {n} cases)", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"build_site.py self-tests: PASS ({n}/{n})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
