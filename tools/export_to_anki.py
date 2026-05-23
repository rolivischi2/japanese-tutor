# /// script
# requires-python = ">=3.11"
# dependencies = ["genanki>=0.13"]
# ///
"""export_to_anki.py — Convert vocab tier CSVs and kanji CSV into Anki .apkg decks.

Reads:
  vocab/tier-1-core-300.csv       → tier-1.apkg
  vocab/tier-2-expand-700.csv     → tier-2.apkg
  vocab/tier-3-fluency-1500.csv   → tier-3.apkg
  kanji/kanji-by-module.csv       → kanji.apkg

Card format (vocab decks):
  Front  : kana form  (audio placeholder: TODO)
  Back   : kanji form (or kana if no kanji) + English glosses + pitch accent
           + first example sentence (if present) + module tag

Card format (kanji deck):
  Front  : kanji character + primary meaning prompt
  Back   : meaning_primary, on-yomi, kun-yomi, stroke count, example sentence

Output files are written to vocab/anki-export/ by default.

The `genanki` third-party library is required.  If it is not installed the
script prints a clear installation message and exits 0.

Usage:
  python3 tools/export_to_anki.py [--help] [--repo-root PATH] [--output-dir PATH]

Exit codes:
  0  Success (or genanki missing — install message printed)
  1  Unexpected error during export
"""

import argparse
import csv
import json
import os
import sys

# ---------------------------------------------------------------------------
# Dependency check — genanki
# ---------------------------------------------------------------------------

try:
    import genanki  # type: ignore
    GENANKI_AVAILABLE = True
except ImportError:
    GENANKI_AVAILABLE = False


# ---------------------------------------------------------------------------
# Stable model / deck IDs  (arbitrary large integers, must be consistent)
# ---------------------------------------------------------------------------
VOCAB_MODEL_ID   = 1_607_392_319
KANJI_MODEL_ID   = 1_607_392_320
TIER1_DECK_ID    = 2_059_400_100
TIER2_DECK_ID    = 2_059_400_101
TIER3_DECK_ID    = 2_059_400_102
KANJI_DECK_ID    = 2_059_400_103


# ---------------------------------------------------------------------------
# CSS shared by both note types
# ---------------------------------------------------------------------------
CARD_CSS = """\
.card {
  font-family: "Hiragino Sans", "Yu Gothic", sans-serif;
  font-size: 20px;
  text-align: center;
  color: #1a1a2e;
  background-color: #f7f7f7;
  padding: 20px;
}
.kana   { font-size: 2em; margin-bottom: 8px; }
.kanji  { font-size: 1.6em; color: #16213e; }
.eng    { font-size: 1em; color: #555; margin: 6px 0; }
.pitch  { font-size: 0.85em; color: #888; margin: 4px 0; }
.example{ font-size: 0.9em; color: #333; border-top: 1px solid #ccc;
          margin-top: 10px; padding-top: 8px; }
.module { font-size: 0.75em; color: #aaa; margin-top: 10px; }
"""


# ---------------------------------------------------------------------------
# Genanki model definitions
# ---------------------------------------------------------------------------

def make_vocab_model():
    return genanki.Model(
        VOCAB_MODEL_ID,
        'Japan-Learning Vocab',
        fields=[
            {'name': 'Id'},
            {'name': 'Kana'},
            {'name': 'Kanji'},
            {'name': 'English'},
            {'name': 'Pitch'},
            {'name': 'ExampleKana'},
            {'name': 'ExampleKanji'},
            {'name': 'ExampleEnglish'},
            {'name': 'Module'},
        ],
        templates=[
            {
                'name': 'Recognition',
                'qfmt': (
                    '<div class="kana">{{Kana}}</div>'
                    '<div class="module">Module {{Module}}</div>'
                ),
                'afmt': (
                    '{{FrontSide}}<hr>'
                    '<div class="kanji">{{Kanji}}</div>'
                    '<div class="eng">{{English}}</div>'
                    '<div class="pitch">Pitch: {{Pitch}}</div>'
                    '{{#ExampleKana}}'
                    '<div class="example">'
                    '<div>{{ExampleKana}}</div>'
                    '{{#ExampleKanji}}<div>{{ExampleKanji}}</div>{{/ExampleKanji}}'
                    '<div><em>{{ExampleEnglish}}</em></div>'
                    '</div>'
                    '{{/ExampleKana}}'
                ),
            }
        ],
        css=CARD_CSS,
    )


def make_kanji_model():
    return genanki.Model(
        KANJI_MODEL_ID,
        'Japan-Learning Kanji',
        fields=[
            {'name': 'Kanji'},
            {'name': 'MeaningPrimary'},
            {'name': 'OnYomi'},
            {'name': 'KunYomi'},
            {'name': 'StrokeCount'},
            {'name': 'ExampleKanji'},
            {'name': 'ExampleKana'},
            {'name': 'ExampleEnglish'},
            {'name': 'Module'},
        ],
        templates=[
            {
                'name': 'Recognition',
                'qfmt': (
                    '<div class="kana" style="font-size:3em">{{Kanji}}</div>'
                    '<div class="eng">What does this kanji mean?</div>'
                    '<div class="module">Module {{Module}}</div>'
                ),
                'afmt': (
                    '{{FrontSide}}<hr>'
                    '<div class="kanji">{{MeaningPrimary}}</div>'
                    '<div class="pitch">On: {{OnYomi}} &nbsp;|&nbsp; Kun: {{KunYomi}}</div>'
                    '<div class="pitch">Strokes: {{StrokeCount}}</div>'
                    '{{#ExampleKanji}}'
                    '<div class="example">'
                    '<div>{{ExampleKanji}}</div>'
                    '<div>{{ExampleKana}}</div>'
                    '<div><em>{{ExampleEnglish}}</em></div>'
                    '</div>'
                    '{{/ExampleKanji}}'
                ),
            }
        ],
        css=CARD_CSS,
    )


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

def read_csv_rows(path: str) -> list[dict]:
    """Read a CSV into a list of dicts.  Returns [] on missing / header-only files."""
    if not os.path.exists(path):
        return []
    rows = []
    try:
        with open(path, 'r', encoding='utf-8', newline='') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rows.append(row)
    except OSError:
        return []
    return rows


# ---------------------------------------------------------------------------
# Vocab deck builder
# ---------------------------------------------------------------------------

def build_vocab_deck(
    deck_id: int,
    deck_name: str,
    csv_path: str,
    model,
) -> tuple[object | None, int]:
    """Build a genanki Deck from a tier CSV.

    Returns (deck, note_count).  Returns (None, 0) if the CSV has no data rows.
    """
    rows = read_csv_rows(csv_path)
    if not rows:
        return None, 0

    deck = genanki.Deck(deck_id, deck_name)

    for row in rows:
        vocab_id  = (row.get('id')    or '').strip()
        kana      = (row.get('kana')  or '').strip()
        kanji     = (row.get('kanji') or '').strip() or kana
        english_raw = row.get('english') or ''
        # english field may be JSON array string or a plain comma-separated string
        if english_raw.startswith('['):
            try:
                english_list = json.loads(english_raw)
                english = ', '.join(str(e) for e in english_list)
            except json.JSONDecodeError:
                english = english_raw
        else:
            english = english_raw

        # Pitch accent
        pitch_pattern = (row.get('pitch_accent_pattern') or
                         row.get('pitch_pattern') or
                         row.get('pitch') or '').strip()
        pitch_drop    = (row.get('pitch_accent_drop_after_mora') or
                         row.get('drop_after_mora') or '').strip()
        pitch = pitch_pattern
        if pitch_drop:
            pitch = f'{pitch_pattern} (drop after mora {pitch_drop})'
        if not pitch:
            pitch = '—'

        # Example sentence (optional columns)
        ex_kana    = (row.get('example_kana')    or '').strip()
        ex_kanji   = (row.get('example_kanji')   or '').strip()
        ex_english = (row.get('example_english') or '').strip()

        module = str(row.get('module_introduced') or '').strip() or '?'

        note = genanki.Note(
            model=model,
            fields=[
                vocab_id,
                kana,
                kanji,
                english,
                pitch,
                ex_kana,
                ex_kanji,
                ex_english,
                module,
            ],
        )
        deck.add_note(note)

    return deck, len(rows)


# ---------------------------------------------------------------------------
# Kanji deck builder
# ---------------------------------------------------------------------------

def build_kanji_deck(
    deck_id: int,
    deck_name: str,
    csv_path: str,
    model,
) -> tuple[object | None, int]:
    """Build a genanki Deck from kanji-by-module.csv.

    Expected columns: order, kanji, primary_meaning, on, kun, module
    Returns (deck, note_count). Returns (None, 0) if empty.
    """
    rows = read_csv_rows(csv_path)
    if not rows:
        return None, 0

    deck = genanki.Deck(deck_id, deck_name)

    for row in rows:
        kanji         = (row.get('kanji')           or '').strip()
        meaning       = (row.get('primary_meaning')  or '').strip()
        on_yomi       = (row.get('on')               or '').strip()
        kun_yomi      = (row.get('kun')              or '').strip()
        stroke_count  = (row.get('stroke_count')     or '').strip()
        module        = str(row.get('module')         or '').strip() or '?'
        ex_kanji      = (row.get('example_kanji')    or '').strip()
        ex_kana       = (row.get('example_kana')     or '').strip()
        ex_english    = (row.get('example_english')  or '').strip()

        if not kanji:
            continue

        note = genanki.Note(
            model=model,
            fields=[
                kanji,
                meaning,
                on_yomi,
                kun_yomi,
                stroke_count,
                ex_kanji,
                ex_kana,
                ex_english,
                module,
            ],
        )
        deck.add_note(note)

    return deck, len(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog='export_to_anki.py',
        description=(
            'Convert japan-learning vocab CSVs and kanji CSV into Anki .apkg decks.\n\n'
            'Produces up to four decks:\n'
            '  tier-1.apkg  — from vocab/tier-1-core-300.csv\n'
            '  tier-2.apkg  — from vocab/tier-2-expand-700.csv\n'
            '  tier-3.apkg  — from vocab/tier-3-fluency-1500.csv\n'
            '  kanji.apkg   — from kanji/kanji-by-module.csv\n\n'
            'Requires: pip install genanki\n\n'
            'Header-only or absent CSVs are skipped gracefully.\n'
            'Exits 0 on success or when genanki is not installed.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--repo-root',
        default=None,
        metavar='PATH',
        help=(
            'Absolute path to the repository root. '
            'Defaults to the parent of the directory containing this script.'
        ),
    )
    parser.add_argument(
        '--output-dir',
        default=None,
        metavar='PATH',
        help=(
            'Directory in which to write .apkg files. '
            'Defaults to <repo-root>/vocab/anki-export/.'
        ),
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Dependency check
    # ------------------------------------------------------------------
    if not GENANKI_AVAILABLE:
        print('ERROR: The `genanki` library is not installed.')
        print()
        print('To install it, run:')
        print('  pip install genanki')
        print()
        print('Then re-run this script.')
        sys.exit(0)

    # ------------------------------------------------------------------
    # Resolve paths
    # ------------------------------------------------------------------
    if args.repo_root:
        repo_root = os.path.abspath(args.repo_root)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(script_dir)

    if args.output_dir:
        output_dir = os.path.abspath(args.output_dir)
    else:
        output_dir = os.path.join(repo_root, 'vocab', 'anki-export')

    os.makedirs(output_dir, exist_ok=True)

    print(f'Repository root : {repo_root}')
    print(f'Output directory: {output_dir}')
    print()

    vocab_model = make_vocab_model()
    kanji_model = make_kanji_model()

    jobs = [
        # (csv_path, deck_id, deck_name, output_name, is_kanji)
        (
            os.path.join(repo_root, 'vocab', 'tier-1-core-300.csv'),
            TIER1_DECK_ID,
            'Japanese::Tier 1 — Core 300',
            'tier-1.apkg',
            False,
        ),
        (
            os.path.join(repo_root, 'vocab', 'tier-2-expand-700.csv'),
            TIER2_DECK_ID,
            'Japanese::Tier 2 — Expand 700',
            'tier-2.apkg',
            False,
        ),
        (
            os.path.join(repo_root, 'vocab', 'tier-3-fluency-1500.csv'),
            TIER3_DECK_ID,
            'Japanese::Tier 3 — Fluency 1500',
            'tier-3.apkg',
            False,
        ),
        (
            os.path.join(repo_root, 'kanji', 'kanji-by-module.csv'),
            KANJI_DECK_ID,
            'Japanese::Kanji by Module',
            'kanji.apkg',
            True,
        ),
    ]

    any_exported = False

    for csv_path, deck_id, deck_name, output_name, is_kanji in jobs:
        csv_rel = os.path.relpath(csv_path, repo_root)
        print(f'Processing {csv_rel} …')

        if not os.path.exists(csv_path):
            print(f'  File not found — skipping.')
            print()
            continue

        if is_kanji:
            deck, count = build_kanji_deck(deck_id, deck_name, csv_path, kanji_model)
        else:
            deck, count = build_vocab_deck(deck_id, deck_name, csv_path, vocab_model)

        if deck is None or count == 0:
            print(f'  No data rows found (header-only or empty) — skipping.')
            print()
            continue

        out_path = os.path.join(output_dir, output_name)
        package = genanki.Package(deck)
        package.write_to_file(out_path)
        print(f'  Wrote {count} cards → {out_path}')
        any_exported = True
        print()

    if any_exported:
        print('Export complete.')
    else:
        print('No decks exported (all source files are empty or absent).')
        print('This is expected for a freshly scaffolded repo.')

    sys.exit(0)


if __name__ == '__main__':
    main()
