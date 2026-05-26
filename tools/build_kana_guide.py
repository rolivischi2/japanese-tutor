#!/usr/bin/env python3
"""Build the self-contained interactive kana guide.

Reads KanjiVG-derived stroke data from ``tools/data/kana-strokes.json`` and the
curated kana metadata below, then emits a single self-contained HTML file at
``modules/00-writing-systems/kana-guide.html`` — no server, no build step at
view time, just open it in a browser.

Usage:  python3 tools/build_kana_guide.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STROKE_PATH = os.path.join(ROOT, "tools", "data", "kana-strokes.json")
OUT_PATH = os.path.join(ROOT, "modules", "00-writing-systems", "kana-guide.html")

# --------------------------------------------------------------------------
# Kana tables. Each section row is (consonant-label, [chars | None]).
# romaji lives in ROMAJI; gaps in the gojuon grid are None.
# --------------------------------------------------------------------------
HIRA_BASE = [
    ("",  ["あ", "い", "う", "え", "お"]),
    ("k", ["か", "き", "く", "け", "こ"]),
    ("s", ["さ", "し", "す", "せ", "そ"]),
    ("t", ["た", "ち", "つ", "て", "と"]),
    ("n", ["な", "に", "ぬ", "ね", "の"]),
    ("h", ["は", "ひ", "ふ", "へ", "ほ"]),
    ("m", ["ま", "み", "む", "め", "も"]),
    ("y", ["や", None, "ゆ", None, "よ"]),
    ("r", ["ら", "り", "る", "れ", "ろ"]),
    ("w", ["わ", None, None, None, "を"]),
    ("n", ["ん", None, None, None, None]),
]
HIRA_DAKU = [
    ("g", ["が", "ぎ", "ぐ", "げ", "ご"]),
    ("z", ["ざ", "じ", "ず", "ぜ", "ぞ"]),
    ("d", ["だ", "ぢ", "づ", "で", "ど"]),
    ("b", ["ば", "び", "ぶ", "べ", "ぼ"]),
    ("p", ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"]),
]
HIRA_YOON = [
    ("ky", ["きゃ", "きゅ", "きょ"]),
    ("sh", ["しゃ", "しゅ", "しょ"]),
    ("ch", ["ちゃ", "ちゅ", "ちょ"]),
    ("ny", ["にゃ", "にゅ", "にょ"]),
    ("hy", ["ひゃ", "ひゅ", "ひょ"]),
    ("my", ["みゃ", "みゅ", "みょ"]),
    ("ry", ["りゃ", "りゅ", "りょ"]),
    ("gy", ["ぎゃ", "ぎゅ", "ぎょ"]),
    ("j",  ["じゃ", "じゅ", "じょ"]),
    ("by", ["びゃ", "びゅ", "びょ"]),
    ("py", ["ぴゃ", "ぴゅ", "ぴょ"]),
]
KATA_BASE = [
    ("",  ["ア", "イ", "ウ", "エ", "オ"]),
    ("k", ["カ", "キ", "ク", "ケ", "コ"]),
    ("s", ["サ", "シ", "ス", "セ", "ソ"]),
    ("t", ["タ", "チ", "ツ", "テ", "ト"]),
    ("n", ["ナ", "ニ", "ヌ", "ネ", "ノ"]),
    ("h", ["ハ", "ヒ", "フ", "ヘ", "ホ"]),
    ("m", ["マ", "ミ", "ム", "メ", "モ"]),
    ("y", ["ヤ", None, "ユ", None, "ヨ"]),
    ("r", ["ラ", "リ", "ル", "レ", "ロ"]),
    ("w", ["ワ", None, None, None, "ヲ"]),
    ("n", ["ン", None, None, None, None]),
]
KATA_DAKU = [
    ("g", ["ガ", "ギ", "グ", "ゲ", "ゴ"]),
    ("z", ["ザ", "ジ", "ズ", "ゼ", "ゾ"]),
    ("d", ["ダ", "ヂ", "ヅ", "デ", "ド"]),
    ("b", ["バ", "ビ", "ブ", "ベ", "ボ"]),
    ("p", ["パ", "ピ", "プ", "ペ", "ポ"]),
]
KATA_YOON = [
    ("ky", ["キャ", "キュ", "キョ"]),
    ("sh", ["シャ", "シュ", "ショ"]),
    ("ch", ["チャ", "チュ", "チョ"]),
    ("ny", ["ニャ", "ニュ", "ニョ"]),
    ("hy", ["ヒャ", "ヒュ", "ヒョ"]),
    ("my", ["ミャ", "ミュ", "ミョ"]),
    ("ry", ["リャ", "リュ", "リョ"]),
    ("gy", ["ギャ", "ギュ", "ギョ"]),
    ("j",  ["ジャ", "ジュ", "ジョ"]),
    ("by", ["ビャ", "ビュ", "ビョ"]),
    ("py", ["ピャ", "ピュ", "ピョ"]),
]

# romaji for every kana, both scripts share the mapping
ROMAJI = {
    "あ": "a", "い": "i", "う": "u", "え": "e", "お": "o",
    "か": "ka", "き": "ki", "く": "ku", "け": "ke", "こ": "ko",
    "さ": "sa", "し": "shi", "す": "su", "せ": "se", "そ": "so",
    "た": "ta", "ち": "chi", "つ": "tsu", "て": "te", "と": "to",
    "な": "na", "に": "ni", "ぬ": "nu", "ね": "ne", "の": "no",
    "は": "ha", "ひ": "hi", "ふ": "fu", "へ": "he", "ほ": "ho",
    "ま": "ma", "み": "mi", "む": "mu", "め": "me", "も": "mo",
    "や": "ya", "ゆ": "yu", "よ": "yo",
    "ら": "ra", "り": "ri", "る": "ru", "れ": "re", "ろ": "ro",
    "わ": "wa", "を": "wo", "ん": "n",
    "が": "ga", "ぎ": "gi", "ぐ": "gu", "げ": "ge", "ご": "go",
    "ざ": "za", "じ": "ji", "ず": "zu", "ぜ": "ze", "ぞ": "zo",
    "だ": "da", "ぢ": "ji", "づ": "zu", "で": "de", "ど": "do",
    "ば": "ba", "び": "bi", "ぶ": "bu", "べ": "be", "ぼ": "bo",
    "ぱ": "pa", "ぴ": "pi", "ぷ": "pu", "ぺ": "pe", "ぽ": "po",
}
# yoon romaji
for _cons, _r in [("き", "ky"), ("し", "sh"), ("ち", "ch"), ("に", "ny"),
                   ("ひ", "hy"), ("み", "my"), ("り", "ry"), ("ぎ", "gy"),
                   ("じ", "j"), ("び", "by"), ("ぴ", "py")]:
    for _small, _v in [("ゃ", "a"), ("ゅ", "u"), ("ょ", "o")]:
        base = _r + _v
        if _r in ("sh", "ch", "j"):
            base = _r + ("a" if _v == "a" else _v)  # sha shu sho / cha / ja
        ROMAJI[_cons + _small] = base

# katakana shares romaji with the hiragana of the same sound
_HK = {
    "ア": "あ", "イ": "い", "ウ": "う", "エ": "え", "オ": "お",
    "カ": "か", "キ": "き", "ク": "く", "ケ": "け", "コ": "こ",
    "サ": "さ", "シ": "し", "ス": "す", "セ": "せ", "ソ": "そ",
    "タ": "た", "チ": "ち", "ツ": "つ", "テ": "て", "ト": "と",
    "ナ": "な", "ニ": "に", "ヌ": "ぬ", "ネ": "ね", "ノ": "の",
    "ハ": "は", "ヒ": "ひ", "フ": "ふ", "ヘ": "へ", "ホ": "ほ",
    "マ": "ま", "ミ": "み", "ム": "む", "メ": "め", "モ": "も",
    "ヤ": "や", "ユ": "ゆ", "ヨ": "よ",
    "ラ": "ら", "リ": "り", "ル": "る", "レ": "れ", "ロ": "ろ",
    "ワ": "わ", "ヲ": "を", "ン": "ん",
    "ガ": "が", "ギ": "ぎ", "グ": "ぐ", "ゲ": "げ", "ゴ": "ご",
    "ザ": "ざ", "ジ": "じ", "ズ": "ず", "ゼ": "ぜ", "ゾ": "ぞ",
    "ダ": "だ", "ヂ": "ぢ", "ヅ": "づ", "デ": "で", "ド": "ど",
    "バ": "ば", "ビ": "び", "ブ": "ぶ", "ベ": "べ", "ボ": "ぼ",
    "パ": "ぱ", "ピ": "ぴ", "プ": "ぷ", "ペ": "ぺ", "ポ": "ぽ",
}
for _k, _h in _HK.items():
    ROMAJI[_k] = ROMAJI[_h]
_SMALL_K = {"ャ": "ゃ", "ュ": "ゅ", "ョ": "ょ"}
for _row in KATA_YOON:
    for _c in _row[1]:
        h = _HK[_c[0]] + _SMALL_K[_c[1]]
        ROMAJI[_c] = ROMAJI[h]

# Original mnemonics — shape tied to sound. Base kana only.
MNEMONIC = {
    "あ": "An <b>A</b>ntenna and a cross over a curl — say “ah”.",
    "い": "Two <b>ee</b>ls swimming side by side.",
    "う": "A face in profile making a <b>oo</b> shape with its mouth.",
    "え": "An <b>e</b>xotic bird with a swooping tail feather.",
    "お": "Like あ but with an extra tail — an <b>o</b>rbiting moon.",
    "か": "A mosquito (蚊 = ka) with one biting dot — say <b>ka</b>.",
    "き": "A <b>key</b> with two teeth.",
    "く": "A <b>cu</b>ckoo’s open beak.",
    "け": "A <b>ke</b>g lying on its side, tap on the left.",
    "こ": "Two <b>co</b>coon halves stacked up.",
    "さ": "A <b>sa</b>iling boat cutting a curl of water.",
    "し": "A fishing hook — <b>she</b> dangles a line.",
    "す": "A loop with a tail — a curly <b>soo</b>venir straw.",
    "せ": "A <b>se</b>at with a cross-bar back.",
    "そ": "A zig-zag <b>so</b>ck darned by hand.",
    "た": "A <b>ta</b>ll figure waving — ナ plus こ.",
    "ち": "A <b>chee</b>rful person leaning back, arms out.",
    "つ": "A <b>tsu</b>nami wave curling left.",
    "て": "A <b>te</b>lephone hook hanging down.",
    "と": "A <b>toe</b> pricked by a thorn.",
    "な": "A <b>na</b>il being hammered, with a knot of rope.",
    "に": "A <b>nee</b>dle threading two stitches.",
    "ぬ": "<b>Noo</b>dles twirled into a knotted loop.",
    "ね": "A cat’s curling tail — “<b>ne</b>-ko” means cat.",
    "の": "A swirling <b>no</b>-entry sign.",
    "は": "A person in a <b>ha</b>t — strokes 1, 3, like “hat”.",
    "ひ": "A wide smile — a person laughing “<b>hee</b>”.",
    "ふ": "Mount <b>Fu</b>ji seen from far away.",
    "へ": "A flat <b>he</b>adland — a low hill on the horizon.",
    "ほ": "は with an extra bar — a <b>ho</b>use’s mailbox.",
    "ま": "<b>Ma</b>ma tying her hair into a looped bun.",
    "み": "The number 2-1 — “<b>mee</b>t at 21”.",
    "む": "A cow with a tuft of hair, mooing “<b>moo</b>”.",
    "め": "An <b>e</b>ye with a ribbon — “me” means eye.",
    "も": "A fish-hook with two worms — catch <b>mo</b>re fish.",
    "や": "A <b>ya</b>cht with a billowing sail.",
    "ゆ": "A <b>u</b>nique fish with a looped fin.",
    "よ": "A <b>yo</b>-yo dangling on its string.",
    "ら": "A person sitting up straight — a “<b>ra</b>”-bbit.",
    "り": "Two drips from a leaky faucet — “<b>ree</b>”.",
    "る": "A curled <b>roo</b>te ending in a loop.",
    "れ": "る’s cousin, kneeling without the loop — “<b>re</b>”.",
    "ろ": "る with the loop opened — an open <b>ro</b>ad.",
    "わ": "れ’s cousin with a loop — a swirl of “<b>wa</b>”nder.",
    "を": "A person kicking a ball — the rare <b>o</b> particle. <b>Sounds exactly like お</b>; only ever used to mark a direct object.",
    "ん": "A lazy <b>n</b> squiggle, like the end of a signature.",
    "ア": "An <b>A</b> with one leg kicked out.",
    "イ": "An <b>ee</b>l leaning on a post.",
    "ウ": "A roof — someone sheltered under it says “<b>oo</b>”.",
    "エ": "An <b>e</b>ngineer’s steel I-beam.",
    "オ": "An <b>o</b>rgan pipe with a cross-brace.",
    "カ": "A box-<b>cu</b>tter’s sharp blade.",
    "キ": "A <b>key</b> — straight, with two notches.",
    "ク": "A <b>coo</b>kie with one bite taken out.",
    "ケ": "A <b>ke</b>ttle’s angular spout.",
    "コ": "An open <b>co</b>ntainer, two square corners.",
    "サ": "A <b>sa</b>ndcastle with a flag on top.",
    "シ": "<b>She</b> smiles — the strokes sweep gently UP ↗.",
    "ス": "A <b>soo</b>per-steep ski slope.",
    "セ": "A <b>se</b>ttee with a slanted backrest.",
    "ソ": "A single <b>sew</b>n stitch — the stroke drops DOWN ↓.",
    "タ": "A name <b>ta</b>g with a diagonal slash.",
    "チ": "A <b>chee</b>rleader — キ with the top lopped off.",
    "ツ": "A <b>tsu</b>nami — the strokes sweep gently UP ↗.",
    "テ": "A <b>te</b>legraph pole with two cross-wires.",
    "ト": "A <b>toe</b> sticking out from a post.",
    "ナ": "A folded <b>na</b>pkin — one clean cross.",
    "ニ": "Two lines — 二 means “two”, read <b>ni</b>.",
    "ヌ": "<b>Noo</b>dles speared by a crossed fork.",
    "ネ": "A fishing <b>ne</b>t hung on a pole.",
    "ノ": "A single <b>no</b> slash — the simplest stroke.",
    "ハ": "Two legs spread wide — a <b>ha</b>ppy stance.",
    "ヒ": "The <b>hee</b>l of a boot.",
    "フ": "A single hooked slope — Mount <b>Fu</b>ji again.",
    "ヘ": "Identical to hiragana へ — a <b>he</b>adland hill.",
    "ホ": "A <b>ho</b>me TV antenna on a cross-mast.",
    "マ": "A <b>ma</b>rker’s tick — a quick check.",
    "ミ": "Three whiskers — “<b>mee</b>”, like 三 (three).",
    "ム": "A cow’s pointed snout going “<b>moo</b>”.",
    "メ": "A crossed X — “<b>me</b>”, two eyes shut tight.",
    "モ": "A fishing pole bent to catch <b>mo</b>re.",
    "ヤ": "A <b>ya</b>cht’s mast and sail.",
    "ユ": "A <b>U</b>-shaped tray you say “yu” into.",
    "ヨ": "A comb with three teeth — a <b>yo</b>-yo’s ridges.",
    "ラ": "A <b>ra</b>bbit’s ear flopping over.",
    "リ": "Two drips again — katakana “<b>ree</b>”.",
    "ル": "A figure with <b>loo</b>ping running legs.",
    "レ": "A single <b>re</b>laxed lean.",
    "ロ": "A plain square <b>roo</b>m.",
    "ワ": "An open mouth at a <b>wa</b>terfall.",
    "ヲ": "A three-stroke “<b>wo</b>” — almost never written today. <b>Sounds exactly like オ</b>.",
    "ン": "A short up-flick ↗ — compare ソ, which flicks down.",
}

# Sound notes for the tricky kana (common L1 interference points for European learners)
NOTE = {
    "う": "Unrounded [ɯ] — keep lips relaxed, don’t push them forward.",
    "し": "[ɕi] — softer and more whistled than English “she”.",
    "す": "Often devoiced to a near-silent “s” at the end of words.",
    "ち": "[tɕi] — like the “chee” in “cheese”.",
    "つ": "[tsɐ] — the “ts” in “cats”, then a relaxed “u”.",
    "ふ": "[ɸɐ] — a soft bilabial blow, halfway between “f” and “h”.",
    "ら": "Tapped [ɾ] — closer to a quick “d” than an English “r”.",
    "り": "Tapped [ɾ] — a light flick of the tongue, never trilled.",
    "る": "Tapped [ɾ] — a light flick of the tongue, never trilled.",
    "れ": "Tapped [ɾ] — a light flick of the tongue, never trilled.",
    "ろ": "Tapped [ɾ] — a light flick of the tongue, never trilled.",
    "を": "Pronounced exactly like お — used only as the object particle.",
    "ぢ": "Pronounced exactly like じ in modern Japanese. The spelling survives in a few words (e.g. 鼻血 はなぢ \"nosebleed\"); otherwise always written じ.",
    "づ": "Pronounced exactly like ず in modern Japanese. The spelling survives in compounds where two morphemes meet (e.g. 三日月 みかづき \"crescent moon\"); otherwise always written ず.",
    "ヂ": "Pronounced exactly like ジ. Effectively never appears in modern katakana — included only for completeness.",
    "ヅ": "Pronounced exactly like ズ. Effectively never appears in modern katakana — included only for completeness.",
    "ヲ": "Pronounced exactly like オ. Effectively never appears in modern katakana — included only for completeness.",
    "ん": "A full mora [ɴ/n/m]; its sound shifts to match the next consonant.",
    "へ": "As the direction particle it is pronounced “e”, not “he”.",
    "は": "As the topic particle it is pronounced “wa”, not “ha”.",
}

# Homophones — kana with identical pronunciation. Rendered as a small "=X"
# badge in the chart and a strongly-worded NOTE in the detail drawer.
SAME_AS = {
    "ぢ": "じ", "づ": "ず", "を": "お",
    "ヂ": "ジ", "ヅ": "ズ", "ヲ": "オ",
}

# Look-alike clusters — easily confused shapes
LOOKALIKE_GROUPS = [
    ["あ", "お"], ["ぬ", "め"], ["ね", "れ", "わ"], ["は", "ほ", "ま"],
    ["き", "さ"], ["け", "は"], ["る", "ろ"], ["い", "り"],
    ["し", "つ", "ち"], ["そ", "ろ"], ["す", "む"],
    ["シ", "ツ"], ["ソ", "ン"], ["ソ", "リ"], ["ク", "ワ", "ウ"],
    ["ク", "タ"], ["コ", "ユ"], ["ノ", "メ", "ヌ", "ス"], ["レ", "ル"],
    ["ナ", "メ"], ["セ", "ヤ"], ["マ", "ム"], ["ニ", "ミ"],
    ["ホ", "ネ"], ["フ", "ワ"], ["ア", "マ"], ["テ", "チ"],
]


def lookalikes(ch):
    out = []
    for grp in LOOKALIKE_GROUPS:
        if ch in grp:
            out += [c for c in grp if c != ch]
    seen, uniq = set(), []
    for c in out:
        if c not in seen:
            seen.add(c)
            uniq.append(c)
    return uniq


def script_of(ch):
    return "hiragana" if "぀" <= ch[0] <= "ゟ" else "katakana"


def build_meta(strokes):
    meta = {}
    all_rows = (HIRA_BASE + HIRA_DAKU + HIRA_YOON +
                KATA_BASE + KATA_DAKU + KATA_YOON)
    for _label, cells in all_rows:
        for ch in cells:
            if ch is None or ch in meta:
                continue
            kind = "yoon" if len(ch) > 1 else (
                "base" if ch in MNEMONIC else "modified")
            # mnemonic
            if ch in MNEMONIC:
                mn = MNEMONIC[ch]
            elif kind == "yoon":
                big, small = ch[0], ch[1]
                mn = ("<b>%s</b> + small <b>%s</b> — blended into a single "
                      "beat: “%s”.") % (big, small, ROMAJI[ch])
            else:  # dakuten / handakuten
                if ROMAJI[ch][0] == "p":
                    mark, sign = "handakuten", "゜"
                else:
                    mark, sign = "dakuten", "゛"
                mn = ("A base kana + the <b>%s</b> mark “%s” — it switches "
                      "the consonant to “%s”.") % (mark, sign, ROMAJI[ch])
            meta[ch] = {
                "r": ROMAJI[ch],
                "m": mn,
                "look": lookalikes(ch),
                "note": NOTE.get(ch, ""),
                "kind": kind,
                "script": script_of(ch),
                "strokes": strokes.get(ch, []),
                "same_as": SAME_AS.get(ch, ""),
            }
    return meta


def section(title, jp, cols, rows):
    return {"title": title, "jp": jp, "cols": cols,
            "rows": [{"label": lbl, "cells": cells} for lbl, cells in rows]}


def main():
    if not os.path.exists(STROKE_PATH):
        sys.exit("missing stroke data: %s" % STROKE_PATH)
    with open(STROKE_PATH, encoding="utf-8") as f:
        strokes = json.load(f)

    data = {
        "scripts": {
            "hiragana": {
                "label": "Hiragana",
                "jp": "ひらがな",
                "sections": [
                    section("Basic", "五十音",
                            ["a", "i", "u", "e", "o"], HIRA_BASE),
                    section("Dakuten & Handakuten",
                            "゙ ゜", ["a", "i", "u", "e", "o"],
                            HIRA_DAKU),
                    section("Combinations", "拗音",
                            ["ya", "yu", "yo"], HIRA_YOON),
                ],
            },
            "katakana": {
                "label": "Katakana",
                "jp": "カタカナ",
                "sections": [
                    section("Basic", "五十音",
                            ["a", "i", "u", "e", "o"], KATA_BASE),
                    section("Dakuten & Handakuten",
                            "゙ ゜", ["a", "i", "u", "e", "o"],
                            KATA_DAKU),
                    section("Combinations", "拗音",
                            ["ya", "yu", "yo"], KATA_YOON),
                ],
            },
        },
        "meta": build_meta(strokes),
    }

    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    html = TEMPLATE.replace("/*__DATA__*/", blob)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    kb = len(html.encode("utf-8")) / 1024
    print("wrote %s  (%.0f KB, %d kana)" %
          (os.path.relpath(OUT_PATH, ROOT), kb, len(data["meta"])))


# --------------------------------------------------------------------------
# HTML template — single self-contained file. /*__DATA__*/ is the only
# injection point (the kana dataset as JSON).
# --------------------------------------------------------------------------
TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Kana Guide — かな</title>
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Noto+Sans+JP:wght@400;500;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --paper:#f1e8d6; --paper-2:#e9dcc2; --ink:#2b2620; --ink-soft:#6f6557;
  --vermilion:#bd3b2c; --vermilion-deep:#9c2f23; --gold:#b08a4a;
  --cell:#f7f0e0; --cell-line:#d8c8a6; --good:#5c7148;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{
  background:var(--paper); color:var(--ink);
  font-family:"Fraunces",Georgia,serif;
  font-optical-sizing:auto;
  -webkit-font-smoothing:antialiased;
  background-image:
    radial-gradient(circle at 18% 12%, rgba(255,255,255,.45), transparent 42%),
    radial-gradient(circle at 86% 88%, rgba(157,47,35,.06), transparent 46%),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/></filter><rect width='100%25' height='100%25' filter='url(%23n)' opacity='0.035'/></svg>");
  min-height:100%;
}
.jp{font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic","Meiryo",sans-serif;font-feature-settings:"palt"}

/* ---- shell ---- */
.wrap{max-width:1080px;margin:0 auto;padding:46px 28px 90px}
header{position:relative;text-align:center;padding-bottom:26px;margin-bottom:8px}
header::after{content:"";position:absolute;left:50%;bottom:0;transform:translateX(-50%);
  width:64px;height:2px;background:var(--vermilion)}
.kicker{font-size:12px;letter-spacing:.42em;text-transform:uppercase;
  color:var(--ink-soft);font-weight:600}
h1.title{font-size:84px;line-height:.96;font-weight:800;letter-spacing:.06em;
  margin:8px 0 4px;color:var(--ink)}
h1.title .seal{color:var(--vermilion)}
.subtitle{font-style:italic;font-size:16px;color:var(--ink-soft)}

/* ---- search ---- */
.search{position:relative;max-width:560px;margin:28px auto 0;width:100%}
.search-input{
  width:100%;display:block;background:var(--cell);
  border:1.5px solid var(--cell-line);border-radius:9px;
  padding:13px 16px 13px 44px;color:var(--ink);
  font-family:"Fraunces",Georgia,serif;font-size:15px;
  transition:border-color .14s ease, box-shadow .14s ease, background .14s ease;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='%236f6557' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'><circle cx='11' cy='11' r='7'/><path d='m21 21-4.3-4.3'/></svg>");
  background-repeat:no-repeat;background-position:14px center;background-size:18px;
}
.search-input:focus{outline:none;background:#fff;
  border-color:var(--vermilion);box-shadow:0 0 0 3px rgba(189,59,44,.12)}
.search-input::placeholder{color:var(--ink-soft);font-style:italic}
.search-results{
  position:absolute;top:calc(100% + 8px);left:0;right:0;z-index:30;
  background:#fff;border:1px solid var(--cell-line);border-radius:9px;
  padding:13px 14px;display:none;
  box-shadow:0 14px 36px -18px rgba(43,38,32,.45)}
.search-results.on{display:block}
.search-hint{font-size:11.5px;color:var(--ink-soft);font-style:italic;
  margin-bottom:9px;line-height:1.45}
.search-hint b{color:var(--ink);font-style:normal;font-weight:600}
.search-row{display:flex;flex-wrap:wrap;gap:6px}
.search-group{display:inline-flex;align-items:center;gap:3px;
  background:var(--cell);border:1px solid var(--cell-line);border-radius:7px;
  padding:5px 8px}
.search-group.homo{border-color:var(--gold)}
.search-romaji{font-size:10.5px;font-weight:700;color:var(--ink-soft);
  letter-spacing:.7px;text-transform:uppercase;margin-right:3px}
.search-kana{
  font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;
  font-size:24px;line-height:1;font-weight:500;color:var(--ink);
  padding:2px 6px;cursor:pointer;border-radius:4px;
  transition:background .12s ease, color .12s ease, transform .12s ease}
.search-kana:hover{background:var(--vermilion);color:#fff;transform:translateY(-1px)}
.search-kana.unknown{color:var(--vermilion-deep);opacity:.45;font-style:italic;
  cursor:default;font-family:"Fraunces",serif;font-size:18px}
.search-kana.unknown:hover{background:transparent;color:var(--vermilion-deep);transform:none}
.search-empty{font-size:13px;color:var(--ink-soft);text-align:center;
  padding:8px 4px;font-style:italic}

/* ---- tabs ---- */
nav.tabs{display:flex;justify-content:center;gap:6px;margin:30px 0 8px;flex-wrap:wrap}
.tab{font-family:"Fraunces",serif;font-size:15px;font-weight:600;
  background:none;border:none;cursor:pointer;color:var(--ink-soft);
  padding:9px 20px 11px;border-radius:3px;position:relative;letter-spacing:.02em}
.tab .tab-jp{font-size:12px;display:block;margin-top:1px;letter-spacing:.14em}
.tab:hover{color:var(--ink)}
.tab.on{color:var(--ink)}
.tab.on::after{content:"";position:absolute;left:18px;right:18px;bottom:3px;
  height:2px;background:var(--vermilion)}

/* ---- chart ---- */
.panel{display:none;animation:rise .5s ease both}
.panel.on{display:block}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.sec{margin-top:34px}
.sec-head{display:flex;align-items:baseline;gap:12px;margin-bottom:14px;
  padding-bottom:7px;border-bottom:1px solid var(--cell-line)}
.sec-head h2{font-size:21px;font-weight:600}
.sec-head .sec-jp{font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;color:var(--vermilion);
  font-size:16px;letter-spacing:.16em}
.sec-head .sec-hint{margin-left:auto;font-size:12.5px;font-style:italic;
  color:var(--ink-soft)}
.grid{display:grid;gap:7px}
.colhead,.rowlab{font-size:11px;font-weight:700;letter-spacing:.12em;
  text-transform:uppercase;color:var(--ink-soft);
  display:flex;align-items:center;justify-content:center}
.rowlab{justify-content:flex-end;padding-right:6px}
.cell{
  position:relative;background:var(--cell);border:1px solid var(--cell-line);
  border-radius:5px;cursor:pointer;padding:9px 4px 7px;text-align:center;
  transition:transform .14s ease,background .14s ease,border-color .14s ease,
    box-shadow .14s ease;
  opacity:0;animation:pop .42s ease forwards}
@keyframes pop{to{opacity:1}}
.cell .k{font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;font-size:30px;font-weight:500;
  line-height:1;color:var(--ink);display:block}
.cell .ro{font-size:10.5px;color:var(--ink-soft);margin-top:5px;
  letter-spacing:.04em;font-style:italic}
.cell:hover{transform:translateY(-3px);background:#fff;
  border-color:var(--vermilion);box-shadow:0 8px 18px -10px rgba(43,38,32,.5)}
.cell:hover .k{color:var(--vermilion-deep)}
.cell.empty{background:transparent;border:1px dashed #d3c4a3;cursor:default;
  animation:none;opacity:.5}
.cell.empty:hover{transform:none;box-shadow:none;border-color:#d3c4a3}
.cell.yoon .k{font-size:23px}
.cell.homophone{border-color:var(--gold);border-width:1.4px}
.cell.homophone:hover{border-color:var(--vermilion)}
.cell .eq{position:absolute;top:3px;right:4px;font-size:10px;line-height:1;
  font-weight:700;color:var(--vermilion);opacity:.78;letter-spacing:.3px;
  background:rgba(253,246,230,.85);padding:2px 4px;border-radius:3px}
.cell.homophone:hover .eq{color:var(--vermilion-deep);opacity:1}

/* ---- detail drawer ---- */
.scrim{position:fixed;inset:0;background:rgba(35,30,24,.34);opacity:0;
  pointer-events:none;transition:opacity .28s ease;z-index:40}
.scrim.on{opacity:1;pointer-events:auto}
.drawer{position:fixed;top:0;right:0;height:100%;width:430px;max-width:92vw;
  background:var(--paper);z-index:50;transform:translateX(102%);
  transition:transform .34s cubic-bezier(.4,.05,.2,1);
  box-shadow:-18px 0 50px -28px rgba(43,38,32,.7);
  border-left:3px solid var(--vermilion);
  display:flex;flex-direction:column}
.drawer.on{transform:none}
.drawer-scroll{overflow-y:auto;padding:22px 30px 36px}
.d-top{display:flex;align-items:center;justify-content:space-between}
.d-nav{display:flex;gap:4px}
.icon-btn{background:none;border:1px solid var(--cell-line);border-radius:4px;
  width:34px;height:34px;cursor:pointer;color:var(--ink-soft);font-size:16px;
  display:flex;align-items:center;justify-content:center;
  transition:all .14s ease;font-family:"Fraunces",serif}
.icon-btn:hover{border-color:var(--vermilion);color:var(--vermilion);
  background:#fff}
.d-hero{text-align:center;margin:10px 0 4px}
.d-hero .big{font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;font-size:108px;
  font-weight:500;line-height:1;color:var(--ink)}
.d-hero .ro{font-size:24px;font-style:italic;color:var(--vermilion-deep);
  margin-top:2px}
.d-hero .kindtag{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;
  color:var(--ink-soft);margin-top:5px}
.d-same-as{font-family:"Fraunces",serif;font-size:15px;font-weight:600;
  color:var(--vermilion-deep);margin-top:6px;letter-spacing:.02em}
.d-same-as .jp{font-size:22px;vertical-align:-3px;margin:0 2px;font-weight:500}
.d-same-as small{font-size:11px;font-weight:500;font-style:italic;
  color:var(--ink-soft);letter-spacing:0;margin-left:4px}
.play{margin:14px auto 4px;display:flex;align-items:center;gap:9px;
  background:var(--vermilion);color:#fdf6e6;border:none;cursor:pointer;
  font-family:"Fraunces",serif;font-size:14px;font-weight:600;
  padding:10px 22px;border-radius:30px;transition:all .15s ease;
  box-shadow:0 6px 16px -8px rgba(157,47,35,.9)}
.play:hover{background:var(--vermilion-deep);transform:translateY(-1px)}
.play:active{transform:translateY(1px)}
.play .tri{font-size:11px}

/* stroke panel — manuscript square */
.stroke-wrap{margin:20px 0 6px}
.label{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-soft);margin-bottom:9px;display:flex;align-items:center;gap:8px}
.label::after{content:"";flex:1;height:1px;background:var(--cell-line)}
.genkou{width:204px;height:204px;margin:0 auto;background:#fbf6e9;
  border:1.5px solid var(--cell-line);border-radius:4px;position:relative}
.genkou svg{display:block;width:100%;height:100%}
.guide{stroke:#e3d4b1;stroke-width:1;stroke-dasharray:4 4}
.ghost{fill:none;stroke:#e0d3b4;stroke-width:5.5;stroke-linecap:round;
  stroke-linejoin:round}
.live{fill:none;stroke:var(--vermilion);stroke-width:6;stroke-linecap:round;
  stroke-linejoin:round}
.snum{font-family:"Fraunces",serif;font-size:8px;fill:#fff;font-weight:700}
.snum-bg{fill:var(--vermilion-deep)}
.stroke-row{display:flex;align-items:center;justify-content:center;gap:14px;
  margin-top:10px}
.stroke-count{font-size:13px;color:var(--ink-soft);font-style:italic}
.replay{background:none;border:none;cursor:pointer;color:var(--vermilion);
  font-family:"Fraunces",serif;font-size:13px;font-weight:600;
  display:flex;align-items:center;gap:5px}
.replay:hover{color:var(--vermilion-deep)}

.card{background:var(--cell);border:1px solid var(--cell-line);
  border-radius:6px;padding:14px 16px;margin-top:18px}
.card.mnem{border-left:3px solid var(--gold)}
.card.note{border-left:3px solid var(--vermilion)}
.card h3{font-size:12px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink-soft);margin-bottom:6px;font-weight:700}
.card p{font-size:15px;line-height:1.5}
.card p b{color:var(--vermilion-deep);font-weight:700}
.look{display:flex;gap:8px;flex-wrap:wrap;margin-top:9px}
.look .lk{font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;font-size:26px;font-weight:500;
  background:#fbf6e9;border:1px solid var(--cell-line);border-radius:5px;
  width:46px;height:46px;display:flex;align-items:center;justify-content:center;
  cursor:pointer;transition:all .14s ease;color:var(--ink)}
.look .lk:hover{border-color:var(--vermilion);color:var(--vermilion);
  transform:translateY(-2px)}

/* ---- quiz ---- */
.quiz{max-width:560px;margin:34px auto 0}
.quiz-setup{text-align:center}
.q-group{margin:20px 0}
.q-group .label{justify-content:center}
.q-group .label::after,.q-group .label::before{content:"";flex:1;height:1px;
  background:var(--cell-line)}
.chip-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.chip{font-family:"Fraunces",serif;font-size:13.5px;font-weight:600;
  background:var(--cell);border:1px solid var(--cell-line);border-radius:30px;
  padding:8px 17px;cursor:pointer;color:var(--ink-soft);transition:all .14s ease}
.chip:hover{border-color:var(--vermilion);color:var(--ink)}
.chip.on{background:var(--vermilion);color:#fdf6e6;border-color:var(--vermilion)}
.start{margin:26px auto 0;display:block;background:var(--ink);color:var(--paper);
  border:none;cursor:pointer;font-family:"Fraunces",serif;font-size:16px;
  font-weight:600;padding:13px 40px;border-radius:4px;letter-spacing:.03em;
  transition:all .15s ease}
.start:hover{background:var(--vermilion-deep)}
.quiz-live{display:none}
.quiz-live.on{display:block}
.scorebar{display:flex;justify-content:space-between;font-size:13px;
  color:var(--ink-soft);font-style:italic;margin-bottom:14px}
.scorebar b{font-style:normal;color:var(--vermilion-deep);font-weight:700}
.prompt{background:var(--cell);border:1px solid var(--cell-line);
  border-radius:8px;padding:34px 20px;text-align:center;margin-bottom:16px}
.prompt .ask{font-size:12px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--ink-soft);margin-bottom:12px}
.prompt .big-q{font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;font-size:88px;
  font-weight:500;line-height:1;color:var(--ink)}
.prompt .big-q.romaji{font-family:"Fraunces",serif;font-style:italic;
  font-size:62px;color:var(--vermilion-deep)}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.opt{background:var(--cell);border:1.5px solid var(--cell-line);
  border-radius:7px;padding:18px 8px;cursor:pointer;text-align:center;
  transition:all .13s ease;font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic",sans-serif;
  font-size:34px;font-weight:500;color:var(--ink)}
.opt.romaji{font-family:"Fraunces",serif;font-style:italic;font-size:24px;font-weight:700}
.opt:hover{border-color:var(--vermilion);transform:translateY(-2px)}
.opt.correct{background:var(--good);border-color:var(--good);color:#fff}
.opt.wrong{background:var(--vermilion);border-color:var(--vermilion);
  color:#fff;animation:shake .34s}
.opt.dim{opacity:.4;pointer-events:none}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-7px)}
  75%{transform:translateX(7px)}}
.q-foot{text-align:center;margin-top:16px;min-height:30px}
.q-next{background:none;border:1px solid var(--cell-line);cursor:pointer;
  font-family:"Fraunces",serif;font-size:14px;font-weight:600;color:var(--ink);
  padding:9px 26px;border-radius:4px}
.q-next:hover{border-color:var(--vermilion);color:var(--vermilion-deep)}
.q-quit{display:block;margin:14px auto 0;background:none;border:none;
  color:var(--ink-soft);cursor:pointer;font-family:"Fraunces",serif;
  font-size:12.5px;font-style:italic;text-decoration:underline}

footer{text-align:center;margin-top:60px;font-size:11.5px;color:var(--ink-soft);
  line-height:1.7}
footer a{color:var(--ink-soft)}
.audio-warn{display:none;text-align:center;font-size:12px;font-style:italic;
  color:var(--vermilion-deep);margin-top:6px}

@media(max-width:560px){
  h1.title{font-size:58px}
  .wrap{padding:32px 14px 70px}
  .cell .k{font-size:25px}
  .opts{grid-template-columns:1fr 1fr}
}

.site-nav{position:sticky;top:0;z-index:100;background:rgba(241,232,214,.92);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--cell-line)}
.site-nav-inner{max-width:1100px;margin:0 auto;padding:10px 22px;display:flex;gap:18px;flex-wrap:wrap;align-items:center;font-family:"Fraunces",Georgia,serif;font-size:13.5px;font-weight:600;letter-spacing:.04em}
.site-nav a{color:var(--ink-soft);text-decoration:none;padding:4px 0;border-bottom:2px solid transparent;transition:color .12s,border-color .12s}
.site-nav a:hover{color:var(--vermilion-deep)}
.site-nav a.active{color:var(--vermilion);border-bottom-color:var(--vermilion)}
.site-nav .nav-brand{color:var(--ink);letter-spacing:.18em;text-transform:uppercase;font-size:11px;margin-right:6px}
@media print{.site-nav{display:none}}
</style>
</head>
<body>
<nav class="site-nav">
  <div class="site-nav-inner">
    <span class="nav-brand">japan-learning</span>
    <a href="/">Home</a>
    <a href="/#curriculum">Curriculum</a>
    <a href="/kana/" class="active">Kana</a>
    <a href="/chart/">Chart</a>
    <a href="/dict/">Dictionary</a>
    <a href="/numbers/">Numbers</a>
  </div>
</nav>
<div class="wrap">
  <header>
    <div class="kicker">Module 00 &middot; Writing Systems</div>
    <h1 class="title jp">か<span class="seal">な</span></h1>
    <div class="subtitle">The Kana Guide &mdash; hiragana &amp; katakana, stroke by stroke</div>
  </header>

  <div class="search">
    <input type="text" id="searchInput" class="search-input"
           placeholder="Search romaji or a name — e.g. shi · kya · ruisu · konnichiwa"
           autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
    <div class="search-results" id="searchResults"></div>
  </div>

  <nav class="tabs" id="tabs">
    <button class="tab on" data-view="hiragana">Hiragana<span class="tab-jp jp">ひらがな</span></button>
    <button class="tab" data-view="katakana">Katakana<span class="tab-jp jp">カタカナ</span></button>
    <button class="tab" data-view="quiz">Practice<span class="tab-jp jp">クイズ</span></button>
  </nav>

  <div class="panel on" id="panel-hiragana"></div>
  <div class="panel" id="panel-katakana"></div>

  <div class="panel" id="panel-quiz">
    <div class="quiz">
      <div class="quiz-setup" id="quizSetup">
        <div class="q-group">
          <div class="label">Mode</div>
          <div class="chip-row" id="qMode">
            <button class="chip on" data-mode="recognise">See kana &rarr; pick sound</button>
            <button class="chip" data-mode="recall">See sound &rarr; pick kana</button>
            <button class="chip" data-mode="lookalike">Look-alike trap</button>
          </div>
        </div>
        <div class="q-group">
          <div class="label">Set</div>
          <div class="chip-row" id="qSet">
            <button class="chip on" data-set="hiragana">Hiragana</button>
            <button class="chip" data-set="katakana">Katakana</button>
            <button class="chip" data-set="both">Both</button>
          </div>
        </div>
        <button class="start" id="qStart">Begin practice</button>
      </div>
      <div class="quiz-live" id="quizLive">
        <div class="scorebar">
          <span>Streak <b id="qStreak">0</b></span>
          <span><b id="qScore">0</b> / <span id="qTotal">0</span> correct</span>
        </div>
        <div class="prompt" id="qPrompt"></div>
        <div class="opts" id="qOpts"></div>
        <div class="q-foot" id="qFoot"></div>
        <button class="q-quit" id="qQuit">end session</button>
      </div>
    </div>
  </div>

  <footer>
    Stroke-order data from <a href="https://kanjivg.tagaini.net/" target="_blank" rel="noopener">KanjiVG</a>
    &copy; Ulrich Apel, CC BY-SA 3.0. Audio uses your browser&rsquo;s Japanese voice.<br>
    Built for the japan-learning curriculum &mdash; Module 00.
    <div class="audio-warn" id="audioWarn">No Japanese voice found in this browser &mdash; audio is unavailable.</div>
  </footer>
</div>

<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-scroll" id="drawerBody"></div>
</aside>

<script>
const DATA = /*__DATA__*/;
const META = DATA.meta;

/* ---------- chart rendering ---------- */
function renderScript(name){
  const s = DATA.scripts[name];
  const root = document.getElementById('panel-'+name);
  let html = '';
  let cellIndex = 0;
  s.sections.forEach(sec=>{
    const ncol = sec.cols.length;
    html += '<div class="sec">';
    html += '<div class="sec-head"><h2>'+sec.title+'</h2>'+
            '<span class="sec-jp jp">'+sec.jp+'</span>'+
            '<span class="sec-hint">tap any kana for stroke order, sound &amp; a mnemonic</span></div>';
    html += '<div class="grid" style="grid-template-columns:34px repeat('+ncol+',1fr)">';
    html += '<div class="colhead"></div>';
    sec.cols.forEach(c=> html += '<div class="colhead">'+c+'</div>');
    sec.rows.forEach(row=>{
      html += '<div class="rowlab">'+(row.label||'&middot;')+'</div>';
      row.cells.forEach(ch=>{
        if(!ch){ html += '<div class="cell empty"></div>'; return; }
        const m = META[ch];
        const delay = (cellIndex++ * 11);
        const yoon = ch.length>1 ? ' yoon' : '';
        const homo = m.same_as ? ' homophone' : '';
        const eq = m.same_as ? '<span class="eq jp">=' + m.same_as + '</span>' : '';
        html += '<div class="cell'+yoon+homo+'" data-k="'+ch+'" style="animation-delay:'+delay+'ms">'+
                '<span class="k jp">'+ch+'</span>'+
                '<span class="ro">'+m.r+'</span>'+
                eq+
                '</div>';
      });
    });
    html += '</div></div>';
  });
  root.innerHTML = html;
  root.querySelectorAll('.cell[data-k]').forEach(el=>{
    el.addEventListener('click',()=>openDetail(el.dataset.k));
  });
}
renderScript('hiragana');
renderScript('katakana');

/* ---------- ordered nav list (for drawer prev/next) ---------- */
function navList(script){
  const out=[];
  DATA.scripts[script].sections.forEach(sec=>{
    sec.rows.forEach(r=> r.cells.forEach(c=>{ if(c) out.push(c); }));
  });
  return out;
}

/* ---------- tabs ---------- */
let currentView='hiragana';
document.querySelectorAll('.tab').forEach(t=>{
  t.addEventListener('click',()=>{
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
    t.classList.add('on');
    const v=t.dataset.view; currentView=v;
    ['hiragana','katakana','quiz'].forEach(p=>{
      document.getElementById('panel-'+p).classList.toggle('on',p===v);
    });
  });
});

/* ---------- audio ---------- */
let jaVoice=null;
function loadVoices(){
  const vs=speechSynthesis.getVoices();
  jaVoice=vs.find(v=>v.lang==='ja-JP')||vs.find(v=>v.lang&&v.lang.toLowerCase().indexOf('ja')===0)||null;
  if(!jaVoice && vs.length){
    document.getElementById('audioWarn').style.display='block';
  }
}
if('speechSynthesis' in window){
  loadVoices();
  speechSynthesis.onvoiceschanged=loadVoices;
}else{
  document.getElementById('audioWarn').style.display='block';
}
let _lastSpeakAt = 0;
function speak(text){
  if(!('speechSynthesis' in window)) return;
  // Debounce: ignore calls within 250ms of the previous (kills any
  // accidental double-fire from listeners / re-render races).
  const now = Date.now();
  if (now - _lastSpeakAt < 250) return;
  _lastSpeakAt = now;
  // Chrome's cancel() is async — give it a tick to flush the queue
  // before queuing the new utterance, or any buffered remnant of the
  // previous one plays out as a "ghost" second sound.
  speechSynthesis.cancel();
  setTimeout(() => {
    const u = new SpeechSynthesisUtterance(text);
    u.lang  = 'ja-JP';
    u.rate  = 0.55;
    u.pitch = 1;
    u.volume = 1;
    if(jaVoice) u.voice = jaVoice;
    speechSynthesis.speak(u);
  }, 60);
}

/* ---------- stroke animation ---------- */
function animateStrokes(container){
  const live=container.querySelectorAll('path.live');
  let t=0;
  live.forEach(p=>{
    const len=p.getTotalLength();
    p.style.transition='none';
    p.style.strokeDasharray=len;
    p.style.strokeDashoffset=len;
    const dur=Math.max(320,Math.min(900,len*7));
    p.getBoundingClientRect();
    setTimeout(()=>{
      p.style.transition='stroke-dashoffset '+dur+'ms ease';
      p.style.strokeDashoffset='0';
    },t);
    t+=dur+120;
  });
}
function strokeSVG(strokes){
  if(!strokes||!strokes.length){
    return '<div class="stroke-count">No stroke data for this combination &mdash; '+
           'see its component kana below.</div>';
  }
  let paths='', nums='';
  strokes.forEach((d,i)=>{
    paths+='<path class="ghost" d="'+d+'"/>';
  });
  let live='';
  strokes.forEach((d,i)=>{ live+='<path class="live" d="'+d+'"/>'; });
  // stroke-start number badges
  strokes.forEach((d,i)=>{
    const m=d.match(/M\s*([-\d.]+)[,\s]+([-\d.]+)/);
    if(m){
      const x=parseFloat(m[1]), y=parseFloat(m[2]);
      nums+='<circle class="snum-bg" cx="'+x+'" cy="'+y+'" r="6.5"/>'+
            '<text class="snum" x="'+x+'" y="'+(y+2.8)+'" text-anchor="middle">'+(i+1)+'</text>';
    }
  });
  return '<div class="genkou"><svg viewBox="0 0 109 109">'+
    '<line class="guide" x1="54.5" y1="0" x2="54.5" y2="109"/>'+
    '<line class="guide" x1="0" y1="54.5" x2="109" y2="54.5"/>'+
    paths+live+nums+'</svg></div>';
}

/* ---------- detail drawer ---------- */
const drawer=document.getElementById('drawer');
const scrim=document.getElementById('scrim');
const drawerBody=document.getElementById('drawerBody');
let drawerKey=null;

function openDetail(ch){
  const m=META[ch];
  if(!m) return;
  drawerKey=ch;
  const kindLabel={base:'Basic kana',modified:'Dakuten / Handakuten',
    yoon:'Combination (yōon)'}[m.kind]||'';
  let html='';
  html+='<div class="d-top">'+
        '<div class="d-nav">'+
        '<button class="icon-btn" id="dPrev" title="Previous (←)">&lsaquo;</button>'+
        '<button class="icon-btn" id="dNext" title="Next (→)">&rsaquo;</button>'+
        '</div>'+
        '<button class="icon-btn" id="dClose" title="Close (Esc)">&times;</button></div>';
  const sameAsHero = m.same_as
    ? '<div class="d-same-as">sounds exactly like <span class="jp">'+m.same_as+
      '</span> <small>('+META[m.same_as].r+')</small></div>'
    : '';
  html+='<div class="d-hero"><div class="big jp">'+ch+'</div>'+
        '<div class="ro">'+m.r+'</div>'+
        sameAsHero+
        '<div class="kindtag">'+kindLabel+'</div></div>';
  html+='<button class="play" id="dPlay"><span class="tri">&#9654;</span> Hear it</button>';
  html+='<div class="stroke-wrap"><div class="label">Stroke order</div>'+
        strokeSVG(m.strokes);
  if(m.strokes&&m.strokes.length){
    html+='<div class="stroke-row"><span class="stroke-count">'+
          m.strokes.length+(m.strokes.length>1?' strokes':' stroke')+
          '</span><button class="replay" id="dReplay">&#8635; replay</button></div>';
  }
  html+='</div>';
  html+='<div class="card mnem"><h3>Mnemonic</h3><p>'+m.m+'</p></div>';
  if(m.note){
    html+='<div class="card note"><h3>Pronunciation</h3><p>'+m.note+'</p></div>';
  }
  if(m.look&&m.look.length){
    let chips='';
    m.look.forEach(c=> chips+='<div class="lk jp" data-lk="'+c+'">'+c+'</div>');
    html+='<div class="card"><h3>Easy to confuse with</h3>'+
          '<div class="look">'+chips+'</div></div>';
  }
  drawerBody.innerHTML=html;

  drawer.classList.add('on'); drawer.setAttribute('aria-hidden','false');
  scrim.classList.add('on');

  const svg=drawerBody.querySelector('.genkou');
  if(svg) animateStrokes(svg);

  document.getElementById('dClose').onclick=closeDetail;
  document.getElementById('dPlay').onclick=()=>speak(ch);
  const rep=document.getElementById('dReplay');
  if(rep) rep.onclick=()=>animateStrokes(drawerBody.querySelector('.genkou'));
  drawerBody.querySelectorAll('.lk').forEach(el=>{
    el.onclick=()=>openDetail(el.dataset.lk);
  });
  const list=navList(m.script);
  const idx=list.indexOf(ch);
  const prev=document.getElementById('dPrev');
  const next=document.getElementById('dNext');
  prev.onclick=()=>{ if(idx>0) openDetail(list[idx-1]); };
  next.onclick=()=>{ if(idx>=0&&idx<list.length-1) openDetail(list[idx+1]); };
  if(idx<=0) prev.style.visibility='hidden';
  if(idx>=list.length-1) next.style.visibility='hidden';
  speak(ch);
}
function closeDetail(){
  drawer.classList.remove('on'); drawer.setAttribute('aria-hidden','true');
  scrim.classList.remove('on'); drawerKey=null;
}
scrim.addEventListener('click',closeDetail);
document.addEventListener('keydown',e=>{
  if(!drawerKey) return;
  if(e.key==='Escape') closeDetail();
  if(e.key==='ArrowLeft'){const b=document.getElementById('dPrev');if(b&&b.style.visibility!=='hidden')b.click();}
  if(e.key==='ArrowRight'){const b=document.getElementById('dNext');if(b&&b.style.visibility!=='hidden')b.click();}
});

/* ---------- quiz ---------- */
let qMode='recognise', qSet='hiragana';
function bindChips(id,setter){
  document.getElementById(id).querySelectorAll('.chip').forEach(c=>{
    c.addEventListener('click',()=>{
      document.getElementById(id).querySelectorAll('.chip').forEach(x=>x.classList.remove('on'));
      c.classList.add('on'); setter(c);
    });
  });
}
bindChips('qMode',c=>qMode=c.dataset.mode);
bindChips('qSet',c=>qSet=c.dataset.set);

function quizPool(){
  let scripts = qSet==='both'?['hiragana','katakana']:[qSet];
  const pool=[];
  scripts.forEach(s=>{
    DATA.scripts[s].sections.forEach(sec=>{
      if(sec.title==='Combinations') return;       // single kana only
      sec.rows.forEach(r=> r.cells.forEach(c=>{ if(c) pool.push(c); }));
    });
  });
  return pool;
}
function sample(arr,n,exclude){
  const p=arr.filter(x=>x!==exclude);
  for(let i=p.length-1;i>0;i--){const j=Math.random()*(i+1)|0;[p[i],p[j]]=[p[j],p[i]];}
  return p.slice(0,n);
}
let qScore=0,qTotal=0,qStreak=0,qAnswered=false;

function newQuestion(){
  qAnswered=false;
  const pool=quizPool();
  const answer=pool[Math.random()*pool.length|0];
  const am=META[answer];
  let distractors;
  if(qMode==='lookalike' && am.look.length){
    distractors=am.look.slice();
    // top up if fewer than 3 look-alikes
    if(distractors.length<3){
      distractors=distractors.concat(sample(pool,3-distractors.length,answer));
    }
    distractors=distractors.slice(0,3);
  }else{
    distractors=sample(pool,3,answer);
  }
  const opts=[answer,...distractors];
  for(let i=opts.length-1;i>0;i--){const j=Math.random()*(i+1)|0;[opts[i],opts[j]]=[opts[j],opts[i]];}

  const showRomajiPrompt=(qMode==='recall');
  const prompt=document.getElementById('qPrompt');
  prompt.innerHTML='<div class="ask">'+
    (showRomajiPrompt?'Which kana makes this sound?':'What sound is this?')+
    '</div><div class="big-q '+(showRomajiPrompt?'romaji':'jp')+'">'+
    (showRomajiPrompt?am.r:answer)+'</div>';
  if(!showRomajiPrompt) speak(answer);

  const optsBox=document.getElementById('qOpts');
  optsBox.innerHTML='';
  opts.forEach(o=>{
    const el=document.createElement('div');
    const asRomaji=!showRomajiPrompt;       // options are romaji unless prompt is romaji
    el.className='opt'+(asRomaji?' romaji':' jp');
    el.textContent=asRomaji?META[o].r:o;
    el.dataset.k=o;
    el.addEventListener('click',()=>chooseAnswer(el,o,answer));
    optsBox.appendChild(el);
  });
  document.getElementById('qFoot').innerHTML='';
}
function chooseAnswer(el,chosen,answer){
  if(qAnswered) return;
  qAnswered=true; qTotal++;
  const correct=META[chosen].r===META[answer].r;
  const box=document.getElementById('qOpts');
  if(correct){
    el.classList.add('correct'); qScore++; qStreak++;
  }else{
    el.classList.add('wrong'); qStreak=0;
    box.querySelectorAll('.opt').forEach(o=>{
      if(META[o.dataset.k].r===META[answer].r) o.classList.add('correct');
    });
  }
  box.querySelectorAll('.opt').forEach(o=>{
    if(!o.classList.contains('correct')&&!o.classList.contains('wrong'))
      o.classList.add('dim');
  });
  speak(answer);
  document.getElementById('qScore').textContent=qScore;
  document.getElementById('qTotal').textContent=qTotal;
  document.getElementById('qStreak').textContent=qStreak;
  const foot=document.getElementById('qFoot');
  foot.innerHTML='<button class="q-next" id="qNext">Next &rarr;</button>';
  document.getElementById('qNext').onclick=newQuestion;
}
document.getElementById('qStart').addEventListener('click',()=>{
  qScore=0;qTotal=0;qStreak=0;
  document.getElementById('qScore').textContent='0';
  document.getElementById('qTotal').textContent='0';
  document.getElementById('qStreak').textContent='0';
  document.getElementById('quizSetup').style.display='none';
  document.getElementById('quizLive').classList.add('on');
  newQuestion();
});
document.getElementById('qQuit').addEventListener('click',()=>{
  document.getElementById('quizLive').classList.remove('on');
  document.getElementById('quizSetup').style.display='block';
});
document.addEventListener('keydown',e=>{
  if(!document.getElementById('quizLive').classList.contains('on')) return;
  if(['1','2','3','4'].includes(e.key)){
    const opts=document.querySelectorAll('#qOpts .opt');
    if(opts[+e.key-1]) opts[+e.key-1].click();
  }
  if(e.key==='Enter'){const n=document.getElementById('qNext');if(n)n.click();}
});

/* ---------- search ---------- */
// Reverse index: romaji "shi" → { hira: ["し"], kata: ["シ"] }. Homophones
// (ぢ/じ, づ/ず, を/お, …) appear together under the same key.
const ROMAJI_INDEX = (function(){
  const idx = {};
  // Process plain forms before homophone vestigials so the standard kana
  // appears first in the result list.
  const keys = Object.keys(META).sort((a,b)=>{
    const va = META[a].same_as ? 1 : 0;
    const vb = META[b].same_as ? 1 : 0;
    return va - vb;
  });
  keys.forEach(ch=>{
    const r = META[ch].r;
    if(!idx[r]) idx[r] = { hira: [], kata: [] };
    const slot = META[ch].script === 'hiragana' ? 'hira' : 'kata';
    idx[r][slot].push(ch);
  });
  return idx;
})();

// Light English → romaji preprocessing. Heuristics, not a true transliterator.
// Handles common patterns so e.g. "louis" → "ruisu" → ル イ ス.
function englishToRomaji(input){
  let s = (input||'').toLowerCase().trim().replace(/[^a-z]/g,'');
  if(!s) return '';
  // 1. Consonants Japanese lacks → closest Japanese consonant.
  s = s.replace(/l/g,'r').replace(/v/g,'b').replace(/x/g,'ks');
  // 2. English silent / aspirated 'h' between a vowel and a non-vowel — drop.
  //    "john" → "jon" → じょん. "sarah" → "sara" → さら.
  //    Preserves "shi", "chi", "ohio" (h between vowels stays).
  s = s.replace(/([aeiou])h(?![aeiou])/g,'$1');
  // 3. English vowel digraphs → single Japanese mora, BUT only when followed
  //    by another vowel (mid-word coalescence like Louis→Ruisu).
  //    At end of word, "ou" / "oo" represent Japanese long-ō / long-ū and
  //    must stay as two morae (arigatou → arigatō → ありがとう).
  s = s.replace(/ou(?=[aeiou])/g,'u').replace(/oo(?=[aeiou])/g,'u')
       .replace(/ee(?=[aeiou])/g,'i').replace(/ea(?=[aeiou])/g,'i');
  // 3. Insert "u" between consecutive consonants — but PRESERVE Japanese
  //    digraphs (sh, ch, ts, *y), geminates (kk, pp, tt, ss = sokuon),
  //    and the moraic 'n' which never takes a vowel.
  const keepPair = (a, b) => {
    if(/^(sh|ch|ts)$/.test(a+b)) return true;   // sibilant digraphs
    if(b === 'y') return true;                  // *y palatalisation
    if(a === b) return true;                    // geminate consonant
    return false;
  };
  // 'n' is excluded from the regex on both sides so e.g. "anna" stays "anna".
  for(let i=0;i<3;i++){
    s = s.replace(/([bcdfghjkmprstvwz])([bcdfghjkmprstvwz])/g,
                  (m,a,b) => keepPair(a,b) ? m : a+'u'+b);
  }
  // 4. Final stranded consonant → add a vowel. 'n' deliberately excluded —
  //    it's the standalone moraic ん.
  s = s.replace(/([td])$/,'$1o').replace(/([bcdfghjkmprsvwxz])$/,'$1u');
  return s;
}

function parseRomaji(input){
  const processed = englishToRomaji(input);
  const tokens = [];
  let i = 0;
  while(i < processed.length){
    let matched = false;
    for(const len of [3,2,1]){
      const chunk = processed.slice(i, i+len);
      if(ROMAJI_INDEX[chunk]){
        tokens.push(Object.assign({romaji: chunk}, ROMAJI_INDEX[chunk]));
        i += len;
        matched = true;
        break;
      }
    }
    if(!matched){
      tokens.push({romaji: processed[i], unknown: true});
      i += 1;
    }
  }
  return { processed, tokens };
}

function renderSearch(query){
  const panel = document.getElementById('searchResults');
  const raw = (query||'').trim();
  if(!raw){ panel.classList.remove('on'); panel.innerHTML=''; return; }

  const { processed, tokens } = parseRomaji(raw);
  const matched = tokens.filter(t=>!t.unknown);
  const allUnknown = tokens.length>0 && matched.length===0;

  if(allUnknown){
    panel.innerHTML = '<div class="search-empty">No kana for "'+raw+'". Try romaji — '+
                      '<b>shi</b>, <b>kya</b>, <b>ruisu</b>, <b>konnichiwa</b>.</div>';
    panel.classList.add('on'); return;
  }

  // Hint line — show preprocessing transformation when it changed the input.
  const rawNorm = raw.toLowerCase().replace(/[^a-z]/g,'');
  let html = '<div class="search-hint">';
  if(processed !== rawNorm){
    html += 'Heard as <b>'+processed+'</b> &middot; ';
  }
  html += matched.length + ' segment' + (matched.length===1?'':'s') +
          ' &middot; tap any kana for strokes &amp; sound';
  html += '</div>';

  html += '<div class="search-row">';
  tokens.forEach(t=>{
    if(t.unknown){
      html += '<div class="search-group"><span class="search-romaji">'+t.romaji+
              '</span><span class="search-kana unknown" title="no match">?</span></div>';
      return;
    }
    // Mark this segment as homophone-bearing if any of its kana are homophones
    const all = [].concat(t.hira||[], t.kata||[]);
    const isHomo = all.some(c => META[c] && META[c].same_as);
    html += '<div class="search-group'+(isHomo?' homo':'')+'">';
    html += '<span class="search-romaji">'+t.romaji+'</span>';
    (t.hira||[]).forEach(ch=>{
      html += '<span class="search-kana jp" data-k="'+ch+'" title="hiragana">'+ch+'</span>';
    });
    (t.kata||[]).forEach(ch=>{
      html += '<span class="search-kana jp" data-k="'+ch+'" title="katakana">'+ch+'</span>';
    });
    html += '</div>';
  });
  html += '</div>';

  panel.innerHTML = html;
  panel.classList.add('on');
  panel.querySelectorAll('.search-kana[data-k]').forEach(el=>{
    el.onclick = (e)=>{ e.stopPropagation(); openDetail(el.dataset.k); };
  });
}

const searchInput = document.getElementById('searchInput');
searchInput.addEventListener('input', e => renderSearch(e.target.value));
searchInput.addEventListener('keydown', e => {
  if(e.key === 'Escape'){
    searchInput.value = '';
    renderSearch('');
    searchInput.blur();
  }
});
// Dismiss panel on outside click
document.addEventListener('click', e => {
  const search = document.querySelector('.search');
  if(search && !search.contains(e.target)){
    document.getElementById('searchResults').classList.remove('on');
  }
});
// "/" anywhere focuses the search box
document.addEventListener('keydown', e => {
  if(e.key === '/' && document.activeElement !== searchInput &&
     !drawerKey && e.target.tagName !== 'INPUT'){
    e.preventDefault();
    searchInput.focus();
  }
});
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
