"""validate.py — Consistency checker for the japan-learning knowledge base.

Performs three checks:

  1. KANJI GATING
     For every module's dialogues.md, find all CJK Unified Ideograph characters
     (U+4E00–U+9FFF) and verify each one appears in kanji/kanji-master.json with
     module_introduced <= that module's number.  This enforces the rule that no
     module may use a kanji before it has been formally introduced.

  2. VOCAB ID REFERENTIAL INTEGRITY
     For every entry in kanji/kanji-master.json, check that each id listed in
     vocab_using exists in at least one of the three tier CSVs under vocab/:
       tier-1-core-300.csv, tier-2-expand-700.csv, tier-3-fluency-1500.csv

  3. STRUCTURAL VALIDATION (lightweight, no third-party libs)
     For every vocab/*/module-vocab.json file, check that each object in the array
     has at least the required fields defined in vocab/schema.json:
       id, kana, reading, pos, english, module_introduced
     Also verifies pos values belong to the allowed enum.

Missing or empty data files (empty JSON arrays, header-only CSVs, absent files)
are handled gracefully — they are reported as "nothing to check" and never cause
a crash.

Usage:
  python3 tools/validate.py [--help] [--repo-root PATH]

Exit codes:
  0  All checks passed (or nothing to check)
  1  One or more validation errors found
"""

import argparse
import csv
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# CJK Unified Ideographs range (U+4E00–U+9FFF)
# ---------------------------------------------------------------------------
CJK_RE = re.compile(r'[一-鿿]')

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
VALID_POS = {
    'noun', 'verb-godan', 'verb-ichidan', 'verb-irregular',
    'i-adj', 'na-adj', 'adv', 'particle', 'conj', 'interj', 'counter',
}
REQUIRED_VOCAB_FIELDS = {'id', 'kana', 'reading', 'pos', 'english', 'module_introduced'}
TIER_CSVS = [
    'tier-1-core-300.csv',
    'tier-2-expand-700.csv',
    'tier-3-fluency-1500.csv',
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json_safe(path: str):
    """Load JSON from path; return None if file missing, None if unreadable."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        return exc  # caller will inspect type


def module_number_from_path(path: str) -> int | None:
    """Extract the two-digit module number from a path like .../modules/04-verbs-.../...
    Returns None if no match.
    """
    match = re.search(r'modules[/\\](\d{2})-', path)
    if match:
        return int(match.group(1))
    return None


def collect_dialogues(repo_root: str) -> list[tuple[int, str]]:
    """Return list of (module_number, filepath) for every dialogues.md found."""
    results = []
    modules_dir = os.path.join(repo_root, 'modules')
    if not os.path.isdir(modules_dir):
        return results
    for entry in sorted(os.listdir(modules_dir)):
        entry_path = os.path.join(modules_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        module_num = module_number_from_path(entry_path + os.sep)
        if module_num is None:
            continue
        dialogues_path = os.path.join(entry_path, 'dialogues.md')
        if os.path.exists(dialogues_path):
            results.append((module_num, dialogues_path))
    return results


def collect_module_vocab_jsons(repo_root: str) -> list[str]:
    """Return list of paths to module-vocab.json files across all modules."""
    results = []
    modules_dir = os.path.join(repo_root, 'modules')
    if not os.path.isdir(modules_dir):
        return results
    for entry in sorted(os.listdir(modules_dir)):
        entry_path = os.path.join(modules_dir, entry)
        if not os.path.isdir(entry_path):
            continue
        mv_path = os.path.join(entry_path, 'module-vocab.json')
        if os.path.exists(mv_path):
            results.append(mv_path)
    return results


def load_kanji_master(repo_root: str) -> tuple[dict | None, str | None]:
    """Load kanji-master.json; return (dict keyed by kanji char, error_message)."""
    path = os.path.join(repo_root, 'kanji', 'kanji-master.json')
    data = load_json_safe(path)
    if data is None:
        return None, f'kanji/kanji-master.json not found at {path}'
    if isinstance(data, Exception):
        return None, f'kanji/kanji-master.json is not valid JSON: {data}'
    if not isinstance(data, list):
        return None, 'kanji/kanji-master.json must be a JSON array'
    if len(data) == 0:
        return {}, None  # valid but empty
    index = {}
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            return None, f'kanji/kanji-master.json entry #{i} is not an object'
        k = entry.get('kanji')
        if not k or not isinstance(k, str):
            return None, f'kanji/kanji-master.json entry #{i} missing "kanji" field'
        index[k] = entry
    return index, None


def load_tier_vocab_ids(repo_root: str) -> set[str]:
    """Collect all vocab ids from the three tier CSV files. Returns a set of strings."""
    ids: set[str] = set()
    vocab_dir = os.path.join(repo_root, 'vocab')
    for filename in TIER_CSVS:
        path = os.path.join(vocab_dir, filename)
        if not os.path.exists(path):
            continue
        try:
            with open(path, 'r', encoding='utf-8', newline='') as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    vocab_id = (row.get('id') or '').strip()
                    if vocab_id:
                        ids.add(vocab_id)
        except OSError:
            pass
    return ids


# ---------------------------------------------------------------------------
# Check 1: Kanji gating
# ---------------------------------------------------------------------------

def check_kanji_gating(repo_root: str, kanji_index: dict) -> list[str]:
    """Return list of error strings (empty = pass)."""
    errors = []
    dialogues = collect_dialogues(repo_root)

    if not dialogues:
        print('  [kanji-gating] No dialogues.md files found — nothing to check.')
        return errors

    for module_num, path in dialogues:
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                text = fh.read()
        except OSError as exc:
            errors.append(f'Cannot read {path}: {exc}')
            continue

        kanji_chars = set(CJK_RE.findall(text))
        if not kanji_chars:
            print(f'  [kanji-gating] Module {module_num:02d} dialogues.md — no kanji found, nothing to check.')
            continue

        for char in sorted(kanji_chars):
            if char not in kanji_index:
                errors.append(
                    f'Module {module_num:02d} dialogues.md uses 「{char}」 '
                    f'which is NOT in kanji-master.json at all.'
                )
            else:
                introduced = kanji_index[char].get('module_introduced')
                if introduced is None:
                    errors.append(
                        f'Module {module_num:02d} dialogues.md uses 「{char}」 '
                        f'whose kanji-master.json entry has no module_introduced field.'
                    )
                elif introduced > module_num:
                    errors.append(
                        f'Module {module_num:02d} dialogues.md uses 「{char}」 '
                        f'but it is introduced in Module {introduced} (too late).'
                    )

    return errors


# ---------------------------------------------------------------------------
# Check 2: vocab_using referential integrity
# ---------------------------------------------------------------------------

def check_vocab_using(kanji_index: dict, tier_ids: set[str]) -> list[str]:
    """Return list of error strings (empty = pass)."""
    errors = []

    if not kanji_index:
        print('  [vocab-using]  kanji-master.json is empty — nothing to check.')
        return errors

    if not tier_ids:
        # No tier CSVs have data yet; skip referential integrity
        print('  [vocab-using]  All tier CSVs are empty or absent — nothing to check.')
        return errors

    for char, entry in sorted(kanji_index.items()):
        for vocab_id in entry.get('vocab_using', []):
            if vocab_id not in tier_ids:
                errors.append(
                    f'kanji-master.json entry 「{char}」 references vocab id '
                    f'"{vocab_id}" which does not exist in any tier CSV.'
                )

    return errors


# ---------------------------------------------------------------------------
# Check 3: Structural validation of module-vocab.json files
# ---------------------------------------------------------------------------

def check_module_vocab_structure(repo_root: str) -> list[str]:
    """Return list of error strings (empty = pass)."""
    errors = []
    paths = collect_module_vocab_jsons(repo_root)

    if not paths:
        print('  [vocab-struct] No module-vocab.json files found — nothing to check.')
        return errors

    for path in paths:
        relative = os.path.relpath(path, repo_root)
        data = load_json_safe(path)

        if data is None:
            print(f'  [vocab-struct] {relative} — file absent, skipping.')
            continue
        if isinstance(data, Exception):
            errors.append(f'{relative}: invalid JSON — {data}')
            continue
        if not isinstance(data, list):
            errors.append(f'{relative}: top-level value must be a JSON array.')
            continue
        if len(data) == 0:
            print(f'  [vocab-struct] {relative} — empty array, nothing to check.')
            continue

        for i, entry in enumerate(data):
            if not isinstance(entry, dict):
                errors.append(f'{relative} entry #{i}: not an object.')
                continue

            # Check required fields
            missing = REQUIRED_VOCAB_FIELDS - entry.keys()
            if missing:
                errors.append(
                    f'{relative} entry #{i} (id={entry.get("id", "?")}): '
                    f'missing required fields: {sorted(missing)}'
                )

            # Check pos enum
            pos = entry.get('pos')
            if pos is not None and pos not in VALID_POS:
                errors.append(
                    f'{relative} entry #{i} (id={entry.get("id", "?")}): '
                    f'invalid pos "{pos}". Must be one of: {sorted(VALID_POS)}'
                )

            # Check english is a list
            english = entry.get('english')
            if english is not None and not isinstance(english, list):
                errors.append(
                    f'{relative} entry #{i} (id={entry.get("id", "?")}): '
                    f'"english" must be an array, got {type(english).__name__}'
                )

            # Check module_introduced is an integer
            mod = entry.get('module_introduced')
            if mod is not None and not isinstance(mod, int):
                errors.append(
                    f'{relative} entry #{i} (id={entry.get("id", "?")}): '
                    f'"module_introduced" must be an integer, got {type(mod).__name__}'
                )

    return errors


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog='validate.py',
        description=(
            'Consistency checker for the japan-learning knowledge base.\n\n'
            'Checks:\n'
            '  1. Every kanji in modules/*/dialogues.md is in kanji-master.json\n'
            '     with module_introduced <= that module\'s number.\n'
            '  2. Every vocab id in kanji-master.json vocab_using exists in a\n'
            '     tier CSV (tier-1, tier-2, or tier-3).\n'
            '  3. Every module-vocab.json has structurally valid entries.\n\n'
            'Empty/missing files are treated as "nothing to check" (not errors).\n'
            'Exits 0 on success, 1 on any validation failure.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--repo-root',
        default=None,
        metavar='PATH',
        help=(
            'Absolute path to the repository root. '
            'Defaults to the directory containing this script\'s parent (i.e. the repo root).'
        ),
    )
    args = parser.parse_args()

    # Determine repo root
    if args.repo_root:
        repo_root = os.path.abspath(args.repo_root)
    else:
        # tools/validate.py lives in <repo_root>/tools/
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(script_dir)

    print(f'Repository root: {repo_root}')
    print()

    all_errors: list[str] = []

    # ------------------------------------------------------------------
    # Load shared data
    # ------------------------------------------------------------------
    print('Loading kanji-master.json …')
    kanji_index, km_error = load_kanji_master(repo_root)
    if km_error:
        print(f'  WARNING: {km_error}')
        kanji_index = {}
    else:
        count = len(kanji_index)
        if count == 0:
            print('  kanji-master.json present but empty — kanji checks will have nothing to verify.')
        else:
            print(f'  Loaded {count} kanji entries.')

    print()
    print('Loading tier CSV vocab ids …')
    tier_ids = load_tier_vocab_ids(repo_root)
    if tier_ids:
        print(f'  Loaded {len(tier_ids)} unique vocab ids from tier CSVs.')
    else:
        print('  No vocab ids found in tier CSVs (files absent or header-only).')

    print()

    # ------------------------------------------------------------------
    # Check 1
    # ------------------------------------------------------------------
    print('CHECK 1: Kanji gating in dialogues.md files')
    errors1 = check_kanji_gating(repo_root, kanji_index)
    if errors1:
        for e in errors1:
            print(f'  ERROR: {e}')
        all_errors.extend(errors1)
    else:
        print('  PASS')

    print()

    # ------------------------------------------------------------------
    # Check 2
    # ------------------------------------------------------------------
    print('CHECK 2: vocab_using referential integrity in kanji-master.json')
    errors2 = check_vocab_using(kanji_index, tier_ids)
    if errors2:
        for e in errors2:
            print(f'  ERROR: {e}')
        all_errors.extend(errors2)
    else:
        print('  PASS')

    print()

    # ------------------------------------------------------------------
    # Check 3
    # ------------------------------------------------------------------
    print('CHECK 3: Structural validation of module-vocab.json files')
    errors3 = check_module_vocab_structure(repo_root)
    if errors3:
        for e in errors3:
            print(f'  ERROR: {e}')
        all_errors.extend(errors3)
    else:
        print('  PASS')

    print()

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print('=' * 60)
    if all_errors:
        print(f'FAIL — {len(all_errors)} error(s) found.')
        sys.exit(1)
    else:
        print('PASS — all checks succeeded (or nothing to check).')
        sys.exit(0)


if __name__ == '__main__':
    main()
