# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A Japanese-language curriculum aimed at **conversational mastery**, not JLPT certification. It is a content repository — Markdown lessons, CSV/JSON vocab and kanji data, and two Python helper scripts — designed so Claude Code can extend it deterministically as the learner progresses.

**Current state:** the directory tree is fully scaffolded, **Module 00** (writing systems) and **Module 01** (copula basics) are built, and the helper scripts exist. Modules 02–12 have `00-overview.md` and `module-vocab.json` only — their drills and dialogues are filled in chapter-by-chapter as the learner advances. `INSTRUCTIONS.md` is the original blueprint and the source of truth for pedagogy and per-module content outlines (§3.5); consult it before authoring any module. `INDEX.md` holds the live module status table (locked/active/done) — it is the authoritative record of the learner's current position.

## Extending the curriculum

The repo is **self-extending**: when the learner finishes Module N, the request is "build Module N+1's drills and dialogues from its overview." To do that:

1. Read the module's existing `00-overview.md` and the matching outline in `INSTRUCTIONS.md` §3.5.
2. Author the per-concept grammar `.md` files, `dialogues.md`, `exercises.md`, `self-talk.md`, and (M04+) `kanji-introduced.md`, following the authoring conventions below.
3. Add new entries to `module-vocab.json` and the relevant `vocab/tier-*.csv`; add kanji to `kanji/kanji-master.json`.
4. Run `python tools/validate.py` and fix any reported errors.
5. Update the status row in `INDEX.md`.

## Commands

Python is managed by **uv**. Never invoke the system `python3` directly — always go through `uv run` so the project's pinned Python (3.13 per `.python-version`) and ephemeral dependencies are used. First-time setup: `uv sync`. Standard library only for `validate.py` and `build_kana_guide.py`; `export_to_anki.py` declares `genanki` via PEP 723 inline metadata so uv resolves it ephemerally without any global install.

- `uv run python tools/validate.py` — checks every kanji used in any module's `dialogues.md` exists in `kanji/kanji-master.json` with `module_introduced` ≤ that module's number, every vocab `id` in a kanji entry's `vocab_using` exists in a tier CSV, and every `module-vocab.json` entry has the schema-required fields. Run this after editing any module content, vocab, or kanji data.
- `uv run tools/export_to_anki.py` — regenerates `tier-1`, `tier-2`, `tier-3`, and `kanji` `.apkg` decks into `vocab/anki-export/`. uv pulls `genanki` ephemerally via the script's PEP 723 header. `.apkg` files are gitignored.
- `uv run python tools/build_kana_guide.py` — regenerates the self-contained interactive `modules/00-writing-systems/kana-guide.html` from `tools/data/kana-strokes.json`. Re-run after editing the stroke data or the kana metadata inside the script.

## Content authoring conventions (the Claude Code contract)

These rules are non-negotiable; they keep content consistent across modules built months apart.

- **Frontmatter:** every `.md` file starts with `--- module: NN file: <slug> lang_focus: <grammar|vocab|...> kanji_level: <range> last_updated: YYYY-MM-DD ---`.
- **Example sentences:** three lines — kana, then kanji-with-furigana (only if the kanji has already been introduced by an earlier module), then English gloss.
- **Romaji is forbidden** everywhere except files under `pronunciation/`.
- **Furigana:** use `<ruby>漢字<rt>かんじ</rt></ruby>` or the shorthand `{漢字|かんじ}`.
- **Kanji gating:** a module may only use kanji introduced in that module or an earlier one. `validate.py` enforces this.
- **Cross-linking:** every grammar point links each example word to its `vocab/` entry by `id`.
- **Data schemas:** vocab entries follow `vocab/schema.json`; kanji entries follow the structure in `INSTRUCTIONS.md` §3.7. `kanji/kanji-by-module.csv` is denormalised and regenerated from `kanji/kanji-master.json` — never hand-edit the CSV.

Each `modules/NN-*/` folder contains: `00-overview.md`, one `.md` per grammar concept, `dialogues.md`, `exercises.md`, `self-talk.md` (M01+), `kanji-introduced.md` (M04+), and `module-vocab.json`. The `tutor/` directory holds tutor-facing companion worksheets (e.g. `01-copula-companion.md`), one per module, named to match.

## Permissions

- **May:** scaffold new module folders, add vocab/kanji rows, regenerate `kanji-by-module.csv` from `kanji-master.json`, build module drills and dialogues on request.
- **Must NOT:** rewrite anything under `pedagogy/` without an explicit prompt — those files encode deliberate pedagogical decisions.

## Architecture and pedagogy you must respect

The 13-module curriculum (M00–M12) is a "verb-form complexity ladder," not a JLPT-ordered one. Three deliberate departures from standard textbooks drive content decisions — do not "correct" them toward Genki orthodoxy:

1. **Polite-first, plain-form-fast.** Modules 01–05 use ます/です. Module 06 introduces plain forms aggressively (Genki delays this to ~Lesson 11). From M07 onward, structures are shown in side-by-side polite/plain tables.
2. **Comprehensible input from Day 1** — listening resources start in Module 00, not at the end.
3. **Pitch accent taught from Module 00** — many L1s impose intensity stress that overrides Japanese pitch, so pitch drilling is front-loaded.

Other intentional ordering choices: existence verbs (あります/います) before adjectives; te-form gets its own module (M05); plain forms (M06) precede sentence-ending particles (M07). The pronunciation track ships with L1-specific transfer notes for Hungarian and German/Swiss-German speakers as examples (see `pronunciation/07-hungarian-transfer-notes.md`, `pronunciation/08-german-swiss-transfer-notes.md`). Forkers with other L1s should add their own file alongside.

The learner's current position is whatever module is marked `active` in `INDEX.md` (Module 01 at last update). When asked to build the next module, follow the workflow in "Extending the curriculum" above.
