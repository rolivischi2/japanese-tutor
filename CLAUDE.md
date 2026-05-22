# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A personal Japanese-language curriculum for one learner ("Roland") aimed at **conversational mastery**, not JLPT certification. It is a content repository — Markdown lessons, CSV/JSON vocab and kanji data, and two Python helper scripts — designed so Claude Code can extend it deterministically as the learner progresses.

**Current state:** the repo is unscaffolded. `INSTRUCTIONS.md` is the complete blueprint and the source of truth. Read it before doing anything substantive. Nothing else exists yet: the directory tree, content files, and tools all still need to be built.

## First-time scaffolding tasks

`INSTRUCTIONS.md` §6 defines the initial deliverables, in order:

1. Scaffold the full directory tree (§2 of `INSTRUCTIONS.md`) as files with frontmatter populated and `TODO` markers per section.
2. Populate `vocab/tier-1-core-300.csv` (intersection of JLPT N5 + first 300 Kaishi 1.5k cards), conforming to `vocab/schema.json`, with pitch accent from the Kanjium dictionary.
3. Fully build **Module 00** (`modules/00-writing-systems/`) — the only module completed at scaffold time. All later modules are filled in chapter-by-chapter as the learner advances.
4. Author `tools/validate.py` and `tools/export_to_anki.py` (see Tools below).

## Commands

No build/test tooling exists yet. Once authored, the two scripts are the only commands:

- `python tools/validate.py` — checks every kanji used in any module's `dialogues.md` exists in `kanji/kanji-master.json` with `module_introduced` ≤ that module's number, and every vocab `id` referenced by a kanji entry exists in a tier CSV. Run this after editing any module content, vocab, or kanji data.
- `python tools/export_to_anki.py` — regenerates `tier-1`, `tier-2`, `tier-3`, and `kanji` `.apkg` decks from the CSV/JSON sources.

## Content authoring conventions (the Claude Code contract)

These rules are non-negotiable; they keep content consistent across modules built months apart.

- **Frontmatter:** every `.md` file starts with `--- module: NN file: <slug> lang_focus: <grammar|vocab|...> kanji_level: <range> last_updated: YYYY-MM-DD ---`.
- **Example sentences:** three lines — kana, then kanji-with-furigana (only if the kanji has already been introduced by an earlier module), then English gloss.
- **Romaji is forbidden** everywhere except files under `pronunciation/`.
- **Furigana:** use `<ruby>漢字<rt>かんじ</rt></ruby>` or the shorthand `{漢字|かんじ}`.
- **Kanji gating:** a module may only use kanji introduced in that module or an earlier one. `validate.py` enforces this.
- **Cross-linking:** every grammar point links each example word to its `vocab/` entry by `id`.
- **Data schemas:** vocab entries follow `vocab/schema.json`; kanji entries follow the structure in `INSTRUCTIONS.md` §3.7. `kanji/kanji-by-module.csv` is denormalised and regenerated from `kanji/kanji-master.json` — never hand-edit the CSV.

Each `modules/NN-*/` folder contains: `00-overview.md`, one `.md` per grammar concept, `dialogues.md`, `exercises.md`, `self-talk.md` (M01+), `kanji-introduced.md` (M04+), and `module-vocab.json`.

## Permissions

- **May:** scaffold new module folders, add vocab/kanji rows, regenerate `kanji-by-module.csv` from `kanji-master.json`, build module drills and dialogues on request.
- **Must NOT:** rewrite anything under `pedagogy/` without an explicit prompt — those files encode deliberate pedagogical decisions.

## Architecture and pedagogy you must respect

The 13-module curriculum (M00–M12) is a "verb-form complexity ladder," not a JLPT-ordered one. Three deliberate departures from standard textbooks drive content decisions — do not "correct" them toward Genki orthodoxy:

1. **Polite-first, plain-form-fast.** Modules 01–05 use ます/です. Module 06 introduces plain forms aggressively (Genki delays this to ~Lesson 11). From M07 onward, structures are shown in side-by-side polite/plain tables.
2. **Comprehensible input from Day 1** — listening resources start in Module 00, not at the end.
3. **Pitch accent taught from Module 00** — the learner's Hungarian L1 imposes first-mora intensity stress, so pitch drilling is front-loaded.

Other intentional ordering choices: existence verbs (あります/います) before adjectives; te-form gets its own module (M05); plain forms (M06) precede sentence-ending particles (M07). The learner's Hungarian L1 / German (Swiss German) L2 background drives specific pronunciation content — see `INSTRUCTIONS.md` §1.3.

**The repo is self-extending:** when the learner finishes Module N, the workflow is "build Module N+1's drills and dialogues from its overview." Claude Code reads these conventions and produces consistent content. The learner's current position is **Module 01** (per `INSTRUCTIONS.md` §3.5).
