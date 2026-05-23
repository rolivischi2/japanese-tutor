---
module: 00
file: 00-overview
lang_focus: writing
kanji_level: 0
last_updated: 2026-05-23
---

# Module 00 — Writing Systems

## Why this module exists

Japanese is written with three scripts working together: **hiragana**, **katakana**, and **kanji**. Two of them — hiragana and katakana, collectively the **kana** — are syllabic alphabets: each symbol stands for one *mora* (a unit of sound, roughly a consonant+vowel beat). They are small, finite, and learnable in two weeks. Kanji are thousands of meaning-symbols; they are deliberately **not** in this module.

This module has **no grammar**. Its single job is to make you a fluent kana reader before any grammar arrives, so that from Module 01 onward you never have to decode symbols and parse grammar at the same time. Decoding must become automatic — like reading the Latin alphabet — or it silently taxes everything built on top of it.

Depending on your L1, you may find kana learning is mostly a *visual* task rather than an auditory one — many learners already have a phonological system that maps cleanly onto most Japanese sounds. If you are a Hungarian speaker, see `pronunciation/07-hungarian-transfer-notes.md` for detailed transfer notes. If you are a German or Swiss German speaker, see `pronunciation/08-german-swiss-german-transfer-notes.md`. The sounds may come easily; the shapes are the work.

## Goals

By the end of this module you can:

1. Read every hiragana symbol — base, dakuten/handakuten, and yōon combinations — on sight, with no chart.
2. Read every katakana symbol on sight, with no chart.
3. Read the long-vowel mark ー and the small-kana foreign-sound combinations (ファ, ティ, ウィ, ジェ …) used in loanwords.
4. **Sight-read kana at 40 mora/min or faster** — see "Practice goal" below. This is milestone M1 in `progress/milestones.md`.
5. Read a handful of fixed greetings written purely in kana (see `dialogues.md`).

You do **not** learn to handwrite kana to any standard here. Recognition is the priority. Light tracing helps memory and is encouraged, but speed of *reading* is what is measured.

## Learning order

Hiragana first, fully, then katakana. Hiragana is the higher-frequency script and the one grammar is written in; katakana shares the same sound system, so learning it second means you only learn new *shapes*, not new sounds.

| Days | Content | File |
|---|---|---|
| 1 | 5 vowels あいうえお, then か-row | `01-hiragana-vowels-and-rows.md` |
| 2 | さ-row, た-row | `01-hiragana-vowels-and-rows.md` |
| 3 | な-row, は-row | `01-hiragana-vowels-and-rows.md` |
| 4 | ま-row, や-row | `01-hiragana-vowels-and-rows.md` |
| 5 | ら-row, わ-row + ん | `01-hiragana-vowels-and-rows.md` |
| 6 | dakuten / handakuten (が ざ だ ば ぱ) | `02-hiragana-dakuten-and-yoon.md` |
| 7 | yōon (きゃ きゅ きょ etc.) | `02-hiragana-dakuten-and-yoon.md` |
| 8 | review + first sight-reading speed test | — |
| 9–13 | full katakana (gojūon, dakuten, yōon) — ~2 rows/day | `03-katakana.md` |
| 14 | katakana loanword traps; final speed test | `04-katakana-loanword-traps.md` |

Pacing is a target, not a contract. If a speed test is failed, repeat days rather than advance — kana is the foundation and a shaky foundation is expensive later. The "one new row per day" rhythm is deliberate: small daily batches plus spaced review beat cramming.

## Daily routine (~25–35 min for this module's portion)

This sits inside the full daily routine in `README.md`. The kana-specific block:

1. **New batch (~8 min).** Read the day's new row in `01`/`02`/`03`. Look at each symbol, say its sound, read the Tofugu mnemonic once.
2. **Tracing (~5 min).** Trace each new symbol 5–10 times on paper or tablet, saying the sound aloud each stroke. This is for memory, not calligraphy.
3. **SRS drill (~10 min).** Run the Anki kana deck (see Tools). New cards: the day's batch. Reviews: everything prior.
4. **Speed drill (~5–10 min).** realkana.com — select all rows learned so far, drill until reading is reflexive.

Plus, from Day 1, the rest of the routine runs in parallel: 15 min Anki (Kaishi 1.5k vocab deck), ~20 min listening (Comprehensible Japanese, Yuki — cijapanese.com), and the pitch-accent perception drill (Kotu.io, 10 min). Listening starts now, before you can read fluently — your ears need a head start. See `pedagogy/00-philosophy.md`.

## Practice goal — 40 mora/min sight-reading

The concrete exit criterion. **Mora** = the kana beat: あ is one mora, きゃ is one mora (a yōon counts as one), the small っ counts as one, a long vowel counts as one. 40 mora/min ≈ reading roughly 8–10 short kana words per minute without a chart and without sounding-out hesitation.

How to measure: in realkana.com or with a kana word list, read aloud continuously for 60 seconds and count morae read correctly. Test at end of Day 8 (hiragana only) and Day 14 (hiragana + katakana). If you are below 40, do not advance — repeat drills until you clear it. 40 mora/min is a *floor*; native casual reading is far faster, and your speed will keep climbing through Module 01 naturally.

Why this specific number: below ~40 mora/min, decoding is still effortful enough to interfere with grammar parsing in later modules. Above it, kana reading is "free" and grammar gets your full attention.

## Tools for this module

| Tool | Use | Link |
|---|---|---|
| **The Kana Guide** (this repo) | Interactive visual guide — every hiragana & katakana with stroke-order animation, audio, a mnemonic, and a practice quiz with look-alike drills. Open the file in any browser; no install. Your primary reference for this module. | `kana-guide.html` (in this folder) |
| **realkana.com** | Browser kana speed drill. Free, no account. Tick the rows you have learned; it shows random kana, you self-check. The main speed-building tool. | realkana.com |
| **Anki + a kana deck** | SRS for durable recall. Use any well-rated hiragana/katakana deck (AnkiWeb), or the kana portion of a starter deck. **Suspend / retire it once Module 00 ends** — kana belongs in your eyes, not your review queue forever. | apps.ankiweb.net |
| **Tofugu hiragana & katakana mnemonics** | Free picture-mnemonic guides — the fastest known way to memorise kana shapes. Referenced throughout `01`–`03` instead of being reinvented here. | tofugu.com/japanese/learn-hiragana / tofugu.com/japanese/learn-katakana |
| **Tofugu kana quiz / kana app** | Optional extra drilling, mnemonic-integrated. | — |

Setup details for Anki are in `tools/anki-setup.md`. Mac Japanese input (useful for typing practice, optional in this module) is in `tools/mac-japanese-input.md`.

## What comes next

Module 01 (Copula Basics) assumes you read kana fluently. Everything from there is written in kana (and, from Module 04, kanji) with **no romaji** — including this module. Romaji is a crutch that would defeat the entire purpose of learning to read, so it does not appear in any module file. The only place Latin-letter transcription is ever used in this repository is the `pronunciation/` track, where it sits next to IPA for explicit sound work.
