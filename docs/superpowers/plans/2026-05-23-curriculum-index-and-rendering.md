# Curriculum Index + On-site Rendering Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy a "Curriculum" section on the landing page listing M00–M12 with status badges. Render every module `.md` file as a styled on-site HTML page. Replace the landing's radial-gradient/noise background with a solid paper color across the whole site.

**Architecture:** A single Python build script (`tools/build_site.py`) is invoked by `scripts/build-vercel.sh`. It parses `INDEX.md` for module status, walks `modules/`, renders each `.md` through a template, and writes the output to `public/`. Pure functions (frontmatter strip, furigana preprocess, link rewrite, markdown render) are small and verifiable via a `--self-test` mode in the script. No external test framework added.

**Tech Stack:** Python 3.13 via uv, Python `markdown` package + `PyYAML` declared in a PEP 723 inline metadata header (matches existing `tools/export_to_anki.py` pattern). HTML5 + CSS3. No JS in the rendered pages.

---

## File map

**Created:**
- `tools/build_site.py` — orchestrator + pure helper functions, ~300 LOC.
- `tools/templates/page.html` — single template for rendered module pages.
- `tools/templates/landing.html` — replaces `scripts/landing.html`; source of truth for the home page.

**Modified:**
- `scripts/build-vercel.sh` — calls `uv run tools/build_site.py` instead of `cp scripts/landing.html`.

**Deleted:**
- `scripts/landing.html` — replaced by `tools/templates/landing.html`.

---

## Task 1: Scaffold `tools/build_site.py` with PEP 723 header and `--self-test` skeleton

**Files:**
- Create: `tools/build_site.py`
- Create: `tools/templates/.gitkeep` (so the empty directory exists before subsequent tasks add templates)

- [ ] **Step 1: Create the templates directory**

```bash
mkdir -p /Users/rvischi/Documents/repositories/japan-learning/tools/templates
touch /Users/rvischi/Documents/repositories/japan-learning/tools/templates/.gitkeep
```

- [ ] **Step 2: Write the script skeleton with PEP 723 header**

Create `tools/build_site.py` with this content:

```python
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


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_tests()
    # Full build implemented in later tasks.
    print("build_site.py: skeleton only — full build not yet implemented")
    return 0


def run_self_tests() -> int:
    print("build_site.py self-tests: 0 cases (skeleton)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

- [ ] **Step 3: Run the skeleton to verify uv + PEP 723 work**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
uv run tools/build_site.py --self-test
```

Expected output:
```
build_site.py self-tests: 0 cases (skeleton)
```

If `uv run` fails to resolve `markdown` or `pyyaml`, the PEP 723 header is wrong — fix and re-run.

- [ ] **Step 4: Commit**

```bash
git add tools/build_site.py tools/templates/.gitkeep
git commit -m "$(cat <<'EOF'
Scaffold tools/build_site.py with PEP 723 header

Empty entry point + --self-test flag. Resolves markdown + pyyaml
ephemerally via uv. Full build logic in subsequent commits.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: `parse_index_md(path) -> dict[str, ModuleMeta]`

Reads `INDEX.md`'s module status table and returns a dict keyed by directory slug. Emits warnings for malformed rows.

**Files:**
- Modify: `tools/build_site.py`

- [ ] **Step 1: Add the function**

Insert after the `ModuleMeta` dataclass:

```python
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
    by_num: dict[str, ModuleMeta] = {}
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
        # Find matching directory on disk.
        dir_match = next(modules_dir.glob(f"{num}-*"), None)
        if dir_match is None:
            print(f"WARN: INDEX row 'M{num}' has no matching modules/ "
                  f"directory; skipping", file=sys.stderr)
            continue
        by_num[dir_match.name] = ModuleMeta(
            slug=dir_match.name,
            number=num,
            title=title,
            status=status,
            key_grammar=key,
        )
    # Add any on-disk modules missing from INDEX.md, default locked.
    for d in sorted(modules_dir.iterdir()):
        if not d.is_dir():
            continue
        if d.name in by_num:
            continue
        print(f"WARN: module {d.name} has no INDEX.md row; defaulting "
              f"to locked", file=sys.stderr)
        num = d.name.split("-", 1)[0]
        title = d.name.split("-", 1)[1].replace("-", " ").title()
        by_num[d.name] = ModuleMeta(
            slug=d.name,
            number=num,
            title=title,
            status="locked",
            key_grammar="",
        )
    return by_num
```

- [ ] **Step 2: Add a self-test case**

Replace `run_self_tests()` body with:

```python
def run_self_tests() -> int:
    failures: list[str] = []

    # Test parse_index_md against the real INDEX.md
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
        print(f"build_site.py self-tests: FAIL ({len(failures)}/{n})", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"build_site.py self-tests: PASS ({n}/{n})")
    return 0
```

- [ ] **Step 3: Run the self-tests**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
uv run tools/build_site.py --self-test
```

Expected: `build_site.py self-tests: PASS (1/1)`.

If a row regex misses, inspect `INDEX.md` line format and adjust `_INDEX_ROW_RE` until all rows parse.

- [ ] **Step 4: Commit**

```bash
git add tools/build_site.py
git commit -m "$(cat <<'EOF'
Add parse_index_md: extract module status table from INDEX.md

Returns a dict keyed by directory slug. Warns and defaults to "locked"
for unknown statuses, INDEX rows without matching directories, and
on-disk modules missing from the table.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: `strip_frontmatter(text) -> (dict, str)`

**Files:**
- Modify: `tools/build_site.py`

- [ ] **Step 1: Add the function**

Insert after `parse_index_md`:

```python
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
```

- [ ] **Step 2: Extend the self-test**

Add inside `run_self_tests()` before the count line:

```python
    # Test strip_frontmatter
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
```

Update the count: change `n = 1` to `n = 3` (one parse_index test + two strip_frontmatter cases).

- [ ] **Step 3: Run the self-tests**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
uv run tools/build_site.py --self-test
```

Expected: `build_site.py self-tests: PASS (3/3)`.

- [ ] **Step 4: Commit**

```bash
git add tools/build_site.py
git commit -m "$(cat <<'EOF'
Add strip_frontmatter: pull YAML header off Markdown files

Returns (dict, body). Empty dict + unchanged body if no frontmatter.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: `preprocess_furigana(text) -> str`

Replace `{漢字|かんじ}` shorthand with `<ruby>漢字<rt>かんじ</rt></ruby>`, but only outside backtick code spans and fenced code blocks.

**Files:**
- Modify: `tools/build_site.py`

- [ ] **Step 1: Add the function**

Insert after `strip_frontmatter`:

```python
_FURIGANA_RE = re.compile(r"\{([^{}|\s]+)\|([^{}|\s]+)\}")
_FENCED_CODE_RE = re.compile(r"^```.*?^```", re.DOTALL | re.MULTILINE)
_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def preprocess_furigana(text: str) -> str:
    """Expand {kanji|kana} shorthand to <ruby>kanji<rt>kana</rt></ruby>.

    Skips content inside fenced code blocks (```...```) and inline code
    spans (`...`).
    """
    # Walk fenced blocks first, preserving them as opaque chunks.
    parts: list[tuple[str, str]] = []  # ("code"|"text", chunk)
    cursor = 0
    for m in _FENCED_CODE_RE.finditer(text):
        if m.start() > cursor:
            parts.append(("text", text[cursor:m.start()]))
        parts.append(("code", m.group(0)))
        cursor = m.end()
    if cursor < len(text):
        parts.append(("text", text[cursor:]))

    # Within text chunks, split out inline code spans before applying the regex.
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
```

- [ ] **Step 2: Extend the self-test**

Add inside `run_self_tests()`:

```python
    # Test preprocess_furigana
    cases = [
        ("{漢字|かんじ}", "<ruby>漢字<rt>かんじ</rt></ruby>"),
        ("plain text", "plain text"),
        ("`{漢字|かんじ}`", "`{漢字|かんじ}`"),  # inline code skipped
        ("```\n{漢字|かんじ}\n```", "```\n{漢字|かんじ}\n```"),  # fenced skipped
        ("see {猫|ねこ} and {犬|いぬ}",
         "see <ruby>猫<rt>ねこ</rt></ruby> and <ruby>犬<rt>いぬ</rt></ruby>"),
    ]
    for src, expected in cases:
        got = preprocess_furigana(src)
        if got != expected:
            failures.append(
                f"preprocess_furigana({src!r}): expected {expected!r}, got {got!r}"
            )
```

Update count: `n = 8` (3 prior + 5 furigana cases).

- [ ] **Step 3: Run the self-tests**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
uv run tools/build_site.py --self-test
```

Expected: `build_site.py self-tests: PASS (8/8)`.

- [ ] **Step 4: Commit**

```bash
git add tools/build_site.py
git commit -m "$(cat <<'EOF'
Add preprocess_furigana: expand {kanji|kana} shorthand to <ruby>

Skips content inside fenced code blocks and inline code spans so the
shorthand renders literally in code samples.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: `rewrite_links(html, current_md_path) -> str`

Rewrite Markdown link targets in already-rendered HTML so internal `.md` links become `.html` and out-of-modules links become GitHub blob URLs.

**Files:**
- Modify: `tools/build_site.py`

- [ ] **Step 1: Add the function**

Insert after `preprocess_furigana`:

```python
_HREF_RE = re.compile(r'href="([^"#?]+)([?#][^"]*)?"')


def rewrite_links(html: str, current_md_path: Path) -> str:
    """Rewrite link `href` attributes in rendered HTML.

    current_md_path is the absolute path of the source .md file. Used to
    resolve relative link targets.

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
        # Resolve relative to the source file's directory.
        resolved = (current_md_path.parent / target).resolve()
        try:
            rel = resolved.relative_to(ROOT)
        except ValueError:
            # Outside the repo — leave as-is.
            return match.group(0)
        parts = rel.parts
        if parts and parts[0] == "modules":
            # Inside modules/ — rewrite to local .html
            new_target = target[:-3] + ".html"
            # Special-case 00-overview.md → index.html (clean URL)
            if new_target.endswith("00-overview.html"):
                new_target = new_target[:-len("00-overview.html")] + "index.html"
            return f'href="{new_target}{suffix}"'
        # Outside modules/ — point to GitHub source.
        return f'href="{GITHUB_BLOB}/{rel.as_posix()}{suffix}"'

    return _HREF_RE.sub(rewrite, html)
```

- [ ] **Step 2: Extend the self-test**

Add inside `run_self_tests()`:

```python
    # Test rewrite_links
    current = MODULES_DIR / "01-copula-basics" / "01-desu-copula.md"

    # local sibling .md → .html
    src = '<a href="./02-wa-topic-particle.md">X</a>'
    got = rewrite_links(src, current)
    expected = '<a href="./02-wa-topic-particle.html">X</a>'
    if got != expected:
        failures.append(f"rewrite_links sibling: {got!r}")

    # 00-overview.md → index.html
    src = '<a href="./00-overview.md">X</a>'
    got = rewrite_links(src, current)
    expected = '<a href="./index.html">X</a>'
    if got != expected:
        failures.append(f"rewrite_links overview: {got!r}")

    # other-module overview
    src = '<a href="../02-existence-and-location/00-overview.md">X</a>'
    got = rewrite_links(src, current)
    expected = '<a href="../02-existence-and-location/index.html">X</a>'
    if got != expected:
        failures.append(f"rewrite_links cross-module: {got!r}")

    # outside-modules .md → GitHub blob
    src = '<a href="../../pronunciation/07-hungarian-transfer-notes.md">X</a>'
    got = rewrite_links(src, current)
    if "github.com/rolivischi2/japanese-tutor/blob/main/pronunciation/07-" not in got:
        failures.append(f"rewrite_links external md: {got!r}")

    # http link untouched
    src = '<a href="https://example.com">X</a>'
    got = rewrite_links(src, current)
    if got != src:
        failures.append(f"rewrite_links http: {got!r}")
```

Update count: `n = 13` (8 prior + 5 link cases).

- [ ] **Step 3: Run the self-tests**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
uv run tools/build_site.py --self-test
```

Expected: `build_site.py self-tests: PASS (13/13)`. Inspect any failure and fix the rewrite logic.

- [ ] **Step 4: Commit**

```bash
git add tools/build_site.py
git commit -m "$(cat <<'EOF'
Add rewrite_links: relative .md → .html or GitHub blob URL

Rewrites href attributes in rendered HTML so cross-links between
modules resolve to local pages; links outside modules/ go to GitHub.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Create `tools/templates/page.html`

The single template for rendered module pages.

**Files:**
- Create: `tools/templates/page.html`

- [ ] **Step 1: Write the template**

Create `tools/templates/page.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}} — japan-learning</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Noto+Sans+JP:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#f1e8d6; --paper-2:#e9dcc2; --ink:#2b2620; --ink-soft:#6f6557;
    --vermilion:#bd3b2c; --vermilion-deep:#9c2f23; --gold:#b08a4a;
    --cell:#f7f0e0; --cell-line:#d8c8a6;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{min-height:100%}
  body{
    background:var(--paper); color:var(--ink);
    font-family:"Fraunces",Georgia,serif;
    -webkit-font-smoothing:antialiased;
    display:flex;flex-direction:column;
  }
  .jp,article :lang(ja){font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic","Meiryo",sans-serif}

  main{flex:1;max-width:1100px;width:100%;margin:0 auto;padding:36px 28px 28px}

  nav.breadcrumb{font-size:13px;color:var(--ink-soft);letter-spacing:.04em;margin-bottom:24px}
  nav.breadcrumb a{color:var(--ink-soft);text-decoration:none;border-bottom:1px solid transparent;transition:border-color .15s}
  nav.breadcrumb a:hover{border-bottom-color:var(--vermilion)}

  .layout{display:grid;grid-template-columns:240px 1fr;gap:48px}
  @media (max-width:760px){
    .layout{grid-template-columns:1fr;gap:24px}
    .sidebar{order:2;border-top:1px solid var(--cell-line);padding-top:16px}
  }

  aside.sidebar h4{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-soft);font-weight:600;margin-bottom:10px}
  aside.sidebar ul{list-style:none}
  aside.sidebar li{margin-bottom:6px}
  aside.sidebar a{color:var(--ink);text-decoration:none;font-size:14px;line-height:1.45;display:block;padding:3px 0;border-left:2px solid transparent;padding-left:10px;margin-left:-12px}
  aside.sidebar a:hover{color:var(--vermilion-deep)}
  aside.sidebar a.current{color:var(--vermilion);font-weight:600;border-left-color:var(--vermilion)}

  article.content{font-size:16.5px;line-height:1.68;max-width:760px}
  article.content h1{font-size:34px;font-weight:700;letter-spacing:.01em;margin-bottom:18px;line-height:1.18}
  article.content h2{font-size:22px;font-weight:600;margin:34px 0 12px}
  article.content h3{font-size:18px;font-weight:600;margin:24px 0 10px;color:var(--vermilion-deep)}
  article.content p{margin-bottom:14px}
  article.content ul,article.content ol{margin:0 0 16px 22px}
  article.content li{margin-bottom:6px}
  article.content blockquote{border-left:3px solid var(--gold);padding:6px 16px;margin:14px 0;background:rgba(255,255,255,.4);font-style:italic;color:var(--ink-soft)}
  article.content blockquote p{margin:0 0 6px}
  article.content blockquote p:last-child{margin:0}
  article.content code{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:.92em;background:var(--cell);padding:1px 5px;border-radius:3px}
  article.content pre{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:13px;background:var(--cell);border:1px solid var(--cell-line);padding:12px 14px;border-radius:5px;overflow-x:auto;margin:14px 0;line-height:1.55}
  article.content pre code{background:none;padding:0}
  article.content a{color:var(--vermilion);text-decoration:none;border-bottom:1px solid rgba(189,59,44,.25);transition:border-color .15s}
  article.content a:hover{border-bottom-color:var(--vermilion)}
  article.content table{border-collapse:collapse;margin:14px 0;font-size:.95em}
  article.content th,article.content td{border:1px solid var(--cell-line);padding:6px 10px;text-align:left}
  article.content th{background:var(--cell);font-weight:600}
  article.content ruby rt{font-size:.55em;color:var(--ink-soft);font-weight:400}
  article.content hr{border:none;border-top:1px solid var(--cell-line);margin:24px 0}

  footer{margin-top:48px;padding:24px 28px 22px;text-align:center;font-size:11.5px;color:var(--ink-soft);line-height:1.7;border-top:1px solid var(--cell-line)}
  footer a{color:var(--ink-soft);text-decoration:underline;text-underline-offset:2px}
  footer a:hover{color:var(--vermilion-deep)}
</style>
</head>
<body>
<main>
  <nav class="breadcrumb"><a href="/">Home</a> &rsaquo; <a href="/#curriculum">Module {{MODULE_NUM}}</a></nav>
  <div class="layout">
    <aside class="sidebar">
      <h4>{{MODULE_TITLE}}</h4>
      <ul>{{SIDEBAR_LIST}}</ul>
    </aside>
    <article class="content">
      {{RENDERED_HTML}}
    </article>
  </div>
</main>
<footer>
  Last updated: {{LAST_UPDATED}} &middot;
  <a href="{{SOURCE_URL}}" target="_blank" rel="noopener">View source on GitHub</a>
</footer>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add tools/templates/page.html
git commit -m "$(cat <<'EOF'
Add tools/templates/page.html for rendered module pages

Single template with breadcrumb, sidebar, content column, footer.
Solid paper background. Furigana ruby styled. Mobile-collapsing layout.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Per-file rendering: `render_md_file()` + `render_module()` + template fill

**Files:**
- Modify: `tools/build_site.py`

- [ ] **Step 1: Add the rendering functions**

Insert after `rewrite_links`:

```python
# File order within a module's sidebar.
def _sidebar_sort_key(name: str) -> tuple:
    """Order: 00-overview first, then numbered grammar files, then
    dialogues, exercises, self-talk, kanji-introduced, then everything
    else alphabetically."""
    base = name.removesuffix(".md")
    fixed_order = {
        "00-overview": 0,
        "dialogues": 100,
        "exercises": 101,
        "self-talk": 102,
        "kanji-introduced": 103,
    }
    if base in fixed_order:
        return (fixed_order[base], base)
    # Numbered grammar files (e.g. 01-desu-copula): rank 10-99 by number.
    m = re.match(r"^(\d{2})-", base)
    if m:
        return (10 + int(m.group(1)), base)
    return (200, base)  # other files at the end


def _human_title(slug: str) -> str:
    """Turn '01-desu-copula' → 'Desu copula'. Pure formatting helper."""
    base = slug.removesuffix(".md")
    m = re.match(r"^\d{2}-(.*)$", base)
    core = m.group(1) if m else base
    return core.replace("-", " ").capitalize()


def _render_sidebar(module: ModuleMeta, files: list[Path], current: Path) -> str:
    """Build the <li><a> list for the sidebar."""
    items: list[str] = []
    for f in sorted(files, key=lambda p: _sidebar_sort_key(p.name)):
        is_current = f.resolve() == current.resolve()
        href = "index.html" if f.name == "00-overview.md" else f.name.replace(".md", ".html")
        label = "Overview" if f.name == "00-overview.md" else _human_title(f.name)
        cls = ' class="current"' if is_current else ""
        items.append(f'<li><a href="{href}"{cls}>{label}</a></li>')
    return "\n        ".join(items)


def render_md_file(
    md_path: Path,
    module: ModuleMeta,
    sibling_md_files: list[Path],
    template: str,
) -> str:
    """Render one .md file to a full HTML page string."""
    raw = md_path.read_text(encoding="utf-8")
    frontmatter, body = strip_frontmatter(raw)
    body = preprocess_furigana(body)

    md = md_lib.Markdown(extensions=["fenced_code", "tables", "attr_list"])
    rendered = md.convert(body)
    rendered = rewrite_links(rendered, md_path)

    page_title = _human_title(md_path.name) if md_path.name != "00-overview.md" else module.title
    sidebar = _render_sidebar(module, sibling_md_files, md_path)
    rel_source = md_path.relative_to(ROOT).as_posix()

    return (template
        .replace("{{TITLE}}", page_title)
        .replace("{{MODULE_NUM}}", module.number)
        .replace("{{MODULE_TITLE}}", f"M{module.number} — {module.title}")
        .replace("{{SIDEBAR_LIST}}", sidebar)
        .replace("{{RENDERED_HTML}}", rendered)
        .replace("{{LAST_UPDATED}}", str(frontmatter.get("last_updated", "—")))
        .replace("{{SOURCE_URL}}", f"{GITHUB_BLOB}/{rel_source}")
    )


def render_module(module: ModuleMeta, out_dir: Path, template: str) -> int:
    """Render all .md files in a module to out_dir/<slug>/. Returns file count."""
    src_dir = MODULES_DIR / module.slug
    md_files = sorted(src_dir.glob("*.md"))
    if not md_files:
        return 0
    target = out_dir / "modules" / module.slug
    target.mkdir(parents=True, exist_ok=True)
    written = 0
    for f in md_files:
        html = render_md_file(f, module, md_files, template)
        out_name = "index.html" if f.name == "00-overview.md" else f.name.replace(".md", ".html")
        (target / out_name).write_text(html, encoding="utf-8")
        written += 1
    return written
```

- [ ] **Step 2: Wire into `main()` (still no landing yet, but rendering should work)**

Replace the body of `main()`:

```python
def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_tests()

    page_template = (TEMPLATES_DIR / "page.html").read_text(encoding="utf-8")
    modules = parse_index_md(ROOT / "INDEX.md", MODULES_DIR)

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    total = 0
    for slug in sorted(modules):
        total += render_module(modules[slug], OUT_DIR, page_template)
    print(f"Rendered {total} module page(s) into {OUT_DIR}/modules/")
    return 0
```

- [ ] **Step 3: Run build_site.py end-to-end and inspect M01**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
uv run tools/build_site.py
ls public/modules/01-copula-basics/
```

Expected: directory contains `index.html`, `01-desu-copula.html`, `02-wa-topic-particle.html`, `03-negative-dewa-arimasen.html`, `04-questions-ka.html`, `05-no-possession.html`, `06-kosoado-preview.html`, `dialogues.html`, `exercises.html`, `self-talk.html`.

Spot-check one rendered file:
```bash
head -50 public/modules/01-copula-basics/index.html
```
Expected: HTML5 boilerplate, sidebar with all M01 files, breadcrumb to Home, rendered content begins with the M01 overview heading.

- [ ] **Step 4: Self-tests still pass**

```bash
uv run tools/build_site.py --self-test
```
Expected: `PASS (13/13)`.

- [ ] **Step 5: Commit**

```bash
git add tools/build_site.py
git commit -m "$(cat <<'EOF'
Render each module .md to a styled HTML page

Adds render_md_file and render_module. Wires main() to walk all modules
and write public/modules/<slug>/<file>.html. 00-overview.md becomes
index.html so module URLs are clean. Sidebar listing per page.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 8: Create `tools/templates/landing.html` and `build_landing()`

**Files:**
- Create: `tools/templates/landing.html`
- Modify: `tools/build_site.py`

- [ ] **Step 1: Write the landing template**

Create `tools/templates/landing.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>japan-learning — curriculum + kana tools</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Noto+Sans+JP:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#f1e8d6; --paper-2:#e9dcc2; --ink:#2b2620; --ink-soft:#6f6557;
    --vermilion:#bd3b2c; --vermilion-deep:#9c2f23; --gold:#b08a4a;
    --cell:#f7f0e0; --cell-line:#d8c8a6;
    --muted-cell:#ece1cb; --muted-text:#a39a8a;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{min-height:100%}
  body{
    background:var(--paper); color:var(--ink);
    font-family:"Fraunces",Georgia,serif;
    -webkit-font-smoothing:antialiased;
    display:flex;flex-direction:column;
  }
  .jp{font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic","Meiryo",sans-serif}

  main{flex:1;max-width:980px;width:100%;margin:0 auto;padding:60px 28px 40px}
  header{text-align:center;margin-bottom:50px;position:relative;padding-bottom:24px}
  header::after{content:"";position:absolute;left:50%;bottom:0;transform:translateX(-50%);
    width:64px;height:2px;background:var(--vermilion)}
  .kicker{font-size:12px;letter-spacing:.42em;text-transform:uppercase;color:var(--ink-soft);font-weight:600}
  h1{font-size:74px;line-height:.96;font-weight:800;letter-spacing:.05em;margin:10px 0 6px;color:var(--ink)}
  h1 .jp{color:var(--vermilion);margin-right:6px;font-weight:700}
  .lede{font-style:italic;font-size:16px;color:var(--ink-soft);max-width:560px;margin:0 auto}

  section.cards{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:6px}
  @media (max-width:680px){
    section.cards{grid-template-columns:1fr}
    h1{font-size:52px}
    main{padding:42px 18px 32px}
    header{margin-bottom:36px}
  }
  .card{
    background:var(--cell);border:1px solid var(--cell-line);border-radius:9px;
    padding:28px 26px 24px;text-decoration:none;color:inherit;
    display:flex;flex-direction:column;gap:12px;
    transition:transform .18s ease, border-color .18s ease, box-shadow .18s ease, background .18s ease;
    position:relative;overflow:hidden;
  }
  .card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;
    background:var(--vermilion);transform:scaleX(0);transform-origin:left;
    transition:transform .25s ease}
  .card:hover:not(.locked){background:#fff;border-color:var(--vermilion);
    transform:translateY(-3px);box-shadow:0 14px 30px -18px rgba(43,38,32,.5)}
  .card:hover:not(.locked)::before{transform:scaleX(1)}

  .card .ch{font-size:50px;line-height:1;font-weight:500;color:var(--ink);display:flex;gap:6px;align-items:flex-end}
  .card .ch .small{font-size:30px;color:var(--ink-soft)}
  .card h2{font-size:21px;font-weight:600;letter-spacing:.01em;line-height:1.2}
  .card p{font-size:14px;color:var(--ink-soft);line-height:1.55}
  .card .arrow{margin-top:auto;font-size:12.5px;font-weight:600;color:var(--vermilion);letter-spacing:.06em;text-transform:uppercase;display:flex;align-items:center;gap:8px}
  .card .arrow::after{content:"→";transition:transform .18s ease}
  .card:hover:not(.locked) .arrow{color:var(--vermilion-deep)}
  .card:hover:not(.locked) .arrow::after{transform:translateX(4px)}

  /* Curriculum section */
  section.curriculum{margin-top:60px}
  section.curriculum h2.section-title{font-size:13px;letter-spacing:.42em;text-transform:uppercase;color:var(--ink-soft);font-weight:600;margin-bottom:8px}
  section.curriculum .lede{margin:0 0 24px;text-align:left;font-style:italic;color:var(--ink-soft);font-size:14.5px}
  .module-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
  .module-card{padding:18px 18px 16px;gap:8px}
  .module-card .module-num{font-size:11px;font-weight:700;letter-spacing:.18em;color:var(--ink-soft);text-transform:uppercase}
  .module-card h3{font-size:17px;font-weight:600;line-height:1.25;letter-spacing:.005em;color:var(--ink)}
  .module-card .key-grammar{font-size:13px;color:var(--ink-soft);line-height:1.5}
  .module-card .status-pill{font-size:10px;letter-spacing:.12em;text-transform:uppercase;padding:2px 9px;border-radius:99px;font-weight:600;align-self:flex-start;margin-top:auto}
  .status-pill.done{background:var(--gold);color:#fff}
  .status-pill.active{background:var(--vermilion);color:#fff}
  .status-pill.locked{background:transparent;color:var(--muted-text);border:1px solid var(--cell-line)}
  .module-card.locked{background:var(--muted-cell);color:var(--muted-text);cursor:not-allowed;pointer-events:none}
  .module-card.locked h3{color:var(--muted-text)}
  .module-card.locked .key-grammar{color:var(--muted-text);opacity:.85}

  .meta{margin-top:42px;font-size:13px;color:var(--ink-soft);line-height:1.6;
    background:rgba(255,255,255,.4);border-left:3px solid var(--gold);padding:14px 18px;border-radius:0 6px 6px 0}
  .meta b{color:var(--ink)}

  footer{margin-top:auto;padding:30px 28px 22px;text-align:center;font-size:11.5px;color:var(--ink-soft);line-height:1.7}
  footer a{color:var(--ink-soft);text-decoration:underline;text-underline-offset:2px}
  footer a:hover{color:var(--vermilion-deep)}
</style>
</head>
<body>
<main>
  <header>
    <div class="kicker">japan-learning</div>
    <h1><span class="jp">日本語</span>curriculum</h1>
    <p class="lede">A 13-module Japanese curriculum aimed at conversational mastery, plus two browser-based kana tools.</p>
  </header>

  <section class="cards">
    <a class="card" href="/kana">
      <div class="ch jp">あ<span class="small">ア</span></div>
      <h2>Interactive Kana Guide</h2>
      <p>Every hiragana &amp; katakana with stroke-order animation, browser audio, mnemonics, look-alike warnings, and a built-in recognition + recall quiz.</p>
      <span class="arrow">Open</span>
    </a>
    <a class="card" href="/chart">
      <div class="ch jp">表</div>
      <h2>Printable Recall Chart</h2>
      <p>Four-page A4 chart — Study sides with kana &amp; picture mnemonics, Test sides for self-quizzing, romaji on foldable answer strips. Cmd+P → PDF.</p>
      <span class="arrow">Open</span>
    </a>
  </section>

  <section class="curriculum" id="curriculum">
    <h2 class="section-title">Curriculum</h2>
    <p class="lede">13 modules, M00 → M12. Conversational-mastery ladder, not JLPT order.</p>
    <div class="module-grid">
      {{MODULE_CARDS}}
    </div>
  </section>

  <p class="meta">
    <b>Pedagogy:</b> on-demand, never always-on. Mnemonics bridge shape→sound; romaji
    lives on foldable strips, not in-cell; the quiz forces retrieval. Pair with Anki +
    Yomitan + daily comprehensible input.
  </p>
</main>
<footer>
  Source &middot;
  <a href="https://github.com/rolivischi2/japanese-tutor" target="_blank" rel="noopener">github.com/rolivischi2/japanese-tutor</a>
  &middot; Stroke data from <a href="https://kanjivg.tagaini.net/" target="_blank" rel="noopener">KanjiVG</a> (CC BY-SA 3.0)
</footer>
</body>
</html>
```

- [ ] **Step 2: Add `build_landing()` to build_site.py**

Insert after `render_module`:

```python
def _render_module_card(module: ModuleMeta) -> str:
    """Single module card. Locked → div, otherwise → anchor."""
    href = f"/modules/{module.slug}/"
    pill = f'<span class="status-pill {module.status}">{module.status}</span>'
    inner = (
        f'<div class="module-num">M{module.number}</div>\n'
        f'        <h3>{module.title}</h3>\n'
        f'        <p class="key-grammar jp">{module.key_grammar}</p>\n'
        f'        {pill}'
    )
    if module.status == "locked":
        return f'<div class="card module-card locked">\n        {inner}\n      </div>'
    return f'<a class="card module-card" href="{href}">\n        {inner}\n      </a>'


def build_landing(modules: dict[str, ModuleMeta], template: str) -> str:
    cards = "\n      ".join(
        _render_module_card(modules[s]) for s in sorted(modules)
    )
    return template.replace("{{MODULE_CARDS}}", cards)
```

- [ ] **Step 3: Extend `main()` to write the landing**

Replace the body of `main()`:

```python
def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_tests()

    page_template = (TEMPLATES_DIR / "page.html").read_text(encoding="utf-8")
    landing_template = (TEMPLATES_DIR / "landing.html").read_text(encoding="utf-8")
    modules = parse_index_md(ROOT / "INDEX.md", MODULES_DIR)

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)
    (OUT_DIR / "kana").mkdir()
    (OUT_DIR / "chart").mkdir()

    total = 0
    for slug in sorted(modules):
        total += render_module(modules[slug], OUT_DIR, page_template)

    landing_html = build_landing(modules, landing_template)
    (OUT_DIR / "index.html").write_text(landing_html, encoding="utf-8")

    print(f"Rendered {total} module page(s) into {OUT_DIR}/modules/")
    print(f"Wrote landing → {OUT_DIR}/index.html")
    return 0
```

(The `kana/` and `chart/` directories are created here so `build-vercel.sh` can `cp` into them without an extra `mkdir`.)

- [ ] **Step 4: Run the full build and inspect**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
uv run tools/build_site.py
ls public/
ls public/modules/
head -30 public/index.html
grep -o 'class="card module-card[^"]*"' public/index.html | sort | uniq -c
```

Expected:
- `public/` contains `index.html`, `kana/`, `chart/`, `modules/`
- `public/modules/` contains 13 module directories
- Landing HTML head shows the new title; the `<section class="curriculum">` section exists
- Card-class grep shows ~2 active/done cards + ~11 locked cards (matches current INDEX.md statuses)

- [ ] **Step 5: Self-tests still pass**

```bash
uv run tools/build_site.py --self-test
```
Expected: `PASS (13/13)`.

- [ ] **Step 6: Commit**

```bash
git add tools/build_site.py tools/templates/landing.html
git commit -m "$(cat <<'EOF'
Generate landing page with curriculum index from build_site.py

Adds tools/templates/landing.html (replaces scripts/landing.html as the
source of truth) and build_landing() which injects a module card grid
read from INDEX.md. Locked modules render as muted, non-clickable cards.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 9: Update `scripts/build-vercel.sh`, delete `scripts/landing.html`

**Files:**
- Modify: `scripts/build-vercel.sh`
- Delete: `scripts/landing.html`

- [ ] **Step 1: Rewrite the build script**

Replace `scripts/build-vercel.sh` with:

```bash
#!/usr/bin/env bash
# Vercel build step. Generates the landing + rendered module pages via
# tools/build_site.py, then copies the two standalone HTML artifacts
# (kana guide, printable chart) into public/. The rest of the repo
# (Markdown lessons, vocab CSVs, Python tools, .venv, etc.) stays out
# of the deployed site.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/public"

# build_site.py wipes and recreates $OUT, including empty kana/ and chart/
# subdirectories. Subsequent cp commands populate those subdirectories.
uv run "$ROOT/tools/build_site.py"

cp "$ROOT/modules/00-writing-systems/kana-guide.html" "$OUT/kana/index.html"
cp "$ROOT/pronunciation/11-kana-printable-chart.html" "$OUT/chart/index.html"

echo
echo "Built $OUT/"
echo "  /                        → $OUT/index.html"
echo "  /kana                    → $OUT/kana/index.html"
echo "  /chart                   → $OUT/chart/index.html"
echo "  /modules/<slug>/...      → $OUT/modules/"
du -sh "$OUT"
```

- [ ] **Step 2: Delete `scripts/landing.html`**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
git rm scripts/landing.html
```

- [ ] **Step 3: Run the full build script end-to-end**

```bash
bash scripts/build-vercel.sh
```

Expected: exits 0, prints "Built …" summary, `public/index.html`, `public/kana/index.html`, `public/chart/index.html`, and `public/modules/<slug>/...` all exist.

- [ ] **Step 4: Verify no Roland/Preply leaked into the rendered output**

```bash
grep -l "Roland\|Preply" public/ -r 2>/dev/null
```
Expected: no output (all source files were already generalized in prior work).

- [ ] **Step 5: Self-tests still pass**

```bash
uv run tools/build_site.py --self-test
```
Expected: `PASS (13/13)`.

- [ ] **Step 6: Commit**

```bash
git add scripts/build-vercel.sh
git commit -m "$(cat <<'EOF'
Wire build_site.py into Vercel build; remove scripts/landing.html

build-vercel.sh now invokes tools/build_site.py to generate the landing
and module pages, then copies the two standalone kana-tools HTML
artifacts into the locations build_site.py prepared.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 10: Browser spot-check + verification before push

**Files:** none modified.

- [ ] **Step 1: Open the landing page in a browser**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
python -m http.server -d public 8765 &
HTTP_PID=$!
sleep 1
open http://localhost:8765/
```

Visually confirm:
- Background is solid `#f1e8d6` — no radial-gradient hotspots, no noise texture
- "Curriculum" section appears below the kana-tools cards
- Module cards show: M-number, title, key grammar, status pill
- M00 (done, gold pill), M01 (active, vermilion pill), M02–M12 (locked, muted, non-clickable)
- Clicking an M00 or M01 card navigates to the module page

- [ ] **Step 2: Open `/modules/01-copula-basics/` in the browser**

```bash
open http://localhost:8765/modules/01-copula-basics/
```

Visually confirm:
- Breadcrumb: Home › Module 01
- Sidebar lists all M01 files in the order: Overview, then numbered grammar files, then dialogues/exercises/self-talk
- Content renders the M01 overview with proper heading hierarchy
- Background is solid paper — same as landing
- Footer shows `Last updated: 2026-05-23` and a working GitHub source link

- [ ] **Step 3: Open `/modules/01-copula-basics/dialogues.html`**

```bash
open http://localhost:8765/modules/01-copula-basics/dialogues.html
```

Visually confirm:
- The three M01 dialogues render with kana visible and English glosses as blockquotes
- Character name is "Alex" (アレックス) throughout — no "Roland"
- The sidebar shows `Dialogues` highlighted as the current page

- [ ] **Step 4: Click cross-links to verify rewriting**

From the M01 overview, click the link to `dialogues.md` (rendered as `dialogues.html`) — should navigate internally. From any grammar file, click a link to another grammar file — should resolve to `.html`. Any link to a non-module file (e.g. `pronunciation/07-...`) should open on GitHub.

- [ ] **Step 5: Kill the local server**

```bash
kill $HTTP_PID
```

- [ ] **Step 6: Run validate.py to confirm no curriculum data regressions**

```bash
uv run python tools/validate.py
```
Expected: PASS.

- [ ] **Step 7: Commit nothing (this is verification only)**

If steps 1-3 surfaced any rendering bugs, fix them in build_site.py / templates and re-run the build. Only proceed to push once the browser checks pass.

---

## Task 11: Push and verify deployed site

**Files:** none modified.

- [ ] **Step 1: Push**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
git push origin main
```

- [ ] **Step 2: Wait briefly for Vercel build, then verify deployed pages**

```bash
sleep 90
curl -sI https://japan-learning-omega.vercel.app/ | head -5
curl -sI https://japan-learning-omega.vercel.app/modules/01-copula-basics/ | head -5
curl -sI https://japan-learning-omega.vercel.app/modules/01-copula-basics/dialogues.html | head -5
```
Expected: each curl returns `HTTP/2 200`.

- [ ] **Step 3: Confirm the deployed landing contains the curriculum section**

```bash
curl -s https://japan-learning-omega.vercel.app/ | grep -o 'class="curriculum"\|class="module-grid"\|M01.*Copula' | head -5
```
Expected: at least the `curriculum` and `module-grid` markers appear in the rendered HTML.

- [ ] **Step 4: If Vercel build failed**

If any of the curl checks return 404 or 500, fetch the Vercel deployment logs (user can paste them) and diagnose. Common failure modes:
- uv not available in the Vercel build environment → may need to install in build-vercel.sh
- Network sandbox blocks PEP 723 dep resolution → fall back to `pyproject.toml` deps

Report the issue with the failing curl + likely cause; do not silently retry.

---

## Notes on style

- All Python uses double quotes for strings, follows PEP 8 line widths (~88 chars).
- HTML templates: 2-space indent. Lowercase tag names. Self-closing void elements as `<meta>` not `<meta />`.
- The placeholder character `Alex` introduced in earlier work stays unchanged — this plan does not touch curriculum content.
- The `tools/templates/.gitkeep` file created in Task 1 can be `git rm`'d once `landing.html` and `page.html` are both in the directory. Optional — leaving it is harmless.
