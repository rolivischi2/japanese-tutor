---
module: 00
file: 04-katakana-loanword-traps
lang_focus: writing
kanji_level: 0
last_updated: 2026-05-23
---

# Katakana — Loanword Traps

You can now decode every katakana symbol. But reading **loanwords** (*gairaigo*) needs three extra pieces: the long-vowel mark **ー**, the **extended foreign-sound combinations** (ファ, ティ, ウィ, ジェ …), and an understanding of *how Japanese reshapes a foreign word* so you can recognise the original underneath. That last point is the real "trap": a Japanese loanword often does **not** sound like the English/German word it came from, and guessing blindly leads you astray.

English and German loanwords in particular are a vocabulary gift — but only once you can decode them. This chapter is Day 14's content.

## 1. The long-vowel mark ー

In katakana, a long vowel is written with a single **horizontal bar ー** (the *chōonpu*), not by repeating a vowel kana the way hiragana does.

- Hiragana long vowel: spelled by adding a vowel kana — おかあさん, とうきょう.
- Katakana long vowel: spelled with ー — コーヒー, ケーキ, タクシー.

The bar means "hold the **preceding** vowel for one more mora". It counts as **one mora**. So:
- コーヒー = コ + ー + ヒ + ー = **four morae**. "coffee"
- ビール = ビ + ー + ル = **three morae**. "beer"
- ケーキ = ケ + ー + キ = **three morae**. "cake"

Caution — this is a length contrast. The bar is **never** silent and **never** optional. Reading コヒー as if it were コーヒー, or skipping the bar, changes the word's rhythm and can change the word. (If your L1 has phonemic vowel length — Hungarian, Finnish, Japanese-adjacent languages — this will feel natural; see `pronunciation/07-hungarian-transfer-notes.md`.) When the text runs **vertically**, the bar is drawn **vertically** — same meaning.

## 2. Extended katakana — foreign-sound combinations

The native gojūon cannot spell sounds Japanese does not have ("fa", "ti", "di", "wi", "she", "je" …). Katakana solves this by combining a base kana with a **small vowel kana** (ァ ィ ゥ ェ ォ) — the same shrinking trick as yōon, extended.

The high-value combinations to recognise:

| Combination | Sound | Built from | Example |
|---|---|---|---|
| ファ フィ フェ フォ | fa fi fe fo | フ + small vowel | フォーク "fork", ソファ "sofa" |
| ティ | ti | テ + small ィ | パーティー "party" |
| ディ | di | デ + small ィ | ディスク "disk" |
| トゥ ドゥ | tu du | ト/ド + small ゥ | タトゥー "tattoo" |
| ウィ ウェ ウォ | wi we wo | ウ + small vowel | ウィスキー "whisky", ウェブ "web" |
| ヴァ ヴィ ヴ ヴェ ヴォ | va vi vu ve vo | ウ + dakuten + small vowel | ヴァイオリン "violin" (often also written バイオリン) |
| シェ | she | シ + small ェ | シェフ "chef", ミルクシェイク "milkshake" |
| ジェ | je | ジ + small ェ | ジェット "jet", オレンジジュース |
| チェ | che | チ + small ェ | チェック "check", チェス "chess" |
| ツァ ツェ ツォ | tsa tse tso | ツ + small vowel | ピッツァ "pizza" |
| クォ | kwo | ク + small ォ | — (rarer) |

Two things to internalise:
- The small vowel **replaces** the base kana's own vowel: フ is [ɸɯ], フ + small ァ = [ɸa]. Same logic as きゃ.
- **ヴ** is the constructed "v". Japanese has no native [v], so many words use ヴ *or* fall back to the バ-row — バイオリン and ヴァイオリン are both seen. When you speak, [b] for ヴ is acceptable and common.

## 3. How Japanese reshapes foreign words — the real trap

Japanese phonology forces every loanword into Japanese-legal syllables. The result can look very different from the source. Knowing the **transformation rules** lets you recover the original — and is essential because the loanword frequently is **not** pronounced like the English word you know.

### Rule A — vowels get inserted to break up consonant clusters

Japanese syllables are (almost always) consonant + vowel. English consonant clusters and word-final consonants get a vowel — usually **ウ**, sometimes **オ** (after t/d) or **イ** — wedged in.

- "milk" → ミルク (mi-ru-ku) — *k* gains a ウ
- "strike" → ストライク (su-to-ra-i-ku) — three inserted vowels
- "bed" → ベッド (be-d-do) — final *d* gains an オ
- "Christmas" → クリスマス (ku-ri-su-ma-su)

This is why loanwords are often **longer** than the original: a one-syllable English word can become four or five morae.

### Rule B — sounds Japanese lacks get substituted

- English /l/ and /r/ both → the Japanese ら-row tap. "light" and "right" both → ライト.
- English "th" → サ-row or ザ-row. "three" → スリー, "the" → ザ.
- English /v/ → バ-row (or ヴ). "video" → ビデオ.
- English /si/ → シ. "system" → システム.

### Rule C — the source is often not English

Many "loanwords" come from German, Portuguese, Dutch, French, etc. Learners with European L1s (especially German) often recognise these immediately:

- アルバイト "part-time job" — from German *Arbeit*
- パン "bread" — from Portuguese *pão*
- エネルギー "energy" — from German *Energie* (note: not the English vowel pattern)
- テーマ "theme/topic" — from German *Thema*
- カルテ "medical chart" — from German *Karte*

### Rule D — clipping and *wasei-eigo*

Japanese frequently **shortens** loanwords, and sometimes **invents** "English" that no English speaker would recognise (*wasei-eigo*, "Japan-made English"):

- テレビ — clipped "television"
- スマホ — clipped "smartphone" (スマート + ホン)
- コンビニ — clipped "convenience store"
- パソコン — "personal computer", a wasei-eigo blend
- サラリーマン — "salaried man" = a (male) office worker; wasei-eigo

The blueprint mentions a tendency toward short forms — many clipped loanwords land around three to four morae. Do not expect the loanword to match the English length or even the English meaning.

**The takeaway:** when you meet an unfamiliar katakana word, decode the kana, then *reverse the transformation rules* — strip inserted vowels, undo the sound substitutions — and a familiar word often appears. But verify the meaning; do not assume it matches the English. This recover-the-source skill is a genuine reading strategy you will use constantly.

---

## Loanword reading practice

Decode each katakana word aloud, then identify the source word and meaning. Answers below — cover them first.

1. コーヒー
2. パーティー
3. テレビ
4. ホテル
5. レストラン
6. インターネット
7. コンピューター
8. アイスクリーム
9. スイス
10. ハンガリー
11. チョコレート
12. エレベーター
13. ファイル
14. ジュース
15. メール

### Answers

1. コーヒー — "coffee" (4 morae; note ー twice).
2. パーティー — "party" (uses ティ for the "ti" sound).
3. テレビ — "television", clipped (Rule D).
4. ホテル — "hotel" (final *l* → ル).
5. レストラン — "restaurant" (from French/English).
6. インターネット — "internet" (note ッ small tsu and inserted vowels).
7. コンピューター — "computer" (uses ピュ yōon; long final ー).
8. アイスクリーム — "ice cream".
9. スイス — "Switzerland" (a place name — from German *Schweiz*, not English).
10. ハンガリー — "Hungary" (place name).
11. チョコレート — "chocolate" (チョ yōon).
12. エレベーター — "elevator / lift".
13. ファイル — "file" (uses ファ for the "fa" sound).
14. ジュース — "juice" (ジュ yōon).
15. メール — "(e-)mail", clipped from "email".

More katakana practice — including the シ/ツ and ソ/ン discrimination drill — is in `exercises.md`. Loanword vocabulary is collected in `module-vocab.json`.

---

## Module 00 complete

With this chapter done you have finished Module 00. You should now read both kana scripts fluently and recognise loanword spelling conventions. Confirm milestone **M1** — 40 mora/min sight-reading combining hiragana and katakana, no chart — then advance to **Module 01 — Copula Basics**, where grammar begins and everything is written in kana with no romaji.
