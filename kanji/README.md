---
module: meta
file: kanji-readme
lang_focus: meta
kanji_level: 0
last_updated: 2026-05-22
---

# Kanji

## Overview

TODO: Describe the kanji learning approach in 2–3 sentences. Recognition-only, no production. Kanji introduced only when the corresponding vocab is already known from audio/kana. Cross-reference `kanji/policy.md` for the full rationale.

## Targets

TODO: State the kanji targets:
- ~30 kanji by end of Module 04
- ~400 kanji by end of Module 08
- ~800 kanji by end of Module 12
(Compare: Genki I+II = ~317 per japanesecomplete.com)

## File Index

TODO: Describe each file:
- `policy.md`: the non-negotiable kanji learning policy
- `order.md`: justification for frequency-driven introduction order
- `kanji-by-module.csv`: denormalised flat list sorted by introduction order (generated from kanji-master.json — never hand-edit)
- `kanji-master.json`: the authoritative kanji data array
- `mnemonics/mnemonic-template.md`: guidance for writing custom mnemonics

## Workflow

TODO: Explain the workflow for adding new kanji:
1. Identify a vocab word Roland already knows in audio/kana form
2. Add entry to `kanji-master.json`
3. Run `python tools/validate.py` to check consistency
4. `kanji-by-module.csv` is regenerated from `kanji-master.json` automatically — never edit manually
