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

import json
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
    - module-vocab.json targets (with optional #anchor) inside modules/ →
      vocab.html with the same anchor (the JSON is rendered as vocab.html)
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
        # module-vocab.json → vocab.html (preserving #anchor / ?query)
        if target.endswith("module-vocab.json"):
            resolved = (current_md_path.parent / target).resolve()
            try:
                rel = resolved.relative_to(ROOT)
            except ValueError:
                return match.group(0)
            if rel.parts and rel.parts[0] == "modules":
                new_target = target[:-len("module-vocab.json")] + "vocab.html"
                return f'href="{new_target}{suffix}"'
            return f'href="{GITHUB_BLOB}/{rel.as_posix()}{suffix}"'
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
    m = re.match(r"^(\d{2})-", base)
    if m:
        return (10 + int(m.group(1)), base)
    return (200, base)


def _human_title(slug: str) -> str:
    """Turn '01-desu-copula' → 'Desu copula'."""
    base = slug.removesuffix(".md")
    m = re.match(r"^\d{2}-(.*)$", base)
    core = m.group(1) if m else base
    return core.replace("-", " ").capitalize()


def _render_sidebar(
    module: ModuleMeta,
    files: list[Path],
    current: Path,
    include_vocab: bool = False,
    current_is_vocab: bool = False,
) -> str:
    items: list[str] = []
    for f in sorted(files, key=lambda p: _sidebar_sort_key(p.name)):
        is_current = f.resolve() == current.resolve() and not current_is_vocab
        href = "index.html" if f.name == "00-overview.md" else f.name.replace(".md", ".html")
        label = "Overview" if f.name == "00-overview.md" else _human_title(f.name)
        cls = ' class="current"' if is_current else ""
        items.append(f'<li><a href="{href}"{cls}>{label}</a></li>')
    if include_vocab:
        cls = ' class="current"' if current_is_vocab else ""
        items.append(f'<li><a href="vocab.html"{cls}>Vocabulary</a></li>')
    return "\n        ".join(items)


def render_vocab_html(json_path: Path) -> str:
    """Render module-vocab.json as the inner HTML body for a vocab page.

    Each entry gets an <h3 id="..."> so links like module-vocab.json#watashi
    (now rewritten to vocab.html#watashi) scroll to the right entry.
    """
    import html as _html
    data = json.loads(json_path.read_text(encoding="utf-8"))
    if not data:
        return "<p>No vocabulary entries yet.</p>"

    def esc(s):
        return _html.escape(str(s), quote=True)

    out = ["<h1>Vocabulary</h1>"]
    out.append(f"<p><em>{len(data)} entries. Each id links from cross-references"
               f" in the grammar files.</em></p>")
    out.append("<hr>")
    for entry in data:
        eid = esc(entry.get("id", ""))
        kana = esc(entry.get("kana", ""))
        kanji = entry.get("kanji")
        kanji_html = f" <span class=\"jp\" style=\"color:var(--ink-soft);font-weight:400\">({esc(kanji)})</span>" if kanji else ""
        english_list = entry.get("english") or []
        english = ", ".join(esc(e) for e in english_list)
        reading = entry.get("reading")
        pos = entry.get("pos") or ""
        pitch = entry.get("pitch_accent") or {}
        notes = entry.get("notes")
        examples = entry.get("example_sentences") or []
        tags = entry.get("tags") or []

        out.append(f'<section id="{eid}" style="margin:22px 0;padding-bottom:18px;border-bottom:1px dashed var(--cell-line)">')
        out.append(f'<h3 class="jp" style="font-size:22px;margin:0 0 4px">{kana}{kanji_html} '
                   f'<span style="font-family:Fraunces,serif;color:var(--ink-soft);font-size:.75em;font-weight:400">— {english}</span></h3>')
        bits = []
        if reading and reading != entry.get("kana"):
            bits.append(f"reading: <span class=\"jp\">{esc(reading)}</span>")
        if pos:
            bits.append(f"{esc(pos)}")
        if pitch.get("pattern"):
            drop = pitch.get("drop_after_mora")
            pp = esc(pitch["pattern"])
            if drop is not None and drop != 0:
                pp += f" (drop after mora {drop})"
            bits.append(f"pitch: {pp}")
        if bits:
            out.append(f'<p style="font-size:13.5px;color:var(--ink-soft);margin:0 0 8px">{" · ".join(bits)}</p>')
        if notes:
            out.append(f'<p style="font-size:14px;margin:6px 0">{esc(notes)}</p>')
        if examples:
            out.append("<ul style=\"margin-top:6px\">")
            for ex in examples:
                k = esc(ex.get("kana", ""))
                e = esc(ex.get("english", ""))
                out.append(f'<li><span class="jp">{k}</span> — <span style="color:var(--ink-soft)">{e}</span></li>')
            out.append("</ul>")
        if tags:
            tag_html = " ".join(
                f'<span style="display:inline-block;font-size:11px;letter-spacing:.06em;text-transform:lowercase;background:var(--cell);color:var(--ink-soft);padding:1px 8px;border-radius:99px;margin-right:4px">{esc(t)}</span>'
                for t in tags
            )
            out.append(f'<p style="margin-top:8px">{tag_html}</p>')
        out.append("</section>")
    return "\n".join(out)


def render_md_file(
    md_path: Path,
    module: ModuleMeta,
    sibling_md_files: list[Path],
    template: str,
    has_vocab: bool = False,
) -> str:
    """Render one .md file to a full HTML page string."""
    raw = md_path.read_text(encoding="utf-8")
    frontmatter, body = strip_frontmatter(raw)
    body = preprocess_furigana(body)

    md = md_lib.Markdown(extensions=["fenced_code", "tables", "attr_list"])
    rendered = md.convert(body)
    rendered = rewrite_links(rendered, md_path)

    page_title = module.title if md_path.name == "00-overview.md" else _human_title(md_path.name)
    sidebar = _render_sidebar(module, sibling_md_files, md_path, include_vocab=has_vocab)
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
    """Render all .md files (and module-vocab.json if non-empty) for a module.

    Returns the number of HTML files written.
    """
    src_dir = MODULES_DIR / module.slug
    md_files = sorted(src_dir.glob("*.md"))
    if not md_files:
        return 0

    vocab_path = src_dir / "module-vocab.json"
    has_vocab = False
    if vocab_path.exists():
        try:
            data = json.loads(vocab_path.read_text(encoding="utf-8"))
            has_vocab = bool(data)
        except json.JSONDecodeError:
            has_vocab = False

    target = out_dir / "modules" / module.slug
    target.mkdir(parents=True, exist_ok=True)
    written = 0
    for f in md_files:
        html = render_md_file(f, module, md_files, template, has_vocab=has_vocab)
        out_name = "index.html" if f.name == "00-overview.md" else f.name.replace(".md", ".html")
        (target / out_name).write_text(html, encoding="utf-8")
        written += 1

    if has_vocab:
        vocab_body = render_vocab_html(vocab_path)
        sidebar = _render_sidebar(
            module, md_files, vocab_path,
            include_vocab=True, current_is_vocab=True,
        )
        rel_source = vocab_path.relative_to(ROOT).as_posix()
        page_html = (template
            .replace("{{TITLE}}", f"{module.title} — Vocabulary")
            .replace("{{MODULE_NUM}}", module.number)
            .replace("{{MODULE_TITLE}}", f"M{module.number} — {module.title}")
            .replace("{{SIDEBAR_LIST}}", sidebar)
            .replace("{{RENDERED_HTML}}", vocab_body)
            .replace("{{LAST_UPDATED}}", "—")
            .replace("{{SOURCE_URL}}", f"{GITHUB_BLOB}/{rel_source}")
        )
        (target / "vocab.html").write_text(page_html, encoding="utf-8")
        written += 1

    return written


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


def _english_sort_key(text: str) -> str:
    """Lowercase + strip leading articles + punctuation for sort ordering."""
    s = (text or "").strip().lower()
    for prefix in ("a ", "an ", "the ", "to "):
        if s.startswith(prefix):
            s = s[len(prefix):]
            break
    s = re.sub(r"[^a-z0-9\s]", "", s)
    return s.strip()


def build_dict_index(modules_dir: Path) -> list[dict]:
    """Walk every module-vocab.json, flatten to a list of word + phrase entries."""
    entries: list[dict] = []
    for d in sorted(modules_dir.iterdir()):
        if not d.is_dir():
            continue
        vocab_path = d / "module-vocab.json"
        if not vocab_path.exists():
            continue
        try:
            data = json.loads(vocab_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if not data:
            continue
        module_num = d.name.split("-", 1)[0]
        for v in data:
            vid = v.get("id", "")
            kana = v.get("kana", "")
            kanji = v.get("kanji")
            reading = v.get("reading") or kana
            english_list = v.get("english") or []
            english = ", ".join(english_list)
            pos = v.get("pos") or ""
            pitch = (v.get("pitch_accent") or {}).get("pattern") or ""
            tags = v.get("tags") or []
            search_parts = [
                vid, kana, reading, english.lower(), pos, " ".join(tags),
            ]
            if kanji:
                search_parts.append(kanji)
            search_text = " ".join(s for s in search_parts if s).lower()
            entries.append({
                "type": "word",
                "module_slug": d.name,
                "module_num": module_num,
                "id": vid,
                "kana": kana,
                "kanji": kanji,
                "reading": reading,
                "english": english,
                "english_first": _english_sort_key(english_list[0]) if english_list else "",
                "english_list": english_list,
                "pos": pos,
                "pitch": pitch,
                "tags": tags,
                "search_text": search_text,
            })
            for ex in (v.get("example_sentences") or []):
                ex_kana = ex.get("kana", "")
                ex_eng = ex.get("english", "")
                ex_kanji = ex.get("kanji")
                ex_search = " ".join(filter(None, [ex_kana, ex_kanji or "", ex_eng.lower()]))
                entries.append({
                    "type": "example",
                    "module_slug": d.name,
                    "module_num": module_num,
                    "parent_id": vid,
                    "kana": ex_kana,
                    "kanji": ex_kanji,
                    "english": ex_eng,
                    "english_first": _english_sort_key(ex_eng),
                    "search_text": ex_search,
                })
    return entries


def render_dict_page(template: str, index: list[dict]) -> str:
    """Inject the index data inline into the dict.html template."""
    data_json = json.dumps(index, ensure_ascii=False, separators=(",", ":"))
    return template.replace("{{INDEX_JSON}}", data_json)


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return run_self_tests()

    page_template = (TEMPLATES_DIR / "page.html").read_text(encoding="utf-8")
    landing_template = (TEMPLATES_DIR / "landing.html").read_text(encoding="utf-8")
    dict_template = (TEMPLATES_DIR / "dict.html").read_text(encoding="utf-8")
    modules = parse_index_md(ROOT / "INDEX.md", MODULES_DIR)

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)
    (OUT_DIR / "kana").mkdir()
    (OUT_DIR / "chart").mkdir()
    (OUT_DIR / "reader").mkdir()
    (OUT_DIR / "dict").mkdir()

    total = 0
    for slug in sorted(modules):
        total += render_module(modules[slug], OUT_DIR, page_template)

    landing_html = build_landing(modules, landing_template)
    (OUT_DIR / "index.html").write_text(landing_html, encoding="utf-8")

    dict_index = build_dict_index(MODULES_DIR)
    dict_html = render_dict_page(dict_template, dict_index)
    (OUT_DIR / "dict" / "index.html").write_text(dict_html, encoding="utf-8")

    print(f"Rendered {total} module page(s) into {OUT_DIR}/modules/")
    print(f"Wrote landing → {OUT_DIR}/index.html")
    print(f"Wrote dictionary → {OUT_DIR}/dict/index.html ({len(dict_index)} entries)")
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

    # module-vocab.json#anchor → vocab.html#anchor (sibling)
    src = '<a href="module-vocab.json#watashi">X</a>'
    got = rewrite_links(src, current)
    if got != '<a href="vocab.html#watashi">X</a>':
        failures.append(f"rewrite_links vocab-sibling: got {got!r}")

    # ./module-vocab.json#foo → vocab.html#foo
    src = '<a href="./module-vocab.json#anata">X</a>'
    got = rewrite_links(src, current)
    if got != '<a href="./vocab.html#anata">X</a>':
        failures.append(f"rewrite_links vocab-dotslash: got {got!r}")

    n = 15
    if failures:
        print(f"build_site.py self-tests: FAIL ({len(failures)} failures, {n} cases)", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"build_site.py self-tests: PASS ({n}/{n})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
