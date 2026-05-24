---
title: /speech — pronunciation practice (Azure Pronunciation Assessment)
date: 2026-05-25
status: approved
---

# Goal

A `/speech` page where the learner picks a curriculum phrase, reads it aloud into the mic, and gets a Duolingo-style score back — overall + per-word accuracy. Powered by Azure Speech Service's Pronunciation Assessment REST API.

# Architecture

Token-mediated, SDK in browser:
- `api/speech-token.js` — Vercel Function. Exchanges `SPEECH_KEY` (server env var) for a short-lived (~10 min) Azure auth token. Returns `{ token, region }`.
- Browser loads Microsoft Speech SDK from CDN, initialises with the token, captures mic audio via `AudioConfig.fromDefaultMicrophoneInput()`, streams it to Azure, parses the assessment JSON, renders scores.
- Audio never traverses Vercel; the function exists only to keep the key off the client.

# Files

**Created:**
- `api/speech-token.js` — Vercel Function. Stdlib `fetch` only; no `package.json` needed.
- `tools/templates/speech.html` — self-contained page (CDN SDK + inline CSS/JS).
- `docs/superpowers/specs/2026-05-25-speech-design.md` — this spec.

**Modified:**
- `tools/build_site.py` — adds `(OUT_DIR / "speech").mkdir()` and writes `public/speech/index.html` from the template.
- `tools/templates/landing.html` — 6th card.
- All 8 nav bars (every template + standalone HTML) — add "Speech" link, mark active on /speech.

# UX flow

1. Visit `/speech` → page loads phrase list from `/dict-index.json` (filter to `type: "example"` only).
2. First phrase shown: kana, romaji ruby, English. Topic dropdown (later) and Next/Random buttons.
3. Click the big mic button:
   - First time: browser prompts for mic permission.
   - SDK starts listening; UI shows "Listening…" with a pulsing indicator.
   - User speaks the phrase. SDK auto-stops at end-of-speech (~1s silence).
4. Spinner while Azure processes (~1–3 s round trip).
5. Result panel:
   - Overall PronunciationScore (0–100) + colored bar.
   - Sub-scores: Accuracy / Fluency / Completeness.
   - Per-word strip: each word coloured green (≥80), yellow (60–79), red (<60).
   - Click a word → small popover with its accuracy + phoneme rows (if Azure returned them).
6. Buttons: "Try again" (same phrase, re-record) / "Next phrase".

# Phrase corpus

Reuses `public/dict-index.json` (built today). Filter to entries where `type === "example"` to get short, well-translated sentences. Currently ~95 phrases (all M00+M01); grows automatically.

# Setup (one-time)

The learner does this once after deploy:
1. Free Azure account (no credit card required for the F0 tier).
2. Azure portal → **Create resource** → **Speech** (free tier `F0` — 5 hours/month).
3. From the resource page, copy **Key 1** and **Region** (e.g. `westeurope`).
4. In Vercel → project settings → Environment Variables, add:
   - `SPEECH_KEY` = the key
   - `SPEECH_REGION` = the region
5. Trigger a redeploy (any git push will do).

# Configuration

- Audio format: handled by the Speech SDK (16 kHz mono PCM internally).
- Reference text passed to Azure: the raw kana string of the phrase (e.g. `わたし は がくせい です。`). Azure's JP model handles kana directly — no romaji conversion needed.
- Pronunciation Assessment config:
  - `GradingSystem: HundredMark`
  - `Granularity: Phoneme`
  - `EnableMiscue: true`
  - `PhonemeAlphabet: SAPI` (Azure's notation; we display word-level by default and only show phoneme detail in a popover if the user clicks)

# Graceful degradation

- If `/api/speech-token` returns 500 because env vars are missing: page renders normally but the mic button is disabled with text "Speech service not configured. See setup steps above."
- If the SDK fails to load from CDN: same disabled state with a different message.
- If mic permission is denied: button shows "Microphone permission denied. Click to retry."
- If Azure returns no NBest result: status shows "No speech detected. Try again."

# Verification

- `bash scripts/build-vercel.sh` succeeds; `public/speech/index.html` exists.
- `/speech` page renders, shows a phrase, mic button visible. Without env vars, mic button is disabled with a helpful message.
- With env vars: clicking the mic captures audio, returns a score, renders word-level coloring.
- Landing now shows 6 cards in the auto-fit grid.
- Every existing page has the new "Speech" nav link.

# Risks

- Setup friction (Azure account + Vercel env vars). Unavoidable; mitigated by clear inline instructions on the page.
- Free-tier quota (5 hrs/mo). For personal use, plenty.
- Azure JP phoneme detail may be sparse on very short utterances; word-level scoring is the dependable signal.
- Vercel Function cold start adds ~300 ms to the first token fetch; warm thereafter.
- Some browsers (Safari) gate `getUserMedia` behind direct user gesture; we only call it on mic button click — should be fine.

# Out of scope (v1)

- Free-form mode (no target text)
- Listening quiz mode (audio → type)
- Saving scores / streaks / gamification
- Mobile-optimised UI (responsive but not hand-tuned for one-handed mobile)
- Whisper/Web Speech fallback if Azure unavailable
- Phrase categorisation beyond what `dict-index.json` already exposes
- Inline phoneme replay (Azure provides ranges but we don't visualise per-phoneme audio)
