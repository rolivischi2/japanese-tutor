---
module: meta
file: export-instructions
lang_focus: meta
kanji_level: 0
last_updated: 2026-05-22
---

# Anki Export Instructions

How to regenerate Anki decks from the CSV/JSON sources in this repository.

---

## Prerequisites

TODO: List prerequisites:
- Python 3.9+
- `genanki` Python package (`pip install genanki`)
- Anki desktop installed (for importing `.apkg` files)

## Script: tools/export_to_anki.py

TODO: Document the script (to be authored by Claude Code per INSTRUCTIONS.md §6 deliverable 5):
- Input: `vocab/tier-1-core-300.csv`, `vocab/tier-2-expand-700.csv`, `vocab/tier-3-fluency-1500.csv`, `kanji/kanji-master.json`
- Output: `vocab/anki-export/core-300.apkg`, `vocab/anki-export/expand-700.apkg`, `vocab/anki-export/fluency-1500.apkg`, `vocab/anki-export/kanji.apkg`

## Usage

TODO: Document commands once the script is authored:
```
python tools/export_to_anki.py --tier 1          # generates core-300.apkg
python tools/export_to_anki.py --tier 2          # generates expand-700.apkg
python tools/export_to_anki.py --tier 3          # generates fluency-1500.apkg
python tools/export_to_anki.py --kanji           # generates kanji.apkg
python tools/export_to_anki.py --all             # generates all four
```

## Card Template

TODO: Document the card note type format:
- Front: kana (with audio if available)
- Back: kanji form + English + pitch accent pattern (H/L notation) + example sentence (kana only if kanji not yet introduced) + module tag

## Import Instructions

TODO: Describe how to import into Anki:
1. Run the export script
2. Open Anki Desktop
3. File → Import → select `.apkg` file
4. Choose import mode: update existing notes by note ID
5. Verify card count after import

## Troubleshooting

TODO: Document common issues and fixes (e.g. duplicate note IDs, encoding issues with Japanese characters on some systems).
