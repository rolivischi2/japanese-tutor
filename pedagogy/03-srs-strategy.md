---
module: meta
file: 03-srs-strategy
lang_focus: meta
kanji_level: 0
last_updated: 2026-05-23
---

# SRS Strategy

## Anki Configuration Recipe

TODO: Document the exact Anki settings:
- New cards/day: 10 (M00–04), then 15 from M05 onward
- Max reviews/day: 200
- Scheduler: FSRS (default settings)
- Bury related cards: ON

## Deck Structure

TODO: Describe the three decks:
- `YourName::Core` — Kaishi 1.5k frequency deck + module-vocab CSVs
- `YourName::Mining` — Yomitan-added cards from immersion content
- `YourName::Kanji` — recognition-only; front = kanji + prompt "what does this mean?"; back = reading + English + example sentence + module tag

## Card Format

TODO: Describe the note type for each deck. For Core/Mining: front = kana (with audio), back = kanji form + English + pitch accent graph + example sentence + module tag. For Kanji: front = isolated kanji, back = primary meaning + on/kun readings + example vocab word.

## Suspension and Maintenance Rules

TODO: Document the rules:
- Suspend mined cards seen only once in 2 weeks of immersion — the word is not frequent enough yet.
- Bury related cards to avoid answer leakage.
- If mature-card retention drops below 85% for 2 weeks: halve new cards/day, do not advance modules.

## What SRS Is NOT For

TODO: Explicitly state: do not create grammar flashcards. Grammar is acquired through reading, listening, and targeted production drills — never through Anki cards explaining rules. Cross-reference `pedagogy/00-philosophy.md` Principle 3.
