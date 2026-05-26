# /drill — backlog of v1-deferred ideas

Captured at v1 ship time (2026-05-26) so they're not forgotten. Each entry
is a candidate for a focused follow-up session — pick by impact when you
revisit.

## Modes / directions

- **Reverse direction**: romaji → kana. Same SRS engine; flips prompt/answer.
- **Sokuon / sequence drills**: multi-character prompts (e.g. `かっぱ`, `ちょっと`) — tests reading at speed, not single recognition.
- **Word-level drill**: pull words from the curriculum dictionary corpus, drill reading. Step beyond character recognition.
- **Phrase-level drill**: full short phrases from `/phrases`, timed.
- **Reverse audio drill**: TTS speaks a syllable, user types/picks the kana. Listening practice.

## Learning aids

- **Audio TTS playback** of the correct answer on every prompt (the kana voice already used in the kana guide).
- **Stroke-order reveal** when wrong: show animated stroke order for the missed character (data already in `tools/data/kana-strokes.json`).
- **Mnemonic hint button** on wrong: surface the same mnemonic shown in the kana guide.

## Engine improvements

- **True SRS with intervals** (SM-2 or FSRS) rather than the v1 Leitner-style bucket. Schedule each item for a specific future timestamp; surface only items due now.
- **Per-set "due now" mode** that only shows the weakest 20% — a fast warm-up.
- **Confidence rating buttons** after each answer (1-4) like Anki, instead of binary right/wrong.

## Insights / history

- **Per-day accuracy graph** — small inline chart of daily success rate.
- **Slowest characters list** — top N characters by average response time (need to record response time per answer).
- **Reaction time tracking** — record ms from prompt → enter; flag items above N standard deviations.
- **Heatmap of confusion pairs** — which characters get mistaken for which (e.g. ね vs れ, シ vs ツ).

## Portability

- **Cloud sync / multi-device progress** — pick a backend (Firebase, Supabase, or a tiny Vercel KV store) and stream the localStorage state up. Useful if the learner switches between phone and laptop.
- **Exportable progress dump** — JSON download button so the user can back up / move between browsers without an account.
- **Importable dump** — paste-in-a-blob restore.

## UI / UX polish

- **Keyboard shortcuts shelf** — `?` to show help, `r` to reset streak, `s` to open settings.
- **Theme toggle** — match the planned dark mode if/when that ships.
- **Touch-friendly answer pad** — on-screen romaji keys for mobile-only sessions (typing on a phone keyboard is slow for romaji).
- **Focus-mode** — full-screen distraction-free toggle that hides the nav.
