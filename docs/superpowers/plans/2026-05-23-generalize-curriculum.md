# Generalize Curriculum Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strip Roland-specific framing from the repo so it works for any forker, while preserving L1-specific pronunciation notes as clearly-labeled optional reference. End state: `grep` for `Roland`/`Preply`/etc. returns only acceptable hits; `validate.py` still passes; pushed to `main`.

**Architecture:** Sequential markdown sweep. No new code, no schema changes, no module content authored. Folder renames via `git mv` to preserve history. Verification is grep-based (assertions that certain strings are absent) plus a final `uv run python tools/validate.py`.

**Tech Stack:** Markdown, JSON, Python (uv), git. No frameworks.

---

## Pre-flight (Task 0)

### Task 0: Verify validate.py and tooling don't depend on `preply/` path

**Files:**
- Read: `tools/validate.py`
- Read: `tools/build_kana_guide.py`
- Read: `tools/export_to_anki.py`

- [ ] **Step 1: Confirm no tooling references `preply` or `Preply`**

Run: `grep -rn "preply\|Preply" tools/`
Expected: No hits in `validate.py`, `export_to_anki.py`. The build scripts only validate module schemas, not tutor files.

- [ ] **Step 2: Confirm validate.py currently passes on a clean tree**

Run: `uv run python tools/validate.py`
Expected: Exits 0 with a "validation OK" message (or similar). This gives us a baseline so any failure after edits is attributable to our changes.

- [ ] **Step 3: Save the baseline grep result for later comparison**

Run:
```bash
grep -rln "Roland\|rolivischi\|Hungarian\|hungarian\|Swiss German\|swiss german\|Preply\|preply" \
  --include="*.md" --include="*.html" --include="*.json" --include="*.py" \
  --exclude-dir=docs --exclude-dir=node_modules . | sort > /tmp/jp-baseline-hits.txt
wc -l /tmp/jp-baseline-hits.txt
```
Expected: ~67 files listed. We'll re-run this after the sweep and diff against an acceptable allow-list.

---

## Folder & file renames (Task 1)

### Task 1: Rename `preply/` and the two preply-named files

**Files:**
- Move: `preply/` → `tutor/`
- Move: `progress/preply-lesson-log.md` → `progress/tutor-lesson-log.md`
- Move: `output-practice/preply-prep-templates.md` → `output-practice/tutor-prep-templates.md`

- [ ] **Step 1: Rename the directory**

Run: `git mv preply tutor`
Expected: `tutor/01-copula-companion.md` exists; `preply/` is gone.

- [ ] **Step 2: Rename the two files**

Run:
```bash
git mv progress/preply-lesson-log.md progress/tutor-lesson-log.md
git mv output-practice/preply-prep-templates.md output-practice/tutor-prep-templates.md
```
Expected: New paths exist; old paths gone.

- [ ] **Step 3: Find and fix any markdown links that referenced old paths**

Run: `grep -rn "preply/\|preply-lesson-log\|preply-prep-templates" --include="*.md" --include="*.html" --include="*.json" .`
For every hit (other than inside `docs/superpowers/`):
- If it's a `[link text](preply/foo.md)` or `preply/foo.md` path reference, edit the file to use the new `tutor/` / `tutor-lesson-log` / `tutor-prep-templates` path.
- If it's prose like "see `preply/01-copula-companion.md`", update to `tutor/01-copula-companion.md`.

- [ ] **Step 4: Confirm path references are fixed**

Run: `grep -rn "preply/\|preply-lesson-log\|preply-prep-templates" --include="*.md" --include="*.html" --include="*.json" . | grep -v "^./docs/superpowers/"`
Expected: No hits.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "Rename preply/ to tutor/; rename preply-* files to tutor-*"
```

---

## Root meta files (Tasks 2–6)

### Task 2: Rewrite `README.md` in generic voice

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the TODO-style README with a real one in generic voice**

Open `README.md`. Keep the frontmatter. Replace the body with content along these lines (engineer should adapt wording but keep meaning):

```markdown
# Japanese Conversational-Mastery Curriculum

## What this repo is

A 13-module Japanese curriculum aimed at conversational mastery (not JLPT certification). Three opinionated departures from textbook orthodoxy: polite-first / plain-form-fast, comprehensible input from Day 1, and pitch accent taught from Module 00.

Content lives in Markdown; vocabulary in CSV/JSON; kanji in JSON. Two Python helpers (under `tools/`) regenerate the Anki deck and the interactive kana guide. Designed so Claude Code can extend it deterministically — see `CLAUDE.md`.

## Who it is for

Any adult learner who wants conversational Japanese. The pronunciation track includes optional L1-specific transfer notes (currently Hungarian and German/Swiss-German) as examples — forkers are encouraged to add their own L1 file alongside.

## How to use this repo

1. Open `INDEX.md` to see module status.
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
- Optional: Migaku (`tools/migaku-setup.md`)

See `tools/` for setup guides for each.
```

- [ ] **Step 2: Verify no personal references remain**

Run: `grep -i "roland\|rolivischi\|hungarian\|swiss\|preply" README.md`
Expected: No hits (or only acceptable ones inside file paths you reference).

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "Rewrite README in generic voice"
```

### Task 3: Rewrite `INDEX.md` (preserve the module status table)

**Files:**
- Modify: `INDEX.md`

- [ ] **Step 1: Edit the "Notes" section and the intro**

Open `INDEX.md`. The module status table (lines 17-31) is already generic — keep it. Replace the leading TODOs and the trailing Notes TODO with real generic content. Example:

```markdown
## Module Status Table

A linear view of the curriculum. Update the `Status` column as modules move from `locked` → `active` → `done`.

[keep the existing table verbatim]

## Notes

- To unlock the next module: complete its exercises, run a tutor session covering its grammar, and update the row above.
- To request Claude Code to build the next module's content, ask: "build Module N+1's drills and dialogues from its overview." See `CLAUDE.md` for the authoring contract.
- Cumulative vocab/kanji counts are estimates; the source of truth is `vocab/tier-*.csv` and `kanji/kanji-master.json`.
```

- [ ] **Step 2: Sweep for personal references**

Run: `grep -i "roland\|hungarian\|swiss\|preply" INDEX.md`
Expected: No hits.

- [ ] **Step 3: Commit**

```bash
git add INDEX.md
git commit -m "Rewrite INDEX.md intro and notes in generic voice"
```

### Task 4: Generalize `INSTRUCTIONS.md`

**Files:**
- Modify: `INSTRUCTIONS.md`

- [ ] **Step 1: Identify Roland-specific passages**

Run: `grep -n "Roland\|Hungarian\|Swiss German\|Preply" INSTRUCTIONS.md`
Read each hit in context (Read tool, with offset/limit if needed).

- [ ] **Step 2: Rewrite §1 (learner profile) in abstract terms**

Replace any "Roland is a 38-year-old Swiss engineer with Hungarian L1" prose with abstract phrasing like "the learner is an adult focused on conversational competence". The §1.3 (phonological background) section should be rewritten to: "L1 transfer is real and should be addressed. This curriculum ships with Hungarian and German/Swiss-German examples under `pronunciation/`; forkers with other L1s should add their own file using the same structure."

- [ ] **Step 3: Sweep the rest of the document**

For every other hit from Step 1, replace:
- "Roland" → "the learner"
- "Roland's L1" → "the learner's L1"
- "Preply tutor" / "Preply session" → "1-on-1 tutor session" / "tutor"

Keep the curriculum blueprint (module outlines in §3.5) intact — it describes content, not the learner.

- [ ] **Step 4: Verify**

Run: `grep -i "roland\|preply" INSTRUCTIONS.md`
Expected: No hits.
Run: `grep -i "hungarian\|swiss german" INSTRUCTIONS.md`
Expected: Only hits where the prose references the L1-specific pronunciation files by name (e.g. "see `pronunciation/07-hungarian-transfer-notes.md`"). Acceptable.

- [ ] **Step 5: Commit**

```bash
git add INSTRUCTIONS.md
git commit -m "Generalize INSTRUCTIONS.md learner profile and remove Preply branding"
```

### Task 5: Generalize `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Locate and rewrite the personal references**

Open `CLAUDE.md`. The following passages need editing:

- Line ~9: `A personal Japanese-language curriculum for one learner ("Roland") aimed at **conversational mastery**` → `A Japanese-language curriculum aimed at **conversational mastery**`
- Line ~9: `so Claude Code can extend it deterministically as the learner progresses.` (keep — already generic)
- Any "Module 01 at last update" — preserve as-is; reflects current state.
- The architecture/pedagogy section's `The learner's Hungarian L1 / German (Swiss German) L2 background drives specific pronunciation content — see INSTRUCTIONS.md §1.3.` → `The pronunciation track ships with L1-specific transfer notes for Hungarian and German/Swiss-German speakers as examples (see pronunciation/07-, pronunciation/08-). Forkers with other L1s should add their own file alongside.`
- The "preply/" mention in the folder layout → "tutor/"
- Reference `01-copula-companion.md` lives under `tutor/`, not `preply/`.

- [ ] **Step 2: Verify**

Run: `grep -i "roland\|preply" CLAUDE.md`
Expected: No hits.
Run: `grep -i "hungarian\|swiss german" CLAUDE.md`
Expected: Only the pronunciation-track callout you wrote in Step 1.

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "Generalize CLAUDE.md learner framing and tutor folder path"
```

### Task 6: Generalize `ROADMAP.md`

**Files:**
- Modify: `ROADMAP.md`

- [ ] **Step 1: Read and rewrite**

Open `ROADMAP.md`. Replace any "Roland's milestones" / "Roland's trip to Japan" / "Preply session count" prose with curriculum-level milestones (which modules to reach by which week of study). Keep the structure if useful; replace personal goals with generic completion markers.

- [ ] **Step 2: Verify**

Run: `grep -i "roland\|preply\|hungarian\|swiss" ROADMAP.md`
Expected: No hits.

- [ ] **Step 3: Commit**

```bash
git add ROADMAP.md
git commit -m "Generalize ROADMAP.md milestones"
```

---

## Pedagogy files (Task 7)

### Task 7: Sweep `pedagogy/*.md`

**Files:**
- Modify: `pedagogy/00-philosophy.md`
- Modify: `pedagogy/01-polite-vs-plain-strategy.md`
- Modify: `pedagogy/02-input-vs-output-balance.md`
- Modify: `pedagogy/03-srs-strategy.md`
- Modify: `pedagogy/05-self-talk-protocol.md`
- Modify: `pedagogy/06-ai-conversation-prompts.md`

- [ ] **Step 1: Identify hits per file**

Run: `grep -n "Roland\|Hungarian\|Swiss German\|Preply" pedagogy/*.md`
Note: `pedagogy/04-*` (if it exists) is also in scope; the grep will find it.

- [ ] **Step 2: For each file, edit the hits**

For every match:
- "Roland" → "the learner" / "you" (pick whichever fits the surrounding sentence; "you" reads better in instructional prose, "the learner" in descriptive prose)
- "Roland's L1 is Hungarian" / similar → drop the specific L1 and reference "your L1" + "see pronunciation/ for L1-specific transfer notes"
- "Roland's Preply tutor" → "your tutor"
- "Preply session" / "Preply lesson" → "tutor session" / "1-on-1 lesson"

Preserve the pedagogical content (the "why" behind each strategy) unchanged.

- [ ] **Step 3: Verify**

Run: `grep -i "roland\|preply" pedagogy/`
Expected: No hits.
Run: `grep -i "hungarian\|swiss german" pedagogy/`
Expected: No hits (or only the pronunciation-track cross-reference). All concrete L1 assumptions belong under `pronunciation/`, not `pedagogy/`.

- [ ] **Step 4: Commit**

```bash
git add pedagogy/
git commit -m "Generalize pedagogy files: remove personal asides and Preply branding"
```

---

## Pronunciation files (Tasks 8–10)

### Task 8: Rewrite `pronunciation/00-overview.md`

**Files:**
- Modify: `pronunciation/00-overview.md`

- [ ] **Step 1: Edit the file**

Read the current file first. Replace any "Roland's L1 is Hungarian" / "Roland's L2 is Swiss German" prose with a generic intro. Add (or update) a section that reads roughly:

```markdown
## L1 transfer notes

Your first language shapes the mistakes you'll make in Japanese. This track ships with two example L1-transfer files:

- `07-hungarian-transfer-notes.md` — for Hungarian L1 speakers
- `08-german-swiss-transfer-notes.md` — for German / Swiss-German speakers

If your L1 isn't covered, treat these as examples: create your own `09-<your-L1>-transfer-notes.md` alongside them using the same structure (vowel inventory, consonant traps, prosody/pitch contrasts).
```

- [ ] **Step 2: Verify**

Run: `grep -i "roland" pronunciation/00-overview.md`
Expected: No hits.

- [ ] **Step 3: Commit**

```bash
git add pronunciation/00-overview.md
git commit -m "Rewrite pronunciation overview: L1 notes as optional examples"
```

### Task 9: Add banners to `07-hungarian-` and `08-german-swiss-` files

**Files:**
- Modify: `pronunciation/07-hungarian-transfer-notes.md`
- Modify: `pronunciation/08-german-swiss-transfer-notes.md`

- [ ] **Step 1: Insert the banner at the top of `07-`**

After the frontmatter, before the first `#` heading, insert:

```markdown
> **Audience:** This file is for learners whose L1 is Hungarian. Skip if it doesn't apply to you.
> **Forkers:** Add your own L1 file alongside (e.g. `09-spanish-transfer-notes.md`) using the same structure — vowel inventory, consonant traps, prosody/pitch contrasts.
```

- [ ] **Step 2: Insert the equivalent banner at the top of `08-`**

After the frontmatter, before the first `#` heading, insert:

```markdown
> **Audience:** This file is for learners whose L1 (or strong L2) is German or Swiss German. Skip if it doesn't apply to you.
> **Forkers:** Add your own L1 file alongside (e.g. `09-spanish-transfer-notes.md`) using the same structure — vowel inventory, consonant traps, prosody/pitch contrasts.
```

- [ ] **Step 3: Verify**

Run: `head -15 pronunciation/07-hungarian-transfer-notes.md pronunciation/08-german-swiss-transfer-notes.md`
Expected: Both files show the banner immediately after the frontmatter.

- [ ] **Step 4: Commit**

```bash
git add pronunciation/07-hungarian-transfer-notes.md pronunciation/08-german-swiss-transfer-notes.md
git commit -m "Add audience banners to L1-specific pronunciation files"
```

### Task 10: Sweep `pronunciation/01-` through `06-` for stray L1 asides

**Files:**
- Modify: `pronunciation/01-mora-and-timing.md`
- Modify: `pronunciation/02-the-five-vowels.md`
- Modify: `pronunciation/03-tricky-consonants.md`
- Modify: `pronunciation/04-long-vowels-and-sokuon.md`
- Modify: `pronunciation/05-pitch-accent-intro.md`
- Modify: `pronunciation/06-pitch-accent-four-patterns.md`

- [ ] **Step 1: Identify hits**

Run: `grep -n "Roland\|Hungarian\|Swiss German\|swiss german\|hungarian" pronunciation/0[1-6]-*.md`

- [ ] **Step 2: For each hit**

- "Roland" → "you"
- "(Hungarian habit)" / "Hungarian speakers tend to…" → "Your L1 may push you toward X — if your L1 is Hungarian/German, see `07-` / `08-`."
- Pithy "Hungarian 'c' transfers well" type asides → keep ONLY if the sentence is teaching a phoneme equivalence as an aid for learners with that L1; otherwise generalize or remove.

Use judgment: short L1 asides that *help* a learner with that L1 are fine if the surrounding text is generic; long passages assuming an L1 should be moved to `07-` or `08-` or rewritten.

- [ ] **Step 3: Verify**

Run: `grep -i "roland" pronunciation/0[1-6]-*.md`
Expected: No hits.

- [ ] **Step 4: Commit**

```bash
git add pronunciation/
git commit -m "Generalize pronunciation files 01-06; preserve L1-specific notes in 07/08"
```

---

## Tools, listening, output-practice, grammar-reference, kanji (Task 11)

### Task 11: Sweep all reference & guide files

**Files:**
- Modify: `tools/anki-setup.md`
- Modify: `tools/migaku-setup.md`
- Modify: `tools/yomitan-setup.md`
- Modify: `tools/kotu-and-dogen.md`
- Modify: `tools/build_kana_guide.py`
- Modify: `listening/podcast-rotation.md`
- Modify: `listening/resources-by-level.md`
- Modify: `output-practice/dialogue-bank.md`
- Modify: `output-practice/ai-conversation-prompts.md`
- Modify: `output-practice/tutor-prep-templates.md` (renamed in Task 1)
- Modify: `grammar-reference/glossary.md`
- Modify: `grammar-reference/common-mistakes.md`
- Modify: `kanji/policy.md`
- Modify: `kanji/order.md`
- Modify: `kanji/README.md`
- Modify: `kanji/mnemonics/mnemonic-template.md`
- Modify: `vocab/anki-export/core-300.apkg.notes.md`

- [ ] **Step 1: Identify all hits across these directories**

Run:
```bash
grep -rn "Roland\|Hungarian\|hungarian\|Swiss German\|swiss german\|Preply\|preply" \
  tools/ listening/ output-practice/ grammar-reference/ kanji/ vocab/anki-export/
```

- [ ] **Step 2: For each file, apply the substitutions**

- "Roland" → "you" / "the learner"
- "Roland's setup" / "Roland uses X" → drop the personal frame; just describe the recommended setup
- "Preply" / "Preply tutor" → "tutor" / "1-on-1 tutor"
- "Hungarian" / "Swiss German" in passing asides → "your L1" + cross-link to `pronunciation/07-` or `08-` if appropriate

For `tools/build_kana_guide.py`: the grep found a hit in this file. Treat any "Roland" in a comment or string as a stray; replace with "the learner" or remove.

- [ ] **Step 3: Verify**

Run:
```bash
grep -rn "Roland\|Preply" tools/ listening/ output-practice/ grammar-reference/ kanji/ vocab/anki-export/
```
Expected: No hits.

- [ ] **Step 4: Commit**

```bash
git add tools/ listening/ output-practice/ grammar-reference/ kanji/ vocab/anki-export/
git commit -m "Generalize tooling guides, listening/output/grammar/kanji reference"
```

---

## Module 00 sweep (Task 12)

### Task 12: Module 00 — sweep for stray personal references

**Files:**
- Modify: `modules/00-writing-systems/00-overview.md`
- Modify: `modules/00-writing-systems/01-hiragana-vowels-and-rows.md`
- Modify: `modules/00-writing-systems/02-hiragana-dakuten-and-yoon.md`
- Modify: `modules/00-writing-systems/03-katakana.md`
- Modify: `modules/00-writing-systems/04-katakana-loanword-traps.md`
- Modify: `modules/00-writing-systems/dialogues.md`
- Modify: `modules/00-writing-systems/module-vocab.json`

- [ ] **Step 1: Identify hits**

Run: `grep -n "Roland\|Hungarian\|hungarian\|Preply\|preply" modules/00-writing-systems/`

- [ ] **Step 2: Apply substitutions**

Same rules as Task 11. For any katakana loanword example using "Roland" / "ローラント", swap to "Alex" / "アレックス".

- [ ] **Step 3: Verify**

Run: `grep -in "roland\|preply" modules/00-writing-systems/`
Expected: No hits.

- [ ] **Step 4: Run validate.py**

Run: `uv run python tools/validate.py`
Expected: Exits 0.

- [ ] **Step 5: Commit**

```bash
git add modules/00-writing-systems/
git commit -m "Generalize Module 00 content (writing systems)"
```

---

## Module 01 — Roland → Alex (Tasks 13–17)

### Task 13: Module 01 dialogues — Roland → Alex

**Files:**
- Modify: `modules/01-copula-basics/dialogues.md`

- [ ] **Step 1: Replace every "Roland" with "Alex"; "ローラント" with "アレックス"**

Open `modules/01-copula-basics/dialogues.md`. Apply find-and-replace (Edit tool with `replace_all: true`):
- `Roland` → `Alex`
- `ローラント` → `アレックス`

Verify the dialogue still reads naturally after each substitution. The character is Swiss, talking to Mika at a meetup; no nationality-coupled lines need editing.

- [ ] **Step 2: Check pitch-accent / mora-count notes**

ローラント = 5 morae (ro-o-ra-n-to). アレックス = 5 morae (a-re-k-ku-su). If the file contains any pitch-accent annotation for the name specifically, leave a brief note: `アレックス pitch pattern: verify on OJAD if drilling this specifically.`

- [ ] **Step 3: Verify**

Run: `grep -n "Roland\|ローラント" modules/01-copula-basics/dialogues.md`
Expected: No hits.

- [ ] **Step 4: Commit**

```bash
git add modules/01-copula-basics/dialogues.md
git commit -m "Module 01: rename dialogue character Roland → Alex (ローラント → アレックス)"
```

### Task 14: Module 01 prose files (grammar 01–06, overview, exercises, self-talk)

**Files:**
- Modify: `modules/01-copula-basics/00-overview.md`
- Modify: `modules/01-copula-basics/01-desu-copula.md`
- Modify: `modules/01-copula-basics/02-wa-topic-particle.md`
- Modify: `modules/01-copula-basics/03-negative-dewa-arimasen.md`
- Modify: `modules/01-copula-basics/04-questions-ka.md`
- Modify: `modules/01-copula-basics/05-no-possession.md`
- Modify: `modules/01-copula-basics/06-kosoado-preview.md`
- Modify: `modules/01-copula-basics/exercises.md`
- Modify: `modules/01-copula-basics/self-talk.md`

- [ ] **Step 1: Identify hits**

Run: `grep -n "Roland\|ローラント\|Hungarian\|hungarian\|Swiss German" modules/01-copula-basics/0*.md modules/01-copula-basics/exercises.md modules/01-copula-basics/self-talk.md`

- [ ] **Step 2: Apply substitutions per file**

For each hit:
- Example sentences with "I am Roland" / "My name is Roland" → "I am Alex" / "My name is Alex"
- `ローラント` → `アレックス` (in any kana example)
- Pronunciation asides like "in Hungarian, X happens" → "your L1 may push you toward X (see `pronunciation/07-` if Hungarian)"
- `02-wa-topic-particle.md:105` cross-link to `pronunciation/07-hungarian-transfer-notes.md` — keep as a "see also" link but rephrase the surrounding prose so it's not assuming the reader is Hungarian.
- `01-desu-copula.md:115` "not the rounded Hungarian/German /u/" → "not the rounded /u/ found in many European languages"

- [ ] **Step 3: Verify**

Run: `grep -in "roland\|ローラント" modules/01-copula-basics/0*.md modules/01-copula-basics/exercises.md modules/01-copula-basics/self-talk.md`
Expected: No hits.

Run: `grep -in "hungarian\|swiss german" modules/01-copula-basics/0*.md modules/01-copula-basics/exercises.md modules/01-copula-basics/self-talk.md`
Expected: Only hits where the text says "see pronunciation/07-..." or "see pronunciation/08-...". No standalone L1 assumptions.

- [ ] **Step 4: Commit**

```bash
git add modules/01-copula-basics/
git commit -m "Module 01: generalize grammar prose, exercises, self-talk"
```

### Task 15: Module 01 vocab JSON — Roland → Alex

**Files:**
- Modify: `modules/01-copula-basics/module-vocab.json`

- [ ] **Step 1: Identify hits**

Run: `grep -n "Roland\|ローラント\|Hungarian\|hungarian" modules/01-copula-basics/module-vocab.json`

- [ ] **Step 2: Apply substitutions**

For each hit:
- `Roland` → `Alex` in English glosses and notes
- `ローラント` → `アレックス` in `kana` fields
- `Roland's home country` → `Alex's home country (Switzerland, in this curriculum's example dialogues)`
- `Roland's L1 country` → `Hungary — used as an example L1 country in this curriculum; see pronunciation/07-`
- `Useful for Roland (developer)` → `Useful for technical learners` (or simply drop the parenthetical)
- For the note on つ: `つ is [tsɯ] — Hungarian 'c' transfers well.` → `つ is [tsɯ]. (Hungarian L1 speakers: 'c' transfers well — see pronunciation/07-)`. The rule: any L1-specific aside in vocab notes gets reframed so the *default reader* isn't assumed to have that L1, but the helpful tip is preserved for those who do, with a cross-link to the relevant pronunciation file.

- [ ] **Step 3: Verify JSON is still valid**

Run: `uv run python -c "import json; json.load(open('modules/01-copula-basics/module-vocab.json'))" && echo OK`
Expected: `OK`.

- [ ] **Step 4: Verify substitutions**

Run: `grep -n "Roland\|ローラント" modules/01-copula-basics/module-vocab.json`
Expected: No hits.

- [ ] **Step 5: Run validate.py**

Run: `uv run python tools/validate.py`
Expected: Exits 0.

- [ ] **Step 6: Commit**

```bash
git add modules/01-copula-basics/module-vocab.json
git commit -m "Module 01 vocab: Roland → Alex; generalize L1-specific notes"
```

### Task 16: `tutor/01-copula-companion.md` (formerly `preply/`)

**Files:**
- Modify: `tutor/01-copula-companion.md`

- [ ] **Step 1: Identify hits**

Run: `grep -n "Roland\|Hungarian\|hungarian\|Preply\|preply\|ローラント" tutor/01-copula-companion.md`

- [ ] **Step 2: Apply substitutions**

- "Roland" → "the learner" / "your tutee" (depending on whether the worksheet addresses the tutor or the learner)
- "Preply tutor" → "tutor"
- Any "Roland's Hungarian L1" asides → "your tutee's L1" or drop entirely

- [ ] **Step 3: Verify**

Run: `grep -i "roland\|preply\|ローラント" tutor/01-copula-companion.md`
Expected: No hits.

- [ ] **Step 4: Commit**

```bash
git add tutor/01-copula-companion.md
git commit -m "Generalize tutor companion worksheet for any tutor session"
```

### Task 17: Module overviews M02–M12

**Files:**
- Modify: `modules/02-existence-and-location/00-overview.md`
- Modify: `modules/03-adjectives/00-overview.md`
- Modify: `modules/04-verbs-present-polite/00-overview.md`
- Modify: `modules/06-past-and-plain-forms/00-overview.md`
- Modify: `modules/11-keigo-conversational/00-overview.md`
- Modify: `modules/12-advanced-conversation/00-overview.md`

(M05, M07, M08, M09, M10 overviews did not appear in the baseline grep, so likely already clean — re-check in Step 1.)

- [ ] **Step 1: Identify hits in all M02–M12 overview files**

Run: `grep -rn "Roland\|Hungarian\|hungarian\|Swiss German\|Preply\|preply\|ローラント" modules/0[2-9]-*/00-overview.md modules/1[0-2]-*/00-overview.md`

- [ ] **Step 2: Apply substitutions per file**

Same rules as previous tasks. Module overviews tend to have short Roland-personalized "by this point Roland should be able to X" prose — replace with "by this point the learner should be able to X" or "you will be able to X".

- [ ] **Step 3: Verify**

Run: `grep -in "roland\|preply" modules/`
Expected: No hits anywhere under `modules/`.

- [ ] **Step 4: Commit**

```bash
git add modules/
git commit -m "Generalize M02–M12 module overviews"
```

---

## Progress data sanitization (Task 18)

### Task 18: Reset progress logs to template form

**Files:**
- Modify: `progress/progress.md`
- Modify: `progress/tutor-lesson-log.md` (renamed in Task 1)
- Modify: `progress/weekly-checkin-template.md`

- [ ] **Step 1: Read each file and identify which content is logged data vs. template**

Open all three. Anything that looks like actual logged content ("Week 3: completed M01 §2, struggled with は vs が") is Roland's private data and should go. The template structure (headings, empty bullet points, example formats) stays.

- [ ] **Step 2: For `progress/progress.md`** 

Replace the body with an empty template along these lines (keep the frontmatter):

```markdown
# Study Progress Log

## Current state

- Active module: M00 (see `INDEX.md`)
- Cumulative vocab: 0
- Cumulative kanji: 0

## Weekly logs

<!-- Add a new section per week. See progress/weekly-checkin-template.md for the structure. -->
```

- [ ] **Step 3: For `progress/tutor-lesson-log.md`** 

Reset to a header + empty template:

```markdown
# Tutor Lesson Log

<!-- One entry per session. Date / module(s) covered / what worked / what to bring back next time. -->

## Template

### YYYY-MM-DD — Lesson N (Module MM)

**Covered:** 

**What clicked:** 

**What didn't:** 

**Homework / bring back:** 
```

- [ ] **Step 4: For `progress/weekly-checkin-template.md`** 

It's already a template. Just sweep for any "Roland"/"Preply" hits and generalize ("Preply session this week" → "tutor session this week", etc.).

- [ ] **Step 5: Verify**

Run: `grep -i "roland\|preply" progress/`
Expected: No hits.

- [ ] **Step 6: Commit**

```bash
git add progress/
git commit -m "Reset progress logs to empty templates; generalize weekly check-in"
```

---

## Final verification (Task 19)

### Task 19: End-to-end verification before push

**Files:** None modified.

- [ ] **Step 1: Re-run the full repository grep**

Run:
```bash
grep -rln "Roland\|rolivischi\|Hungarian\|hungarian\|Swiss German\|swiss german\|Preply\|preply" \
  --include="*.md" --include="*.html" --include="*.json" --include="*.py" \
  --exclude-dir=docs --exclude-dir=node_modules . | sort > /tmp/jp-after-hits.txt
diff /tmp/jp-baseline-hits.txt /tmp/jp-after-hits.txt
cat /tmp/jp-after-hits.txt
```

Expected remaining files (the allow-list):
- `pronunciation/07-hungarian-transfer-notes.md` — deliberately kept; banner added
- `pronunciation/08-german-swiss-transfer-notes.md` — deliberately kept; banner added
- `pronunciation/00-overview.md` — references the above by filename
- Any file containing a cross-link prose like "see pronunciation/07-..." — acceptable

Anything else in the after-hits file must be fixed. If a file appears in the after-hits list that isn't on the allow-list above, return to its task and re-edit.

- [ ] **Step 2: Confirm no `rolivischi` reference (the username)**

Run: `grep -rn "rolivischi" --exclude-dir=docs --exclude-dir=.git --exclude-dir=node_modules .`
Expected: Only the footer link in `public/index.html` and `scripts/landing.html` (`github.com/rolivischi2/japanese-tutor`) — that's the source link, kept by design.

- [ ] **Step 3: Confirm no broken markdown links to `preply/` paths**

Run: `grep -rn "preply" --include="*.md" --include="*.html" --include="*.json" --exclude-dir=docs .`
Expected: No hits.

- [ ] **Step 4: Run validate.py**

Run: `uv run python tools/validate.py`
Expected: Exits 0 with success message.

- [ ] **Step 5: Confirm `git status` is clean and all commits are in**

Run: `git status && git log --oneline -20`
Expected: Working tree clean. Log shows the series of generalization commits on top of `acc2c43` (the prior tip).

- [ ] **Step 6: Push to `main`**

Run: `git push origin main`
Expected: Push succeeds; Vercel will auto-deploy. The deployed kana tools site (`japan-learning-omega.vercel.app`) is unaffected by these content changes — confirm in a browser after the deploy finishes.

---

## Notes on style

- Prefer "you" over "the learner" in instructional prose (more direct, more natural). Use "the learner" only when the third person reads better (e.g. abstract design discussion in pedagogy files).
- When removing a personal aside ("Roland struggles with X"), check whether the underlying pedagogical point is still made by surrounding text. If not, rephrase the point in generic terms — don't just delete.
- Keep all cross-links between files. If you rename a path (e.g. `preply/` → `tutor/`), grep all `.md` files for the old path and fix references (Task 1 Step 3 covers this).
- Commit messages: factual and short. Examples above are fine; no need for a long body.
