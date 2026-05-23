---
title: Curriculum index + on-site Markdown rendering + landing-page background
date: 2026-05-23
status: approved
---

# Curriculum index + on-site Markdown rendering + landing-page background

## Goal

The deployed site (`japan-learning-omega.vercel.app`) currently surfaces only the kana tools. Add a curriculum index to the landing page that lists all 13 modules with status, and render each module's Markdown lessons as on-site HTML pages so visitors can read the curriculum without leaving the site. Also: clean up the landing background — drop the two radial-gradient hotspots and the SVG noise filter; use the solid `--paper` color.

## Non-goals

- No search.
- No styled rendering of JSON files (vocab, kanji master).
- No rendering of `pedagogy/`, `pronunciation/`, `tools/`, `kanji/`, `vocab/`, `tutor/`, `progress/`, `output-practice/`, or `listening/` directories. Modules only. (Spec scope: "Curriculum modules only.")
- No build-time link validation.
- No interactive features beyond what each Markdown file already contains.
- No backwards compatibility with the old landing — straight replacement.

## Decisions baked in

1. **Background:** solid `--paper #f1e8d6` across both the landing and every rendered module page. Remove the two `radial-gradient` layers and the `data:image/svg+xml` noise filter from `scripts/landing.html`. Module pages get the same solid background for consistency.
2. **Rendering toolchain:** Python `markdown` package via uv, declared with PEP 723 inline metadata (same pattern as `tools/export_to_anki.py`). No new system-level dependencies, no static site generator.
3. **Scope of rendered files:** every `.md` file under `modules/MXX-*/`. JSON files are not rendered — the module overview page gets a footnote linking to `module-vocab.json` on GitHub.
4. **Module status source-of-truth:** `INDEX.md`'s module status table. `build_site.py` parses it. Unknown / unparseable rows default to `locked` and emit a build-time warning.
5. **Landing card behaviour:** `done` and `active` modules are clickable cards linking to `/modules/<slug>/`. `locked` modules render as visually muted, non-clickable cards (status pill says "locked").
6. **URL structure:** `/modules/<slug>/` (e.g. `/modules/01-copula-basics/`) renders the module's `00-overview.md`. Other files in the module become `/modules/<slug>/<filename>.html` (e.g. `/modules/01-copula-basics/01-desu-copula.html`).
7. **Furigana:** both source forms (`<ruby>漢字<rt>かんじ</rt></ruby>` and shorthand `{漢字|かんじ}`) render correctly. Shorthand is preprocessed into the explicit `<ruby>` form before Markdown rendering. Preprocessing skips content inside backtick code spans and fenced code blocks.
8. **Cross-link rewriting:** Markdown links pointing to local `.md` files (e.g. `[X](./01-desu-copula.md)`, `[X](dialogues.md)`) get rewritten to `.html` extensions. Links to other modules' files use full path (e.g. `[Y](../02-existence-and-location/00-overview.md)` → `../02-existence-and-location/00-overview.html`). Links to non-module files (e.g. `pronunciation/07-...`, `tutor/01-...`) become GitHub source links (since those files aren't rendered on-site). External links pass through.
9. **Sidebar on module pages:** a simple list of every file in the same module, with the currently-viewed file highlighted. Order: `00-overview`, then the numbered grammar files in order, then `dialogues`, `exercises`, `self-talk`, then any other `.md`. The sidebar lives in the page template; the build script supplies the list per page.

## Scope of changes

### New files
- **`tools/build_site.py`** — Python script (PEP 723 header declaring `markdown` and `PyYAML` dependencies). Responsibilities:
  - Parse `INDEX.md` to get the module status table → dict keyed by module slug.
  - Walk `modules/MXX-*/`, collect all `.md` files, group by module.
  - For each module file: strip YAML frontmatter (extract `last_updated`), preprocess furigana shorthand, rewrite local `.md` links to `.html` (or to GitHub for non-module targets), render via the Python `markdown` lib (with `extensions=['fenced_code', 'tables', 'attr_list']`).
  - Inject the rendered HTML into `tools/templates/page.html` with substitutions for: page title, module title, breadcrumb, sidebar list, `last_updated`.
  - Write to `public/modules/<slug>/<file>.html`. The overview file goes to `public/modules/<slug>/index.html`.
  - Build a Python dict `{slug: {title, status, key_grammar, has_overview}}` representing the module index.
  - Render the landing page from a separate `tools/templates/landing.html` template, injecting both the kana-tools cards (preserved) and the new modules section.
  - Write the rendered landing to `public/index.html`.
  - Print a summary line per output file (matches the existing build-vercel.sh aesthetic).

- **`tools/templates/page.html`** — single HTML template for rendered module pages. Uses the same Fraunces / Noto Sans JP fonts, paper / vermilion / gold palette from the existing landing. Solid `--paper` background. Layout: header with breadcrumb (`Home › Module NN`), main two-column layout (sidebar with module file list on left, rendered content on right), footer with `last_updated` and source-link to GitHub. Mobile: sidebar collapses above main content. Uses CSS Grid; no JS required.

- **`tools/templates/landing.html`** — replaces `scripts/landing.html` as the source of truth for the landing page. Same kana-tools cards as before, plus a new "Curriculum" section with a grid of module cards. Solid `--paper` background. Template tokens `{{KANA_TOOLS_CARDS}}` and `{{MODULE_CARDS}}` substituted by `build_site.py`.

### Modified files
- **`scripts/build-vercel.sh`** — replace the three `cp` lines for `index.html`, `kana/index.html`, `chart/index.html` with:
  1. `cp` for `kana/index.html` and `chart/index.html` (these still come straight from `modules/00-writing-systems/kana-guide.html` and `pronunciation/11-kana-printable-chart.html`).
  2. `uv run tools/build_site.py` — generates `public/index.html` and `public/modules/...`.
  - The existing `du -h` summary line is updated to reflect the new outputs.

### Deleted files
- **`scripts/landing.html`** — replaced by `tools/templates/landing.html`. The old file is removed; build script no longer references it.

## Template / HTML structure

### `tools/templates/landing.html` (outline)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <!-- fonts + meta (same as current) -->
  <style>
    :root { --paper:#f1e8d6; --paper-2:#e9dcc2; --ink:#2b2620; --ink-soft:#6f6557;
            --vermilion:#bd3b2c; --vermilion-deep:#9c2f23; --gold:#b08a4a;
            --cell:#f7f0e0; --cell-line:#d8c8a6;
            --muted-cell:#ece1cb; --muted-text:#a39a8a; }
    body { background: var(--paper); /* no gradients, no noise */ ... }
    .status-pill { font-size:11px; letter-spacing:.08em; text-transform:uppercase; padding:2px 8px; border-radius:99px; }
    .status-done { background:var(--gold); color:#fff; }
    .status-active { background:var(--vermilion); color:#fff; }
    .status-locked { background:transparent; color:var(--muted-text); border:1px solid var(--cell-line); }
    .card.locked { background:var(--muted-cell); color:var(--muted-text); cursor:not-allowed; pointer-events:none; }
  </style>
</head>
<body>
  <main>
    <header><!-- existing header --></header>

    <section class="cards">
      {{KANA_TOOLS_CARDS}}  <!-- existing two cards, hand-edited in template -->
    </section>

    <section class="curriculum">
      <h2>Curriculum</h2>
      <p class="section-lede">13 modules, M00 → M12. Conversational-mastery ladder, not JLPT order.</p>
      <div class="module-grid">
        {{MODULE_CARDS}}
      </div>
    </section>

    <p class="meta">…existing pedagogy meta box…</p>
  </main>
  <footer>…existing footer…</footer>
</body>
</html>
```

A module card (generated by the script):

```html
<a class="card module-card" href="/modules/01-copula-basics/">
  <div class="module-num">M01</div>
  <h3>Copula Basics</h3>
  <p class="key-grammar">です、じゃない、は、か、の</p>
  <span class="status-pill status-active">active</span>
</a>
```

A locked module card:

```html
<div class="card module-card locked">
  <div class="module-num">M05</div>
  <h3>Te-form</h3>
  <p class="key-grammar">て-form, 11 uses</p>
  <span class="status-pill status-locked">locked</span>
</div>
```

### `tools/templates/page.html` (outline)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>{{TITLE}} — japan-learning</title>
  <!-- fonts + same :root vars + body { background: var(--paper); } -->
  <style>
    .layout { display: grid; grid-template-columns: 220px 1fr; gap: 36px; }
    @media (max-width: 720px) { .layout { grid-template-columns: 1fr; } .sidebar { order: 2; } }
    .sidebar a.current { color: var(--vermilion); font-weight: 600; }
    article.content { font-size: 16.5px; line-height: 1.65; }
    article.content ruby rt { font-size: 0.6em; color: var(--ink-soft); }
    /* tables, code blocks, blockquotes styled per the kana-tools palette */
  </style>
</head>
<body>
  <main>
    <nav class="breadcrumb"><a href="/">Home</a> › <a href="/#modules">Module {{MODULE_NUM}}</a></nav>
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
    Last updated: {{LAST_UPDATED}} ·
    <a href="https://github.com/rolivischi2/japanese-tutor/blob/main/{{SOURCE_PATH}}">View source on GitHub</a>
  </footer>
</body>
</html>
```

## Build sequence (per `scripts/build-vercel.sh`)

1. Wipe and recreate `public/`.
2. Copy `modules/00-writing-systems/kana-guide.html` → `public/kana/index.html`.
3. Copy `pronunciation/11-kana-printable-chart.html` → `public/chart/index.html`.
4. Run `uv run tools/build_site.py`. This:
   - Parses `INDEX.md` for module statuses.
   - Walks `modules/`, renders each `.md` to a styled HTML page under `public/modules/<slug>/`.
   - Writes `public/index.html` (the landing) with the kana-tools cards + module-grid.
5. Print summary of generated files.

## INDEX.md parsing rules

`build_site.py` reads `INDEX.md` and looks for the markdown table starting `| Module | Status |`. For each row:
- Slug: extract from the "Module" column text (e.g. `M00 — Writing Systems` → look up the matching `modules/00-*` directory).
- Title: same column, stripped of the `MXX — ` prefix.
- Status: from the "Status" column, exact lowercase match for `done`, `active`, or `locked`.
- Key grammar: from the "Key grammar" column verbatim.

If a row's status string isn't one of the three, default to `locked` and emit `WARN: unknown status '...' for module XX, defaulting to locked`.

If a `modules/MXX-*` directory exists but isn't in the INDEX.md table, emit `WARN: module XX has no INDEX.md row` and default to `locked`.

If a row references a slug whose directory doesn't exist, skip the row and emit `WARN: INDEX row 'MXX' has no matching modules/ directory`.

## Furigana preprocessing

Regex: `\{([^{}|]+)\|([^{}|]+)\}` matched outside backtick code spans and fenced code blocks. Replacement: `<ruby>\1<rt>\2</rt></ruby>`.

Implementation: split the source by fenced code blocks (```…```) and inline code spans (`...`), apply the regex only to non-code chunks, then rejoin. Keep the implementation small — ~20 LOC.

## Link rewriting rules

Regex match all Markdown link targets: `\]\(([^)]+)\)`.

For each target `t`:
- If `t` starts with `http://`, `https://`, `mailto:`, or `#` → pass through unchanged.
- Else strip a leading `./`, then:
  - If `t` ends with `.md` and resolves (relative to the current file's directory) to a path under `modules/`: replace `.md` with `.html`. Special-case: if it resolves to `<module>/00-overview.md`, rewrite to `<module>/index.html` so URLs are clean.
  - If `t` ends with `.md` but resolves outside `modules/`: rewrite to a GitHub blob URL: `https://github.com/rolivischi2/japanese-tutor/blob/main/<resolved-path>`.
  - If `t` ends with `.json` or any other extension → leave unchanged (or rewrite to GitHub blob — keep simple: just rewrite to GitHub).
  - If `t` has no extension (e.g. `[X](../pronunciation/)`): leave unchanged.

## Verification

- `bash scripts/build-vercel.sh` runs locally without error.
- `public/index.html` exists; opens in a browser; the kana-tools cards still work; a new Curriculum section shows 13 module cards with status badges; the M00 and M01 cards link to `/modules/00-writing-systems/` and `/modules/01-copula-basics/`.
- `public/modules/01-copula-basics/index.html` renders the overview with furigana visible, sidebar listing the seven M01 files, breadcrumb back to home, last_updated footer.
- `public/modules/01-copula-basics/dialogues.html` renders the three dialogues with the kana visible and the English glosses as blockquotes.
- Background on all pages is solid `#f1e8d6` — no radial gradient, no noise texture.
- Locked module cards (M02–M12) are visually muted and not clickable (verify by attempting to click).
- `uv run python tools/validate.py` still PASSes (this work doesn't touch curriculum data).
- After push: `curl -sI https://japan-learning-omega.vercel.app` returns 200; `curl -sI https://japan-learning-omega.vercel.app/modules/01-copula-basics/` returns 200.

## Risks

- **`markdown` package quirks with Japanese punctuation** — mitigation: spot-check a rendered M01 page in a browser before committing.
- **`INDEX.md` table parse drift** — mitigated by the warning-and-default behaviour above.
- **`{漢字|かんじ}` preprocessing leaking into code spans** — mitigated by the split-around-code-blocks approach. A test case: include a line like `` Use the shorthand `{漢字|かんじ}` `` in some module file; the rendered page should show the literal shorthand in the code span, not `<ruby>`.
- **Vercel build environment** — uv must be available. Per the existing `pyproject.toml` + `uv.lock` + `tools/build_kana_guide.py` pattern, `scripts/build-vercel.sh` already assumes uv. If Vercel's build image lacks uv, the existing build already fails today — this spec adds nothing new on that front. (Standard fix: install uv in `build-vercel.sh` before invocation, but only if needed.)
- **Locked modules with empty content** — M02–M12 overview files exist and have real content; only their drills/dialogues are missing. Rendering the overview is fine. The sidebar for a locked module will show only `00-overview` and (potentially) link to the empty `module-vocab.json` via the footnote.
