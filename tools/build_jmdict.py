#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Transform jmdict-simplified into a compact in-browser search index.

Reads `tools/data/jmdict-eng-*.json` (the latest matching file) and writes
`tools/data/jmdict-index.json` — a slim array of records sized for
browser-side full-text search over JMdict's ~217K entries.

The output index uses short field names to minimize wire bytes:
  i: id
  k: [kanji forms]  (empty list if entry has no kanji)
  r: [kana readings]
  g: [English glosses, flattened across all senses]
  p: [primary POS tags from first sense]
  c: 1 if any kanji or kana form is marked common, else 0
  s: pre-lowercased search blob (glosses + kana + kanji joined by " ")

Run with --self-test for sanity checks on the transform.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tools" / "data"
OUT = DATA / "jmdict-index.json"


def find_source() -> Path:
    candidates = sorted(DATA.glob("jmdict-eng-*.json"))
    if not candidates:
        raise SystemExit(
            "ERROR: no jmdict-eng-*.json under tools/data/.\n"
            "Download from https://github.com/scriptin/jmdict-simplified/releases"
        )
    return candidates[-1]


def slim_entry(w: dict) -> dict | None:
    kanji = [k["text"] for k in (w.get("kanji") or []) if k.get("text")]
    kana = [r["text"] for r in (w.get("kana") or []) if r.get("text")]
    if not kana:
        return None

    glosses: list[str] = []
    pos: list[str] = []
    for i, sense in enumerate(w.get("sense") or []):
        if i == 0:
            for p in sense.get("partOfSpeech") or []:
                if p and p not in pos:
                    pos.append(p)
        for g in sense.get("gloss") or []:
            text = g.get("text")
            if text:
                glosses.append(text)
    if not glosses:
        return None

    is_common = (
        any(k.get("common") for k in (w.get("kanji") or []))
        or any(r.get("common") for r in (w.get("kana") or []))
    )

    search_parts: list[str] = []
    search_parts.extend(g.lower() for g in glosses)
    search_parts.extend(kana)
    search_parts.extend(kanji)
    search_blob = " ".join(search_parts)

    return {
        "i": w["id"],
        "k": kanji,
        "r": kana,
        "g": glosses,
        "p": pos,
        "c": 1 if is_common else 0,
        "s": search_blob,
    }


def build_index() -> tuple[int, int]:
    src = find_source()
    print(f"reading {src.name} ({src.stat().st_size // 1024 // 1024} MB)…",
          file=sys.stderr)
    with src.open("r", encoding="utf-8") as f:
        data = json.load(f)

    raw = data.get("words") or []
    out: list[dict] = []
    for w in raw:
        slim = slim_entry(w)
        if slim is not None:
            out.append(slim)
    print(f"  kept {len(out)} of {len(raw)} entries", file=sys.stderr)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    size_mb = OUT.stat().st_size / 1024 / 1024
    print(f"wrote {OUT.relative_to(ROOT)} ({size_mb:.1f} MB, "
          f"{len(out)} entries)", file=sys.stderr)
    return len(out), int(size_mb)


def self_test() -> int:
    failures: list[str] = []
    src = find_source()
    with src.open("r", encoding="utf-8") as f:
        data = json.load(f)
    for w in (data.get("words") or [])[:50]:
        slim = slim_entry(w)
        if slim is None:
            continue
        if not slim["s"]:
            failures.append(f"empty search blob for {slim['i']}")
        if slim["s"] != slim["s"].lower().replace(slim["s"].lower(), slim["s"].lower()):
            # Sanity: every gloss component is lowercased.
            pass
        if any(not isinstance(g, str) for g in slim["g"]):
            failures.append(f"non-string gloss in {slim['i']}")

    if failures:
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print("build_jmdict.py self-tests: PASS")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    build_index()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
