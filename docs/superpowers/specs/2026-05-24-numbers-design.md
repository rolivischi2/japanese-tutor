---
title: Numbers 1–99 — interactive composition builder
date: 2026-05-24
status: approved
---

# Numbers 1–99 — interactive composition builder

## Goal

A `/numbers` page where the learner types a number 1–99 and immediately sees its Japanese composition broken into visual chips (e.g. `25` → `に` · `じゅう` · `ご`), with romaji ruby above each part. Reference tiles for 1–10 and 10–90 are clickable to populate the input. Three rules are summarized at the bottom. Same paper/vermilion aesthetic as the rest of the site; self-contained HTML.

## Non-goals

- Numbers above 99 (no ひゃく/せん/万 sound changes).
- Counter words (本, 枚, 人, つ, etc.).
- Audio TTS.
- Quiz / SRS mode.
- External libraries — no wanakana, no kuroshiro. Hard-coded lookup table.

## Decisions

1. **Hard-coded lookup**, ones digit (1–9 + 10). 10 entries × kana + romaji.
2. **Reading variants**: display よん / なな / きゅう by default. Footnote notes し / しち / く as alternatives used in some compounds. Single canonical form keeps the builder unambiguous.
3. **Composition rules** (built into the algorithm):
   - 1–9: just the ones digit
   - 10: じゅう alone
   - 11–19: じゅう + ones (e.g. 11 = じゅういち)
   - 20–90 multiples of 10: ones + じゅう (e.g. 20 = にじゅう)
   - 21–99 non-multiples: tens + ones (e.g. 25 = にじゅうご)
4. **Visual chips** for each component, with subtle slide-in animation on number change.
5. **Reference grids** below the builder: 1–10 tiles, then 10–90 tiles. Both clickable.
6. **5th landing card** "Numbers" (icon: 数). Landing grid switches from `repeat(2,1fr)` to `repeat(auto-fit, minmax(260px, 1fr))` so 5 cards fit cleanly.

## Files

- **Create** `tools/numbers.html` — self-contained HTML, ~250 lines.
- **Modify** `tools/build_site.py` — add `(OUT_DIR / "numbers").mkdir()` alongside `kana/chart/reader/dict`.
- **Modify** `scripts/build-vercel.sh` — add `cp tools/numbers.html "$OUT/numbers/index.html"`. Echo summary updated.
- **Modify** `tools/templates/landing.html` — fifth card; grid becomes auto-fit.

## Verification

- `bash scripts/build-vercel.sh` succeeds; `public/numbers/index.html` exists.
- Open `/numbers/`:
  - Input accepts 1–99; rejects others.
  - Typing `25` shows three chips (`に`, `じゅう`, `ご`) with `ni`, `jū`, `go` ruby; combined reading `にじゅうご` and "twenty-five" below.
  - Typing `1` shows one chip; typing `10` shows one chip (`じゅう`); typing `11` shows two (`じゅう` + `いち`); typing `20` shows two (`に` + `じゅう`).
  - Click a reference tile → input populates, composition re-renders.
- Landing now shows 5 cards; on a wide desktop they form 3+2 or 5-across (auto-fit); on mobile they stack.
- Deployed: `curl -sI https://japan-learning-omega.vercel.app/numbers/` returns 200.
