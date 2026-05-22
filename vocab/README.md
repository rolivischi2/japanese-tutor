---
module: meta
file: vocab-readme
lang_focus: vocab
kanji_level: 0
last_updated: 2026-05-22
---

# Vocabulary

## Overview

TODO: Describe the three-tier vocabulary system and how it maps to the curriculum:
- Tier 1 (core-300): highest-priority conversational words; targeted at Module 00–03 period; sourced from JLPT N5 + Kaishi 1.5k first 300 + BCCWJ spoken corpus
- Tier 2 (expand-700): JLPT N4-ish + remaining Kaishi 1.5k + topical buckets; Module 04–07
- Tier 3 (fluency-1500): Tango N3 + BCCWJ top 3500; brings total to ~2500 (conversational-fluency floor)

## CSV Schema

TODO: Document the CSV column headers. Derive from `vocab/schema.json`:
`id, kana, kanji, reading, pos, transitivity, english, pitch_pattern, drop_after_mora, module_introduced, tier, frequency_rank_bccwj, notes, tags`

## Anki Integration

TODO: Explain the workflow: CSVs → `tools/export_to_anki.py` → `.apkg` files in `vocab/anki-export/`. Card format: front = kana (with audio), back = kanji form + English + pitch accent graph + example sentence + module tag.

## Special Files

TODO: Describe the specialised CSVs:
- `greetings-and-fixed-phrases.csv`: ~46 fixed expressions used from Day 1
- `numbers-and-counters.csv`: numbers + the 10 core counters from M04
- `time-expressions.csv`: days, months, time words, frequency adverbs
- `pitch-accent-overlay.csv`: pitch pattern data for every Tier 1+2 word (sourced from NHK Accent Dictionary / Kanjium database)
