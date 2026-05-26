#!/usr/bin/env bash
# Vercel build step. Generates the landing + rendered module pages via
# tools/build_site.py, then copies the two standalone HTML artifacts
# (kana guide, printable chart) into public/. The rest of the repo
# (Markdown lessons, vocab CSVs, Python tools, .venv, etc.) stays out
# of the deployed site.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/public"

# build_site.py wipes and recreates $OUT, including empty kana/ and chart/
# subdirectories. Subsequent cp commands populate those subdirectories.
uv run "$ROOT/tools/build_site.py"

cp "$ROOT/modules/00-writing-systems/kana-guide.html" "$OUT/kana/index.html"
cp "$ROOT/pronunciation/11-kana-printable-chart.html" "$OUT/chart/index.html"
cp "$ROOT/tools/numbers.html"                         "$OUT/numbers/index.html"
cp "$ROOT/tools/drill.html"                           "$OUT/drill/index.html"
cp "$ROOT/tools/assets/favicon.png"                   "$OUT/favicon.png"
cp "$ROOT/tutor/m01-situations-source.pdf"            "$OUT/modules/01-copula-basics/source.pdf"
cp "$ROOT/tools/data/jmdict-index.json"               "$OUT/jmdict-index.json"

echo
echo "Built $OUT/"
echo "  /                        → $OUT/index.html"
echo "  /kana                    → $OUT/kana/index.html"
echo "  /chart                   → $OUT/chart/index.html"
echo "  /dict                    → $OUT/dict/index.html"
echo "  /numbers                 → $OUT/numbers/index.html"
echo "  /drill                   → $OUT/drill/index.html"
echo "  /jmdict-index.json       → $OUT/jmdict-index.json (~44 MB)"
echo "  /modules/<slug>/...      → $OUT/modules/"
du -sh "$OUT"
