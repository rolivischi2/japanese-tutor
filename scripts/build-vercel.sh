#!/usr/bin/env bash
# Vercel build step. Copies the two user-facing HTML artifacts and a
# landing page into public/, which is what Vercel deploys. The rest of
# the repo (Markdown lessons, vocab CSVs, Python tools, .venv, etc.)
# stays out of the deployed site.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/public"

rm -rf "$OUT"
mkdir -p "$OUT/kana" "$OUT/chart"

cp "$ROOT/modules/00-writing-systems/kana-guide.html" "$OUT/kana/index.html"
cp "$ROOT/pronunciation/11-kana-printable-chart.html" "$OUT/chart/index.html"
cp "$ROOT/scripts/landing.html"                       "$OUT/index.html"

echo
echo "Built $OUT/"
echo "  /        → $OUT/index.html"
echo "  /kana    → $OUT/kana/index.html"
echo "  /chart   → $OUT/chart/index.html"
du -h "$OUT"/{index.html,kana/index.html,chart/index.html} | sort -k2
