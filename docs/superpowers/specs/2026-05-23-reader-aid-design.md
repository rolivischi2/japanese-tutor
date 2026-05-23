---
title: Reader Aid — screen-capture OCR + romaji ruby
date: 2026-05-23
status: approved
---

# Reader Aid — screen-capture OCR + romaji ruby

## Goal

A `/reader` page on the deployed site that helps the learner read Japanese text shown by a tutor (or any source) during a live session. Workflow: click "Capture screen", browser screen-share API grabs a frame of the chosen window, Tesseract.js OCRs the Japanese text, kuroshiro/wanakana renders it with romaji as ruby above each word (kanji+kana) or mora (pure kana). Fully client-side, no API keys, no server.

## Non-goals (v1)

- No region cropping after capture.
- No saved capture history.
- No audio TTS playback.
- No English glosses or word definitions (Yomitan handles that on copyable text).
- No clipboard-paste fallback (the learner picked screen capture as the input method).
- No mobile support beyond what the browser screen-share API gives for free.
- No cloud OCR / Vercel Functions. Fully static deploy.

## Decisions baked in

1. **All client-side.** OCR via Tesseract.js. Romaji via kuroshiro + kuroshiro-analyzer-kuromoji (for mixed kanji+kana) with wanakana as the pure-kana fallback. No backend, no API key, no Vercel Function.
2. **Libraries from CDN.** First-session download cost: ~10 MB (Tesseract JP model) + ~25 MB (kuroshiro/kuromoji dictionary) + small library JS (~200 KB). Cached afterwards. CDN: unpkg.com (matches what the existing kana-guide.html already uses for fonts/libraries).
3. **Single self-contained HTML file.** `tools/reader.html` is the source of truth. It contains its own HTML, inline CSS, inline JS, and `<script src=...>` CDN imports. Same authoring pattern as the existing `modules/00-writing-systems/kana-guide.html`.
4. **Whole-frame OCR in v1.** No cropping UI. The captured image goes to Tesseract as-is. If real-world accuracy is poor, region-selection can be added later.
5. **Screen capture only.** The "Capture screen" button calls `navigator.mediaDevices.getDisplayMedia()`. Browser shows its native picker (screen / window / tab). Tool grabs ONE frame, immediately stops the stream (no continuous capture). User clicks the button again for the next frame.
6. **Ruby rendering rules.**
   - If recognized text contains any CJK Unified Ideograph (kanji): pass the entire text through kuroshiro in `mode: "furigana", to: "romaji"`. Output is HTML with one `<ruby>` per token from the kuromoji tokenizer.
   - If text is pure kana (hiragana/katakana only): use wanakana to split into morae (handles ya/yu/yo combinations, sokuon, long-vowel mark), wrap each mora in `<ruby><kana><rt>romaji</rt></ruby>`.
   - If parsing fails for any reason: fall back to displaying the OCR text plain, with the error message above it.
7. **Display: ruby + raw side-by-side.** Top: rendered ruby. Below: the raw Tesseract output as selectable plain text, so the learner can copy it elsewhere or spot OCR errors.
8. **Landing-page integration.** The "Reader Aid" becomes a third card in the existing kana-tools section of `/`. The cards section grid expands from 2 columns to 3 on desktop; stays 1 column on mobile. Existing Kana Guide and Printable Chart cards keep their current copy.

## Scope of changes

### New files

- **`tools/reader.html`** — single self-contained HTML page (~400-600 LOC counting inline CSS+JS). Structure:
  - `<head>`: fonts (Fraunces + Noto Sans JP, matching landing aesthetic), inline CSS using the same `--paper`/`--vermilion`/`--gold` palette as `tools/templates/landing.html` for visual consistency. CDN `<script>` tags for Tesseract.js, kuroshiro, kuroshiro-analyzer-kuromoji, wanakana.
  - `<body>`: header with title + brief instructions, control row (`Capture screen` button, status text), preview area for the captured image, result area with ruby output on top + raw OCR text below.
  - Inline JS: ~150-300 LOC. Functions: `captureScreen()` → grabs one frame from `getDisplayMedia()`, draws to canvas, returns blob; `runOCR(blob)` → Tesseract worker with `jpn` language, returns recognized text + confidence; `renderRomaji(text)` → routes to `renderRomajiKuroshiro` (mixed) or `renderRomajiWanakana` (pure kana), returns HTML string; `setStatus(msg)` → updates the status line. UI event handlers wire these together.

### Modified files

- **`tools/build_site.py`** — one line added inside `main()`: `(OUT_DIR / "reader").mkdir()` alongside the existing `kana` and `chart` mkdirs.
- **`scripts/build-vercel.sh`** — one line added: `cp "$ROOT/tools/reader.html" "$OUT/reader/index.html"`. Echo summary line updated to mention `/reader`.
- **`tools/templates/landing.html`** — third card added in the `.cards` section. Grid template column count adjusted from `1fr 1fr` to `repeat(3, 1fr)` on desktop; mobile breakpoint kept as `1fr`. Hero kicker / `h1` text can stay the same.

### Deleted files

- None.

## CDN libraries (specific pins)

- Tesseract.js: `https://unpkg.com/tesseract.js@5/dist/tesseract.min.js`. Tesseract worker auto-fetches `jpn.traineddata` from the standard tessdata CDN on first OCR call.
- kuroshiro: `https://unpkg.com/kuroshiro@1.2.0/dist/kuroshiro.min.js`
- kuroshiro-analyzer-kuromoji: `https://unpkg.com/kuroshiro-analyzer-kuromoji@1.1.0/dist/kuroshiro-analyzer-kuromoji.min.js`
- wanakana: `https://unpkg.com/wanakana@5/wanakana.min.js`

All four are MIT-licensed. Version pins are minor-version-stable. If a CDN release breaks compatibility (e.g. unpkg pulls a `5.1.0` that changes Tesseract's worker API), the page falls back to the global-error path with a clear message; the rest of the site is unaffected.

## UI flow (concrete)

1. Page loads. Header shows: "Reader Aid — capture, OCR, romaji above each character". Status line: "Ready. Click Capture screen to begin."
2. User clicks **Capture screen**. Browser shows native screen/window/tab picker.
3. User picks the Preply tutor window. Browser starts a screen-share stream. Tool reads one frame via `<video>` element + `<canvas>`, then immediately stops the stream tracks.
4. Captured frame appears in preview area at ~40% width.
5. Status line: "Loading OCR model…" (only first time; cached after).
6. Status line: "Recognizing…" while Tesseract runs (5–20s depending on image size).
7. Result area populates:
   - Ruby block: rendered HTML with romaji above each token/mora.
   - Raw block: plain text below, selectable for copy-paste.
   - Status line: "Done. Confidence: NN%."
8. User clicks **Capture screen** again for the next sentence. Repeat.

If OCR returns empty text or kuroshiro/wanakana throw: status shows the error, raw text shows whatever OCR produced (possibly empty), ruby area shows "(no romaji rendered)".

## Rendering specifics

### Mixed kanji+kana path
```js
const kuroshiro = new Kuroshiro();
await kuroshiro.init(new KuroshiroAnalyzerKuromoji({
  dictPath: "https://unpkg.com/kuromoji@0.1.2/dict/"
}));
const html = await kuroshiro.convert(text, {
  mode: "furigana",
  to: "romaji",
  romajiSystem: "hepburn"
});
// html is a string like '<ruby>食<rt>ta</rt>べ<rt>be</rt>る<rt>ru</rt></ruby> ...'
// (kuroshiro emits per-mora ruby segments)
```

### Pure kana path
```js
function splitMorae(kanaText) {
  const tokens = wanakana.tokenize(kanaText, { detailed: true });
  // tokens is e.g. [{ type: 'hiragana', value: 'きゃ' }, ...]
  // Further split each kana token into morae using wanakana's stripOkurigana
  // OR use a simple regex: /[ぁ-んァ-ヶー]+/ then segment by mora rules.
  const out = [];
  for (const t of tokens) {
    if (t.type !== "hiragana" && t.type !== "katakana") {
      out.push({ kana: t.value, romaji: t.value });
      continue;
    }
    // Mora split: combine small ya/yu/yo with preceding char; sokuon
    // attaches to next; long-vowel mark attaches to previous.
    const morae = splitKanaIntoMorae(t.value);
    for (const m of morae) {
      out.push({ kana: m, romaji: wanakana.toRomaji(m) });
    }
  }
  return out;
}
```

`splitKanaIntoMorae(kanaText)` is a 20-line function that walks the string and groups characters by these rules:
- A small kana (ゃゅょゎァィェォャュョッ) attaches to the preceding base.
- The katakana long-vowel mark ー attaches to the preceding.
- Sokuon っ/ッ attaches to the FOLLOWING base.
- Otherwise each kana stands alone.

This is deterministic, well-defined, no external lib needed.

### HTML output
```html
<ruby>き<rt>ki</rt></ruby><ruby>ょ<rt>(part of きょ)</rt></ruby>
```
becomes the cleaner:
```html
<ruby>きょ<rt>kyo</rt></ruby>
```
when morae are grouped correctly. Spec uses the grouped form.

## Verification

- Local: `bash scripts/build-vercel.sh` produces `public/reader/index.html`.
- Local server: `python -m http.server -d public 8765`, open `http://localhost:8765/reader/`, click Capture screen, pick a window, verify OCR + ruby render works on at least one test image.
- Landing card: open `http://localhost:8765/`, confirm three cards display side-by-side, the new "Reader Aid" card links to `/reader/`.
- Deployed: after push, `curl -sI https://japan-learning-omega.vercel.app/reader/` returns 200; landing's `class="card"` count is 3 (the two kana-tools cards plus reader).
- Smoke test image: capture a known sentence (e.g. `これは ペン です。`), confirm Tesseract reads it correctly and the ruby output shows `kore-wa pen desu` (or close to it).

## Risks

- **Tesseract.js JP accuracy on screen-share text**: small font, low contrast, and font hinting can degrade OCR. Mitigation: display raw output next to ruby so the learner can spot errors; raw text is also useful for re-running through Yomitan. If accuracy is poor in practice, add a region-crop step or swap OCR engines later.
- **First-load size (~35 MB)**: noticeable on a slow connection. Mitigation: clear status messages during model load ("Loading OCR model, ~10 MB — first time only"). Cached after. Pre-loading on page open before first click is an optimization for v2.
- **CDN outage / version drift**: a CDN-served library could break with a new minor version. Mitigation: pin major versions in the URLs (already specified above). If unpkg goes down, page can't function until the CDN recovers. Self-hosting the libs under `public/reader/vendor/` is the v2 fallback.
- **Browser screen-share permission flow**: re-prompts every tab session. Not a blocker, just expected.
- **Tesseract worker memory**: large captures (4K screen-share) can use ~500 MB of RAM during recognition. Browser tab may slow down. Mitigation: downscale frames wider than 2000px before sending to OCR. Implementation: simple canvas-resize step before `toBlob`.
- **Mixed-script edge cases**: text containing CJK characters that aren't kanji (e.g. Chinese-only ideographs misrecognized by Tesseract's JP model) may make kuroshiro emit unreadable output. Mitigation: if kuroshiro throws, fall back to wanakana for any kana-only segments and show the original characters as-is for the rest.

## Out of scope (explicit reminder)

- Cropping
- TTS
- Glossary lookup
- Capture history
- Clipboard paste
- Region-of-interest selection
- Self-hosted libs
- Pre-loading models on page open
- Mobile-specific UI
- Vertical Japanese text
