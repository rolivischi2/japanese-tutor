---
module: meta
file: tools-readme
lang_focus: tooling
kanji_level: 0
last_updated: 2026-05-22
---

# tools/

Two Python 3 helper scripts for the japan-learning knowledge base.
Standard library only for `validate.py`; `export_to_anki.py` requires `genanki`.

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
python3 tools/validate.py

# With explicit repo root (useful if running from a different directory):
python3 tools/validate.py --repo-root /path/to/japan-learning

# Help:
python3 tools/validate.py --help
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

**Dependencies:**

```bash
pip install genanki
```

If `genanki` is not installed the script prints a clear message and exits 0.

**How to run:**

```bash
# From the repo root:
python3 tools/export_to_anki.py

# Custom output directory:
python3 tools/export_to_anki.py --output-dir /path/to/output

# Help:
python3 tools/export_to_anki.py --help
```

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
python3 tools/build_kana_guide.py
```

The generated `kana-guide.html` is committed to the repo; open it directly in
any browser (no server needed).

---

## Dependency summary

| Script                 | External dependencies |
|------------------------|-----------------------|
| `validate.py`          | None (stdlib only)    |
| `build_kana_guide.py`  | None (stdlib only)    |
| `export_to_anki.py`    | `genanki` (`pip install genanki`) |
