---
title: Generalize the curriculum for any learner
date: 2026-05-23
status: approved
---

# Generalize the curriculum for any learner

## Goal

Strip the "Roland's personal curriculum" framing from the repository so anyone can fork and use it as a generic Japanese conversational-mastery curriculum. Preserve the existing pedagogical work — including the L1-specific pronunciation transfer notes — by clearly labeling persona-coupled material as optional reference rather than core requirement.

## Non-goals

- Authoring new module content for M02–M12 (they remain scaffolded as-is).
- Refactoring pedagogy decisions (polite-first/plain-fast, te-form module, kanji policy, etc.).
- Building any templating or `learner-profile.yaml` system — too much engineering for a content repo.
- Touching the deployed kana tools site (`public/index.html`, kana guide, chart) — already generic.
- Renaming the GitHub repo or the existing `github.com/rolivischi2/japanese-tutor` source link in the footer.

## Decisions baked in

1. **Placeholder character: "Alex"** (gender-neutral, transliterates to アレックス) replaces "Roland" / ローラント wherever the learner's name appears in M01 dialogues, exercises, and example sentences.
2. **L1-specific pronunciation files kept verbatim.** `pronunciation/07-hungarian-transfer-notes.md` and `pronunciation/08-german-swiss-transfer-notes.md` stay under their current filenames. Each gets a top-of-file banner: *"This file is for learners whose L1 is X. Skip if it doesn't apply. Forkers: add your own L1 file alongside (e.g. `09-spanish-transfer-notes.md`) following the same structure."* The presence of two examples becomes a feature — it shows the pattern.
3. **`preply/` → `tutor/`** (folder rename via `git mv`). All "Preply" mentions in prose become "your tutor" or "1-on-1 tutor session". The Preply-tutor *workflow* is preserved; only the platform-specific branding is removed.
4. **Progress data sanitised, templates preserved.** `progress/progress.md` is reset to an empty template (Roland's logged content removed). `progress/preply-lesson-log.md` → `progress/tutor-lesson-log.md`, also reset to template form. Same for `output-practice/preply-prep-templates.md` → `output-practice/tutor-prep-templates.md`.
5. **CLAUDE.md self-extension rules preserved.** The "self-extending" workflow keeps working — only the framing changes ("when the learner finishes module N" not "when Roland finishes module N"). The Hungarian/German L1 callouts in the pedagogy section are generalised to "the learner's L1 background drives the pronunciation track — see `pronunciation/` for L1-specific transfer notes."
6. **Nationality "Swiss" in M01 dialogues is kept.** Alex is Swiss — it's a dialogue choice, not learner-coupled, and it preserves the existing dialogue logic (Swiss + Hungarian camera → ハンガリー katakana vocab).

## Scope of changes

### Root meta files (full rewrite)
- `README.md` — generic project orientation; replace "Roland is X" → "the learner / you".
- `INDEX.md` — generic curriculum map; preserve the module status table.
- `INSTRUCTIONS.md` — keep the curriculum blueprint intact; rewrite §1 (learner profile) to describe an abstract conversational learner; remove Hungarian-L1/Swiss-German-L2 specifics from prose (they remain referenced from the pronunciation track as L1-specific examples).
- `CLAUDE.md` — update repository description, pedagogy section, and the "Extending the curriculum" workflow to use generic language.
- `ROADMAP.md` — generic timeline; remove personal milestones.

### Pedagogy (`pedagogy/*.md`)
- `00-philosophy.md`, `01-polite-vs-plain-strategy.md`, `02-input-vs-output-balance.md`, `03-srs-strategy.md`, `05-self-talk-protocol.md`, `06-ai-conversation-prompts.md` — remove every "Roland is X" / "Roland's tutor session" / "Roland's L1 is Hungarian" aside. Pedagogy reads as universal recommendations.

### Pronunciation (`pronunciation/*.md`)
- `00-overview.md` — generic intro; the "L1 transfer notes" section lists `07-` and `08-` as optional reference for learners with those L1s, and invites forkers to add their own.
- `01-` through `06-` — these are mostly language-universal; sweep for stray "Hungarian"/"German" asides and replace with "your L1" or remove.
- `07-hungarian-transfer-notes.md` — add banner, otherwise unchanged.
- `08-german-swiss-transfer-notes.md` — add banner, otherwise unchanged.

### Tools (`tools/*.md` and `tools/build_kana_guide.py`)
- `anki-setup.md`, `migaku-setup.md`, `yomitan-setup.md`, `kotu-and-dogen.md` — remove personal asides ("Roland uses X"), keep all setup instructions intact.
- `build_kana_guide.py` — sweep for any "Roland" in comments/strings (one occurrence per earlier grep); replace with neutral wording.

### Listening / Output / Grammar / Kanji reference
- `listening/podcast-rotation.md`, `listening/resources-by-level.md` — generic phrasing.
- `output-practice/dialogue-bank.md`, `output-practice/ai-conversation-prompts.md` — generic phrasing.
- `output-practice/preply-prep-templates.md` → rename → `tutor-prep-templates.md`; generic phrasing.
- `grammar-reference/glossary.md`, `grammar-reference/common-mistakes.md` — sweep.
- `kanji/policy.md`, `kanji/order.md`, `kanji/README.md`, `kanji/mnemonics/mnemonic-template.md`, `vocab/anki-export/core-300.apkg.notes.md` — sweep.

### Module content (M01 only — M00 is already mostly clean)
- `modules/00-writing-systems/*` — sweep for stray Roland/Hungarian references and clean.
- `modules/01-copula-basics/dialogues.md` — replace "Roland" → "Alex", "ローラント" → "アレックス" throughout. Adjust pitch-accent notes if the new katakana name changes mora count (アレックス = a-re-k-ku-su, 5 morae vs ローラント = ro-o-ra-n-to, 5 morae — same length; pitch pattern should be preserved or re-checked).
- `modules/01-copula-basics/01-desu-copula.md`, `02-wa-topic-particle.md`, `03-negative-dewa-arimasen.md`, `04-questions-ka.md`, `05-no-possession.md`, `06-kosoado-preview.md`, `exercises.md`, `self-talk.md`, `00-overview.md` — sweep; replace Roland with Alex in example sentences; replace "Hungarian habit" prose with generic "your L1 habit (see pronunciation/)".
- `modules/01-copula-basics/module-vocab.json` — replace "Roland" → "Alex"; the entry for ハンガリー with note "Roland's L1 country" → "L1 country example (Alex's L1, in this curriculum)"; "Useful for Roland (developer)" → "Useful for technical learners".
- `modules/02-` through `modules/12-` overview files — sweep for any Roland/Hungarian/Preply mentions.

### Folder rename
- `git mv preply tutor` — preserves history. The single existing file `01-copula-companion.md` gets a content sweep too.

### Progress data
- `progress/progress.md` — reset to template; Roland's logged content removed.
- `progress/preply-lesson-log.md` → `progress/tutor-lesson-log.md` (`git mv`), reset to template.
- `progress/weekly-checkin-template.md` — already a template; sweep for any Roland-specific phrasing.

## Workflow

1. Run a baseline `grep -ril "roland\|hungarian\|swiss german\|preply"` and save the full list (already have it).
2. Verify `tools/validate.py` does not reference the `preply/` path (it shouldn't — Preply files aren't part of the validated schema).
3. Folder renames first (`git mv`), so subsequent edits operate on the new paths.
4. Work top-down: root meta files → pedagogy → pronunciation → tools/listening/output → kanji → modules → progress.
5. After every batch of file edits, run `uv run python tools/validate.py` to confirm no schema or kanji-gating regressions.
6. Final sweep: re-run the baseline grep; every remaining hit must be (a) the deliberately-kept L1 transfer files, (b) the footer GitHub link, or (c) the docs/superpowers/ spec directory itself. Anything else gets fixed.
7. Commit in logical chunks (rename, root meta, content sweep) with descriptive messages.
8. Push to `main` (auto-deploys to Vercel — the deployed kana tools site is unaffected by these content changes).

## Verification

- `uv run python tools/validate.py` → exits 0.
- `grep -ri "Roland\|rolivischi" $(find . -type f -name "*.md" -not -path "./docs/*" -not -path "./node_modules/*")` → returns only the footer GitHub link.
- `grep -ri "Preply" $(find . -type f -name "*.md" -not -path "./docs/*")` → returns no hits.
- `grep -ri "Hungarian\|Swiss German" $(find . -type f -name "*.md" -not -path "./docs/*")` → returns only hits inside `pronunciation/07-hungarian-transfer-notes.md`, `pronunciation/08-german-swiss-transfer-notes.md`, and the `pronunciation/00-overview.md` index entry pointing at them.
- Spot-check M01 dialogue still reads naturally with "Alex" / "アレックス".
- Visit deployed `japan-learning-omega.vercel.app` after push and confirm the kana tools site still renders (no change expected; sanity check only).

## Risks

- **Subtle Roland/Hungarian references in prose** can be missed by grep if phrased indirectly ("the learner's mother tongue"). Mitigation: read every file that touches L1 transfer at least once during the sweep.
- **Renaming `preply/` could break a link** in a markdown file. Mitigation: after rename, grep for `preply/` paths in all `.md` and fix any link references.
- **アレックス vs ローラント pitch accent**: both are 5 morae but the natural pitch pattern may differ. Low risk — the pedagogical point is about pattern application, not the specific name. Will leave a brief note in the dialogue file if needed.
