---
module: meta
file: readme
lang_focus: meta
kanji_level: 0
last_updated: 2026-05-23
---

# Japanese Conversational-Mastery Curriculum

## What this repo is

A 13-module Japanese curriculum aimed at conversational mastery (not JLPT certification). Three opinionated departures from textbook orthodoxy: polite-first / plain-form-fast, comprehensible input from Day 1, and pitch accent taught from Module 00.

Content lives in Markdown; vocabulary in CSV/JSON; kanji in JSON. Two Python helpers (under `tools/`) regenerate the Anki deck and the interactive kana guide. Designed so Claude Code can extend it deterministically — see `CLAUDE.md`.

## Who it is for

Any adult learner who wants conversational Japanese. The pronunciation track includes optional L1-specific transfer notes (currently Hungarian in `pronunciation/07-hungarian-transfer-notes.md` and German/Swiss-German in `pronunciation/08-german-swiss-transfer-notes.md`) as examples — forkers are encouraged to add their own L1 file alongside.

## How to use this repo

1. Open `INDEX.md` to see module status (locked / active / done).
2. Open the active module's `00-overview.md`, then work through the grammar files in order.
3. Do `exercises.md` and `self-talk.md`.
4. Log progress in `progress/progress.md` and tutor sessions in `progress/tutor-lesson-log.md`.

`CLAUDE.md` describes how to extend the repo with Claude Code (build the next module's drills and dialogues from its overview).

## Daily routine (~65 min/day)

- 15 min Anki (new cards + reviews)
- 20 min current-module grammar/vocab
- 20 min listening (`listening/resources-by-level.md`)
- 10 min shadowing or self-talk output

## Dependencies

- [Anki](https://apps.ankiweb.net/) + the Kaishi 1.5k starter deck
- [Yomitan](https://github.com/yomidevs/yomitan) browser extension (see `tools/yomitan-setup.md`)
- Python 3.13 via [uv](https://docs.astral.sh/uv/) for the helper scripts
- Optional: Migaku (see `tools/migaku-setup.md`)

See `tools/` for setup guides for each.
