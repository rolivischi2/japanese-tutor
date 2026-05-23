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


_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def strip_frontmatter(text: str) -> tuple[dict, str]:
    """Strip a YAML frontmatter block from the start of a Markdown file.

    Returns (frontmatter_dict, body_text). If no frontmatter is present,
    returns ({}, text).
    """
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return ({}, text)
    data = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():]
    return (data, body)


_FURIGANA_RE = re.compile(r"\{([^{}|\s]+)\|([^{}|\s]+)\}")
_FENCED_CODE_RE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def preprocess_furigana(text: str) -> str:
    """Expand {kanji|kana} shorthand to <ruby>kanji<rt>kana</rt></ruby>.

    Skips content inside fenced code blocks (```...```) and inline code
    spans (`...`).
    """
    parts: list[tuple[str, str]] = []
    cursor = 0
    for m in _FENCED_CODE_RE.finditer(text):
        if m.start() > cursor:
            parts.append(("text", text[cursor:m.start()]))
        parts.append(("code", m.group(0)))
        cursor = m.end()
    if cursor < len(text):
        parts.append(("text", text[cursor:]))

    out: list[str] = []
    for kind, chunk in parts:
        if kind == "code":
            out.append(chunk)
            continue
        sub_cursor = 0
        for im in _INLINE_CODE_RE.finditer(chunk):
            if im.start() > sub_cursor:
                out.append(_FURIGANA_RE.sub(
                    r"<ruby>\1<rt>\2</rt></ruby>",
                    chunk[sub_cursor:im.start()],
                ))
            out.append(im.group(0))
            sub_cursor = im.end()
        if sub_cursor < len(chunk):
            out.append(_FURIGANA_RE.sub(
                r"<ruby>\1<rt>\2</rt></ruby>",
                chunk[sub_cursor:],
            ))
    return "".join(out)


_HREF_RE = re.compile(r'href="([^"#?]+)([?#][^"]*)?"')


def rewrite_links(html: str, current_md_path: Path) -> str:
    """Rewrite link `href` attributes in rendered HTML.

    Rules:
    - http(s)://, mailto:, anchors → unchanged
    - .md targets resolving under modules/ → .html (00-overview.md →
      index.html for clean URLs)
    - .md targets resolving outside modules/ → GitHub blob URL
    - other extensions or no extension → unchanged
    """

    def rewrite(match: re.Match[str]) -> str:
        target = match.group(1)
        suffix = match.group(2) or ""
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)
        if not target.endswith(".md"):
            return match.group(0)
        resolved = (current_md_path.parent / target).resolve()
        try:
            rel = resolved.relative_to(ROOT)
        except ValueError:
            return match.group(0)
        parts = rel.parts
        if parts and parts[0] == "modules":
            new_target = target[:-3] + ".html"
            if new_target.endswith("00-overview.html"):
                new_target = new_target[:-len("00-overview.html")] + "index.html"
            return f'href="{new_target}{suffix}"'
        return f'href="{GITHUB_BLOB}/{rel.as_posix()}{suffix}"'

    return _HREF_RE.sub(rewrite, html)


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

    # strip_frontmatter
    sample = "---\nmodule: 01\nfile: foo\n---\n# Hello\n\nbody"
    fm, body = strip_frontmatter(sample)
    if fm.get("module") != 1 or fm.get("file") != "foo":
        failures.append(f"strip_frontmatter: frontmatter dict wrong: {fm!r}")
    if not body.startswith("# Hello"):
        failures.append(f"strip_frontmatter: body wrong: {body!r}")

    no_fm = "# Plain\n"
    fm, body = strip_frontmatter(no_fm)
    if fm != {} or body != no_fm:
        failures.append(f"strip_frontmatter: no-fm case wrong: {fm!r}, {body!r}")

    # preprocess_furigana
    furi_cases = [
        ("{漢字|かんじ}", "<ruby>漢字<rt>かんじ</rt></ruby>"),
        ("plain text", "plain text"),
        ("`{漢字|かんじ}`", "`{漢字|かんじ}`"),
        ("```\n{漢字|かんじ}\n```", "```\n{漢字|かんじ}\n```"),
        ("see {猫|ねこ} and {犬|いぬ}",
         "see <ruby>猫<rt>ねこ</rt></ruby> and <ruby>犬<rt>いぬ</rt></ruby>"),
    ]
    for src, expected in furi_cases:
        got = preprocess_furigana(src)
        if got != expected:
            failures.append(
                f"preprocess_furigana({src!r}): expected {expected!r}, got {got!r}"
            )

    # rewrite_links
    current = MODULES_DIR / "01-copula-basics" / "01-desu-copula.md"

    link_cases = [
        ('<a href="./02-wa-topic-particle.md">X</a>',
         '<a href="./02-wa-topic-particle.html">X</a>',
         "sibling"),
        ('<a href="./00-overview.md">X</a>',
         '<a href="./index.html">X</a>',
         "overview"),
        ('<a href="../02-existence-and-location/00-overview.md">X</a>',
         '<a href="../02-existence-and-location/index.html">X</a>',
         "cross-module"),
        ('<a href="https://example.com">X</a>',
         '<a href="https://example.com">X</a>',
         "http"),
    ]
    for src, expected, label in link_cases:
        got = rewrite_links(src, current)
        if got != expected:
            failures.append(f"rewrite_links {label}: got {got!r}")

    # external md → GitHub blob
    src = '<a href="../../pronunciation/07-hungarian-transfer-notes.md">X</a>'
    got = rewrite_links(src, current)
    if "github.com/rolivischi2/japanese-tutor/blob/main/pronunciation/07-" not in got:
        failures.append(f"rewrite_links external-md: got {got!r}")

    n = 13
    if failures:
        print(f"build_site.py self-tests: FAIL ({len(failures)} failures, {n} cases)", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"build_site.py self-tests: PASS ({n}/{n})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
