---
module: meta
file: tools-readme
lang_focus: tooling
kanji_level: 0
last_updated: 2026-05-23
---

# tools/

Three Python 3 helper scripts for the japan-learning knowledge base.
Python is managed by **uv** — never invoke the system `python3` directly. The
project's Python version is pinned in `.python-version` (3.13) and metadata
lives in `pyproject.toml`. First-time setup:

```bash
uv sync          # creates .venv with pinned Python, no third-party deps yet
```

`validate.py` and `build_kana_guide.py` are standard-library only and run under
the bare venv. `export_to_anki.py` needs `genanki` — its PEP 723 inline
metadata lets uv resolve that ephemerally, so no global install ever happens.

---

## validate.py

**What it does:** Consistency checker for the entire knowledge base.

Performs three checks:

1. **Kanji gating** — Every CJK character (U+4E00–U+9FFF) found in any
   `modules/NN-*/dialogues.md` must be present in `kanji/kanji-master.json`
   with `module_introduced` ≤ that module's number.

2. **vocab_using integrity** — Every vocab `id` listed in any
   `kanji/kanji-master.json` `vocab_using` array must appear in at least one
   tier CSV (`tier-1-core-300.csv`, `tier-2-expand-700.csv`, or
   `tier-3-fluency-1500.csv`).

3. **Structural validation** — Every `module-vocab.json` file must contain
   objects that have the required fields (`id`, `kana`, `reading`, `pos`,
   `english`, `module_introduced`) and valid `pos` enum values.

Missing or empty files are reported as "nothing to check" and never cause a
crash — this is expected for a partially scaffolded repo.

**Dependencies:** Python 3 standard library only.

**How to run:**

```bash
# From the repo root:
uv run python tools/validate.py

# With explicit repo root (useful if running from a different directory):
uv run python tools/validate.py --repo-root /path/to/japan-learning

# Help:
uv run python tools/validate.py --help
```

**Exit codes:** 0 = PASS, 1 = one or more errors found.

Run this script after editing any module dialogue, vocab entry, or kanji entry.

---

## export_to_anki.py

**What it does:** Converts the vocab tier CSVs and kanji CSV into Anki `.apkg`
deck files ready for import.

| Source file                     | Output deck               |
|---------------------------------|---------------------------|
| `vocab/tier-1-core-300.csv`     | `vocab/anki-export/tier-1.apkg` |
| `vocab/tier-2-expand-700.csv`   | `vocab/anki-export/tier-2.apkg` |
| `vocab/tier-3-fluency-1500.csv` | `vocab/anki-export/tier-3.apkg` |
| `kanji/kanji-by-module.csv`     | `vocab/anki-export/kanji.apkg`  |

Card format (vocab decks):
- **Front:** kana form (audio: TODO)
- **Back:** kanji form + English glosses + pitch accent + example sentence + module tag

Card format (kanji deck):
- **Front:** kanji character + "What does this kanji mean?"
- **Back:** primary meaning, on/kun readings, stroke count, example sentence

Header-only or absent CSV files are skipped gracefully with a message.

**Dependencies:** `genanki` (declared inline in the script's PEP 723 header).

**How to run:**

```bash
# From the repo root — uv resolves genanki ephemerally from the PEP 723 header:
uv run tools/export_to_anki.py

# Custom output directory:
uv run tools/export_to_anki.py --output-dir /path/to/output

# Help:
uv run tools/export_to_anki.py --help
```

Equivalent alternative using the named dependency group from `pyproject.toml`
(installs `genanki` into `.venv` persistently rather than ephemerally):

```bash
uv run --group anki python tools/export_to_anki.py
```

If `genanki` is not available the script prints a clear message and exits 0.

---

## build_kana_guide.py

**What it does:** Builds the interactive kana guide — a single self-contained
HTML file at `modules/00-writing-systems/kana-guide.html` with every hiragana
and katakana, stroke-order animation, browser audio, mnemonics, and a practice
quiz.

It reads stroke paths from `tools/data/kana-strokes.json` (extracted from
KanjiVG, CC BY-SA 3.0) and the curated kana metadata held inside the script
itself (romaji, mnemonics, look-alike clusters, pronunciation notes). Edit that
metadata in the script, then re-run to regenerate the guide.

**Dependencies:** Python 3 standard library only.

**How to run:**

```bash
uv run python tools/build_kana_guide.py
```

The generated `kana-guide.html` is committed to the repo; open it directly in
any browser (no server needed).

---

## Dependency summary

| Script                 | External dependencies | uv invocation |
|------------------------|-----------------------|---------------|
| `validate.py`          | None (stdlib only)    | `uv run python tools/validate.py` |
| `build_kana_guide.py`  | None (stdlib only)    | `uv run python tools/build_kana_guide.py` |
| `export_to_anki.py`    | `genanki` (declared inline via PEP 723) | `uv run tools/export_to_anki.py` |
