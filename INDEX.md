---
module: meta
file: index
lang_focus: meta
kanji_level: 0
last_updated: 2026-05-23
---

# Curriculum Index

## Module Status Table

A linear view of the curriculum. Update the `Status` column as modules move from `locked` → `active` → `done`.

| Module | Status | Est. weeks | Key grammar | Vocab (cum.) | Kanji (cum.) | Milestone |
|--------|--------|------------|-------------|-------------|-------------|-----------|
| M00 — Writing Systems | done | 2 | Hiragana, katakana | 0 | 0 | M1: kana sight-reading |
| M01 — Copula Basics | active | 3 | です、じゃない、は、か、の | ~80 | 0 | M2: 60-second self-intro |
| M02 — Existence & Location | locked | 3 | あります、います、に vs で、こそあど | ~160 | 0 | M3: describe a room |
| M03 — Adjectives | locked | 3 | い-adj、な-adj、comparatives | ~240 | 0 | M3: describe people |
| M04 — Verbs (present polite) | locked | 4 | ます-form, verb groups, first kanji | ~360 | ~30 | M4: daily schedule |
| M05 — Te-form | locked | 4–6 | て-form, 11 uses | ~510 | ~55 | M5: instructions, progressive |
| M06 — Past & Plain Forms | locked | 4 | plain non-past/past/negative | ~660 | ~85 | M6: narrate yesterday |
| M07 — Casual & Sentence Particles | locked | 3 | ね、よ、な、かな、contractions | ~780 | ~115 | M7: 5-min casual conversation |
| M08 — Potential / Volitional / Conditional | locked | 4 | potential, volitional, たら/ば/なら/と | ~930 | ~145 | M8: express hypotheticals |
| M09 — Giving / Receiving | locked | 3 | あげる、くれる、もらう、uchi/soto | ~1010 | ~165 | M9: describe favours |
| M10 — Passive / Causative | locked | 3 | passive, causative, causative-passive | ~1110 | ~190 | M10: news headlines |
| M11 — Conversational Keigo | locked | 3 | 尊敬語、謙譲語、shop phrases | ~1230 | ~215 | M11: survive Japan trip |
| M12 — Advanced Conversation | locked | open | aizuchi, slang, hedging, onomatopoeia | ~1500+ | ~400+ | M12: 10-min free conversation |

## Notes

- To unlock the next module: complete its exercises, run a tutor session covering its grammar, and update the `Status` column above.
- To request Claude Code to build the next module's content, ask: "build Module N+1's drills and dialogues from its overview." See `CLAUDE.md` for the authoring contract.
- Cumulative vocab/kanji counts are estimates; the source of truth is `vocab/tier-*.csv` and `kanji/kanji-master.json`.
- Progress is logged in `progress/progress.md`; tutor sessions in `progress/tutor-lesson-log.md`.
