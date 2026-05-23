# Reader Aid Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a `/reader` page on the deployed site that captures one frame via browser screen-share, OCRs Japanese text via Tesseract.js, and renders romaji as ruby above each token (kuroshiro for mixed kanji+kana) or mora (wanakana for pure kana).

**Architecture:** A single self-contained HTML file (`tools/reader.html`) with inline CSS + JS, loading three libraries from unpkg CDN. The build pipeline adds one `mkdir` line in `tools/build_site.py` and one `cp` line in `scripts/build-vercel.sh`. The landing template gets a third card.

**Tech Stack:** Plain HTML/CSS/JS (no framework, no JS build step). CDN libs: Tesseract.js v5 (OCR), kuroshiro v1.2 + kuroshiro-analyzer-kuromoji v1.1 (kanji→romaji ruby), wanakana v5 (pure-kana → romaji + mora split).

---

## File map

**Created:**
- `tools/reader.html` — single self-contained HTML page. Inline CSS + JS. CDN script tags.

**Modified:**
- `tools/build_site.py` — one `(OUT_DIR / "reader").mkdir()` line added.
- `scripts/build-vercel.sh` — one `cp` line added; echo summary updated.
- `tools/templates/landing.html` — third card in the kana-tools `.cards` section; grid template column count goes from `1fr 1fr` to `repeat(3, 1fr)` on desktop.

**Deleted:** none.

---

## Task 1: Wire the build pipeline (mkdir + cp + landing third-card, with placeholder reader.html)

Goal of this task: get the deploy plumbing working end-to-end with a stub page so the rest of the work just edits the stub.

**Files:**
- Create: `tools/reader.html` (placeholder content)
- Modify: `tools/build_site.py`
- Modify: `scripts/build-vercel.sh`
- Modify: `tools/templates/landing.html`

- [ ] **Step 1: Create the placeholder `tools/reader.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reader Aid — japan-learning</title>
</head>
<body>
<h1>Reader Aid</h1>
<p>Coming soon. (Wiring test.)</p>
</body>
</html>
```

- [ ] **Step 2: Add `(OUT_DIR / "reader").mkdir()` in `tools/build_site.py`**

In `tools/build_site.py`, find the block inside `main()` that already creates `kana/` and `chart/` directories:

```python
    (OUT_DIR / "kana").mkdir()
    (OUT_DIR / "chart").mkdir()
```

Change it to:

```python
    (OUT_DIR / "kana").mkdir()
    (OUT_DIR / "chart").mkdir()
    (OUT_DIR / "reader").mkdir()
```

- [ ] **Step 3: Add the `cp` line in `scripts/build-vercel.sh`**

In `scripts/build-vercel.sh`, find the two existing `cp` lines:

```bash
cp "$ROOT/modules/00-writing-systems/kana-guide.html" "$OUT/kana/index.html"
cp "$ROOT/pronunciation/11-kana-printable-chart.html" "$OUT/chart/index.html"
```

Add one more line after them:

```bash
cp "$ROOT/tools/reader.html"                          "$OUT/reader/index.html"
```

Then update the echo summary block. The existing summary is:

```bash
echo
echo "Built $OUT/"
echo "  /                        → $OUT/index.html"
echo "  /kana                    → $OUT/kana/index.html"
echo "  /chart                   → $OUT/chart/index.html"
echo "  /modules/<slug>/...      → $OUT/modules/"
du -sh "$OUT"
```

Add one line for /reader:

```bash
echo
echo "Built $OUT/"
echo "  /                        → $OUT/index.html"
echo "  /kana                    → $OUT/kana/index.html"
echo "  /chart                   → $OUT/chart/index.html"
echo "  /reader                  → $OUT/reader/index.html"
echo "  /modules/<slug>/...      → $OUT/modules/"
du -sh "$OUT"
```

- [ ] **Step 4: Update the landing template grid + add third card**

In `tools/templates/landing.html`, find the CSS line:

```css
  section.cards{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:6px}
```

Change to:

```css
  section.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:6px}
```

And in the mobile media query, find:

```css
    section.cards{grid-template-columns:1fr}
```

Verify it's still `1fr` (it is — no change needed). Add a tablet breakpoint above it (since 3 cards at 720-1024px gets cramped). The full media query block becomes:

```css
  @media (max-width:980px){
    section.cards{grid-template-columns:1fr 1fr}
  }
  @media (max-width:680px){
    section.cards{grid-template-columns:1fr}
    h1{font-size:52px}
    main{padding:42px 18px 32px}
    header{margin-bottom:36px}
  }
```

Then find the closing `</section>` of the existing `<section class="cards">` block. Right before it (after the existing two `<a class="card">` entries), add the third card:

```html
    <a class="card" href="/reader">
      <div class="ch jp">読</div>
      <h2>Reader Aid</h2>
      <p>Live screen capture + Japanese OCR. Romaji ruby above every kana/word. Use it when your tutor shows hiragana you can&rsquo;t read on the spot.</p>
      <span class="arrow">Open</span>
    </a>
```

- [ ] **Step 5: Build and verify**

Run:

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
bash scripts/build-vercel.sh
ls public/reader/
head -10 public/reader/index.html
grep -oE 'class="card[^"]*"' public/index.html | grep -v module | sort | uniq -c
```

Expected:
- `public/reader/index.html` exists
- Its first lines match the placeholder
- The grep shows 3 `class="card"` entries in the kana-tools section (not counting `module-card`).

- [ ] **Step 6: Run build_site self-tests**

```bash
uv run tools/build_site.py --self-test
```
Expected: `PASS (13/13)`.

- [ ] **Step 7: Commit**

```bash
git add tools/reader.html tools/build_site.py scripts/build-vercel.sh tools/templates/landing.html
git commit -m "$(cat <<'EOF'
Wire /reader into build pipeline with placeholder content

Adds public/reader/ directory creation in build_site.py, cp line in
build-vercel.sh, and a third "Reader Aid" card on the landing page
(grid expands to 3 columns desktop, 2 on tablet, 1 on mobile).
The page content itself is a stub — real implementation in subsequent
commits.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: Page shell, CDN imports, and screen-capture logic

Replace the stub with a real page that shows the UI and captures one frame from the browser screen-share API.

**Files:**
- Modify: `tools/reader.html` (full replacement)

- [ ] **Step 1: Replace `tools/reader.html` with the page shell + capture logic**

Write the complete file contents:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reader Aid — japan-learning</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Noto+Sans+JP:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root{
    --paper:#f1e8d6; --paper-2:#e9dcc2; --ink:#2b2620; --ink-soft:#6f6557;
    --vermilion:#bd3b2c; --vermilion-deep:#9c2f23; --gold:#b08a4a;
    --cell:#f7f0e0; --cell-line:#d8c8a6;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{min-height:100%}
  body{
    background:var(--paper); color:var(--ink);
    font-family:"Fraunces",Georgia,serif;
    -webkit-font-smoothing:antialiased;
  }
  .jp,.romaji-output :lang(ja),ruby{font-family:"Noto Sans JP","Hiragino Kaku Gothic ProN","Yu Gothic","Meiryo",sans-serif}

  main{max-width:1000px;width:100%;margin:0 auto;padding:36px 24px 48px}
  header{margin-bottom:24px;padding-bottom:14px;border-bottom:1px solid var(--cell-line)}
  .kicker{font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--ink-soft);font-weight:600}
  h1{font-size:36px;font-weight:700;letter-spacing:.01em;margin:6px 0 4px}
  .tagline{font-style:italic;font-size:14.5px;color:var(--ink-soft);max-width:680px}

  .controls{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin:18px 0}
  button{font-family:inherit;font-size:14.5px;font-weight:600;letter-spacing:.02em;
    padding:10px 18px;border:1px solid var(--vermilion);background:var(--vermilion);
    color:#fff;border-radius:6px;cursor:pointer;transition:background .15s,transform .12s}
  button:hover:not(:disabled){background:var(--vermilion-deep);transform:translateY(-1px)}
  button:disabled{background:var(--cell);border-color:var(--cell-line);color:var(--ink-soft);cursor:not-allowed}
  button.secondary{background:transparent;color:var(--vermilion);}
  button.secondary:hover:not(:disabled){background:rgba(189,59,44,.08)}

  .status{font-size:13.5px;color:var(--ink-soft);min-height:1.4em}
  .status.err{color:var(--vermilion-deep)}

  .preview-wrap{margin-top:18px}
  .preview-wrap img{display:block;max-width:100%;border:1px solid var(--cell-line);border-radius:5px;background:#fff}

  .results{margin-top:24px}
  .results h3{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--ink-soft);font-weight:600;margin-bottom:8px;margin-top:18px}
  .romaji-output{font-size:24px;line-height:2.4;background:#fff;border:1px solid var(--cell-line);border-radius:6px;padding:18px 22px;min-height:80px;letter-spacing:.02em}
  .romaji-output ruby{margin:0 1px}
  .romaji-output ruby rt{font-size:.45em;color:var(--vermilion-deep);font-weight:500;letter-spacing:.02em}
  .raw-output{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:14px;line-height:1.7;background:var(--cell);border:1px solid var(--cell-line);border-radius:5px;padding:12px 16px;white-space:pre-wrap;min-height:40px;color:var(--ink)}

  .meta{margin-top:32px;font-size:13px;color:var(--ink-soft);line-height:1.6;
    background:rgba(255,255,255,.4);border-left:3px solid var(--gold);padding:12px 16px;border-radius:0 6px 6px 0}
  .meta b{color:var(--ink)}
</style>
</head>
<body>
<main>
  <header>
    <div class="kicker">japan-learning</div>
    <h1>Reader Aid</h1>
    <p class="tagline">Capture a screen region of Japanese text. OCR converts it to characters; romaji renders above every word or mora as a reading crutch.</p>
  </header>

  <div class="controls">
    <button id="capture-btn" type="button">Capture screen</button>
    <button id="reread-btn" type="button" class="secondary" disabled>Re-OCR last capture</button>
    <span id="status" class="status">Ready.</span>
  </div>

  <div class="preview-wrap" id="preview-wrap" hidden>
    <img id="preview" alt="Captured frame">
  </div>

  <div class="results">
    <h3>Romaji</h3>
    <div class="romaji-output" id="romaji-output" lang="ja">—</div>
    <h3>Raw OCR text</h3>
    <div class="raw-output" id="raw-output">—</div>
  </div>

  <p class="meta">
    <b>First-time load:</b> ~10 MB OCR model + ~25 MB kanji dictionary download (cached after).
    <b>Tip:</b> share the smallest window containing the text — OCR is faster and more accurate on tight crops.
  </p>
</main>

<script>
// ──────────────────────────────────────────────────────────────
// State
// ──────────────────────────────────────────────────────────────
const statusEl = document.getElementById("status");
const captureBtn = document.getElementById("capture-btn");
const rereadBtn = document.getElementById("reread-btn");
const previewWrap = document.getElementById("preview-wrap");
const previewEl = document.getElementById("preview");
const romajiOut = document.getElementById("romaji-output");
const rawOut = document.getElementById("raw-output");

let lastBlob = null;

function setStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.classList.toggle("err", isError);
}

// ──────────────────────────────────────────────────────────────
// Screen capture: getDisplayMedia → one frame → blob
// ──────────────────────────────────────────────────────────────
async function captureScreen() {
  setStatus("Requesting screen access…");
  let stream;
  try {
    stream = await navigator.mediaDevices.getDisplayMedia({ video: { cursor: "never" } });
  } catch (err) {
    setStatus("Screen capture cancelled.", true);
    return null;
  }

  const video = document.createElement("video");
  video.srcObject = stream;
  await new Promise(resolve => video.onloadedmetadata = resolve);
  await video.play();

  // Downscale very large frames so OCR stays manageable.
  const maxW = 2000;
  const scale = video.videoWidth > maxW ? maxW / video.videoWidth : 1;
  const w = Math.round(video.videoWidth * scale);
  const h = Math.round(video.videoHeight * scale);

  const canvas = document.createElement("canvas");
  canvas.width = w;
  canvas.height = h;
  canvas.getContext("2d").drawImage(video, 0, 0, w, h);

  stream.getTracks().forEach(t => t.stop());

  const blob = await new Promise(r => canvas.toBlob(r, "image/png"));
  previewEl.src = URL.createObjectURL(blob);
  previewWrap.hidden = false;
  setStatus(`Captured ${w}×${h}.`);
  return blob;
}

// ──────────────────────────────────────────────────────────────
// Wire UI (OCR + romaji rendering added in later tasks)
// ──────────────────────────────────────────────────────────────
captureBtn.addEventListener("click", async () => {
  captureBtn.disabled = true;
  romajiOut.textContent = "—";
  rawOut.textContent = "—";
  try {
    const blob = await captureScreen();
    if (blob) {
      lastBlob = blob;
      rereadBtn.disabled = false;
      // Subsequent tasks will OCR + render here.
    }
  } catch (err) {
    setStatus("Capture failed: " + err.message, true);
  } finally {
    captureBtn.disabled = false;
  }
});

rereadBtn.addEventListener("click", () => {
  if (!lastBlob) return;
  setStatus("Re-OCR not implemented yet (Task 3).");
});
</script>
</body>
</html>
```

- [ ] **Step 2: Build and open locally**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
bash scripts/build-vercel.sh
python3 -m http.server -d public 8765 &
echo $! > /tmp/jp-reader-server.pid
sleep 1
open http://localhost:8765/reader/
```

Click **Capture screen**. Browser should prompt for screen/window/tab. After selecting, a captured image should appear and status should read `Captured WxH.`

- [ ] **Step 3: Stop the local server**

```bash
kill $(cat /tmp/jp-reader-server.pid)
rm /tmp/jp-reader-server.pid
```

- [ ] **Step 4: Commit**

```bash
git add tools/reader.html
git commit -m "$(cat <<'EOF'
Reader Aid: page shell + screen-capture logic

Captures one frame from getDisplayMedia, downscales to <=2000px wide,
displays the preview. OCR + romaji rendering deferred to the next tasks.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: OCR via Tesseract.js

Add Tesseract.js, run OCR on the captured blob, populate the raw-output box with the recognized text.

**Files:**
- Modify: `tools/reader.html`

- [ ] **Step 1: Add the Tesseract.js script tag**

In `tools/reader.html`, find the `<link rel="stylesheet">` line in the `<head>` and add this immediately after the `<style>...</style>` block (just before `</head>`):

```html
<script src="https://unpkg.com/tesseract.js@5/dist/tesseract.min.js"></script>
```

- [ ] **Step 2: Add the OCR function inside the `<script>` block**

In `tools/reader.html`, find the comment line `// Wire UI (OCR + romaji rendering added in later tasks)` and replace everything between it and `</script>` with:

```js
// ──────────────────────────────────────────────────────────────
// OCR via Tesseract.js (Japanese)
// ──────────────────────────────────────────────────────────────
let ocrWorker = null;
async function getOcrWorker() {
  if (ocrWorker) return ocrWorker;
  setStatus("Loading OCR model (~10 MB, first time only)…");
  ocrWorker = await Tesseract.createWorker("jpn", 1, {
    logger: m => {
      if (m.status && m.progress != null) {
        setStatus(`OCR: ${m.status} (${Math.round(m.progress * 100)}%)`);
      }
    },
  });
  return ocrWorker;
}

async function runOCR(blob) {
  const worker = await getOcrWorker();
  setStatus("Recognizing…");
  const { data } = await worker.recognize(blob);
  return { text: data.text.trim(), confidence: data.confidence };
}

// ──────────────────────────────────────────────────────────────
// Wire UI
// ──────────────────────────────────────────────────────────────
async function processBlob(blob) {
  romajiOut.textContent = "(romaji rendering in Task 4)";
  rawOut.textContent = "";
  try {
    const { text, confidence } = await runOCR(blob);
    rawOut.textContent = text || "(empty OCR result)";
    setStatus(`Done. Confidence: ${Math.round(confidence)}%.`);
  } catch (err) {
    setStatus("OCR failed: " + err.message, true);
  }
}

captureBtn.addEventListener("click", async () => {
  captureBtn.disabled = true;
  romajiOut.textContent = "—";
  rawOut.textContent = "—";
  try {
    const blob = await captureScreen();
    if (blob) {
      lastBlob = blob;
      rereadBtn.disabled = false;
      await processBlob(blob);
    }
  } catch (err) {
    setStatus("Capture failed: " + err.message, true);
  } finally {
    captureBtn.disabled = false;
  }
});

rereadBtn.addEventListener("click", async () => {
  if (!lastBlob) return;
  rereadBtn.disabled = true;
  try {
    await processBlob(lastBlob);
  } finally {
    rereadBtn.disabled = false;
  }
});
```

Note: the previous version of these click handlers from Task 2 is fully replaced.

- [ ] **Step 3: Build and verify in a browser**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
bash scripts/build-vercel.sh
python3 -m http.server -d public 8765 &
echo $! > /tmp/jp-reader-server.pid
sleep 1
open http://localhost:8765/reader/
```

Click **Capture screen**, pick a window containing Japanese text (e.g. open `http://localhost:8765/modules/01-copula-basics/dialogues` in another tab and share that tab). Status should progress through OCR loading → recognizing → "Done. Confidence: NN%". The raw OCR box should fill with the recognized text.

- [ ] **Step 4: Stop the local server**

```bash
kill $(cat /tmp/jp-reader-server.pid)
rm /tmp/jp-reader-server.pid
```

- [ ] **Step 5: Commit**

```bash
git add tools/reader.html
git commit -m "$(cat <<'EOF'
Reader Aid: add Tesseract.js OCR pipeline

Loads the jpn OCR model on first use, displays raw recognized text and
confidence. Worker cached so subsequent captures skip the model load.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Romaji rendering — wanakana (pure-kana) + kuroshiro (mixed kanji+kana)

Add the two libraries and wire `processBlob` to render the recognized text with ruby above.

**Files:**
- Modify: `tools/reader.html`

- [ ] **Step 1: Add the three new CDN script tags**

In `tools/reader.html`, find the existing Tesseract `<script>` tag in `<head>`. Add three more right after it:

```html
<script src="https://unpkg.com/tesseract.js@5/dist/tesseract.min.js"></script>
<script src="https://unpkg.com/wanakana@5/wanakana.min.js"></script>
<script src="https://unpkg.com/kuroshiro@1.2.0/dist/kuroshiro.min.js"></script>
<script src="https://unpkg.com/kuroshiro-analyzer-kuromoji@1.1.0/dist/kuroshiro-analyzer-kuromoji.min.js"></script>
```

- [ ] **Step 2: Add the romaji helpers and rewrite `processBlob`**

In the `<script>` block, find the section comment `// OCR via Tesseract.js (Japanese)` block. Just BEFORE it, insert:

```js
// ──────────────────────────────────────────────────────────────
// Romaji rendering: pure-kana via wanakana, mixed via kuroshiro
// ──────────────────────────────────────────────────────────────
const KANJI_RE = /[一-鿿㐀-䶿]/;

function hasKanji(text) {
  return KANJI_RE.test(text);
}

const SMALL_KANA = new Set("ぁぃぅぇぉゃゅょゎァィゥェォャュョヮ");
const SOKUON = new Set("っッ");
const LONG_MARK = "ー";

/** Split a kana-only string into morae. Handles yoon, sokuon, long-vowel mark. */
function splitKanaIntoMorae(text) {
  const out = [];
  let i = 0;
  while (i < text.length) {
    let mora = text[i++];
    // Sokuon attaches to the NEXT base mora.
    if (SOKUON.has(mora) && i < text.length) {
      let next = text[i++];
      while (i < text.length && (SMALL_KANA.has(text[i]) || text[i] === LONG_MARK)) {
        next += text[i++];
      }
      out.push(mora + next);
      continue;
    }
    // Attach trailing small kana and long-vowel marks to the current mora.
    while (i < text.length && (SMALL_KANA.has(text[i]) || text[i] === LONG_MARK)) {
      mora += text[i++];
    }
    out.push(mora);
  }
  return out;
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, c => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  }[c]));
}

/** Render kana-only text as ruby HTML using wanakana for romaji. */
function renderWithWanakana(text) {
  const out = [];
  for (const line of text.split("\n")) {
    const morae = splitKanaIntoMorae(line);
    const lineHtml = morae.map(m => {
      if (wanakana.isKana(m) || /[ぁ-んァ-ヶー]/.test(m)) {
        const romaji = wanakana.toRomaji(m);
        return `<ruby>${escapeHtml(m)}<rt>${escapeHtml(romaji)}</rt></ruby>`;
      }
      return escapeHtml(m);
    }).join("");
    out.push(lineHtml);
  }
  return out.join("<br>");
}

let kuroshiro = null;
async function getKuroshiro() {
  if (kuroshiro) return kuroshiro;
  setStatus("Loading kanji dictionary (~25 MB, first time only)…");
  kuroshiro = new Kuroshiro();
  await kuroshiro.init(new KuromojiAnalyzer({
    dictPath: "https://unpkg.com/kuromoji@0.1.2/dict/",
  }));
  return kuroshiro;
}

/** Render mixed kanji+kana text as furigana-style ruby with romaji. */
async function renderWithKuroshiro(text) {
  const k = await getKuroshiro();
  return await k.convert(text, {
    mode: "furigana",
    to: "romaji",
    romajiSystem: "hepburn",
  });
}

async function renderRomaji(text) {
  if (!text) return "(no text)";
  try {
    if (hasKanji(text)) {
      return await renderWithKuroshiro(text);
    }
    return renderWithWanakana(text);
  } catch (err) {
    return `(romaji render failed: ${escapeHtml(err.message)})`;
  }
}
```

- [ ] **Step 3: Update `processBlob` to call `renderRomaji`**

Find the existing `async function processBlob(blob) { … }` and replace it with:

```js
async function processBlob(blob) {
  romajiOut.textContent = "";
  rawOut.textContent = "";
  try {
    const { text, confidence } = await runOCR(blob);
    rawOut.textContent = text || "(empty OCR result)";
    setStatus("Rendering romaji…");
    const html = await renderRomaji(text);
    romajiOut.innerHTML = html;
    setStatus(`Done. OCR confidence: ${Math.round(confidence)}%.`);
  } catch (err) {
    setStatus("Processing failed: " + err.message, true);
  }
}
```

- [ ] **Step 4: Build and verify in browser**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
bash scripts/build-vercel.sh
python3 -m http.server -d public 8765 &
echo $! > /tmp/jp-reader-server.pid
sleep 1
open http://localhost:8765/reader/
```

Test cases (open in separate tab and share THAT tab via the Capture button):
1. Pure hiragana: open `http://localhost:8765/modules/01-copula-basics/dialogues` and share — recognized text should show romaji above each mora (look for ruby `rt` elements in DevTools).
2. Mixed kanji+kana: open `http://localhost:8765/modules/01-copula-basics/05-no-possession` — should trigger kuroshiro path and render furigana-style romaji.

If the kuroshiro dictionary download stalls (the 25 MB path comes from unpkg's `/kuromoji@0.1.2/dict/` — a directory of small `.dat.gz` files), check the browser network tab. Status will say "Loading kanji dictionary…" until the lookup tables download.

- [ ] **Step 5: Stop the local server**

```bash
kill $(cat /tmp/jp-reader-server.pid)
rm /tmp/jp-reader-server.pid
```

- [ ] **Step 6: Commit**

```bash
git add tools/reader.html
git commit -m "$(cat <<'EOF'
Reader Aid: romaji rendering — wanakana (kana) + kuroshiro (kanji)

Pure-kana text is split into morae (handling yoon, sokuon, long-vowel
mark) and rendered as ruby via wanakana.toRomaji. Text containing
kanji is passed to kuroshiro in furigana→romaji mode, which emits
HTML with per-token ruby. Falls back to a visible error in the
romaji box if either path throws.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Push and verify deployed

**Files:** none modified.

- [ ] **Step 1: Push**

```bash
cd /Users/rvischi/Documents/repositories/japan-learning
git push origin main
```

- [ ] **Step 2: Wait for Vercel build, then verify the page is live**

```bash
until curl -s https://japan-learning-omega.vercel.app/reader/ | grep -q 'Reader Aid'; do sleep 5; done
echo "DEPLOYED"
curl -sI https://japan-learning-omega.vercel.app/reader/ | head -3
```

Expected: eventually prints `DEPLOYED` and `HTTP/2 200`.

- [ ] **Step 3: Verify landing card and reader page in a browser**

```bash
open https://japan-learning-omega.vercel.app/
```

Visually confirm:
- Three cards on the landing (Kana Guide, Printable Chart, Reader Aid)
- Click "Reader Aid" → loads /reader/
- Click "Capture screen" → browser prompt → pick a window with Japanese text → OCR runs → ruby renders

- [ ] **Step 4: If the deployed build fails**

If `curl -sI` returns 404, Vercel build likely failed. Check Vercel dashboard or `gh run list` if GitHub Actions is wired. Common cause: nothing changed in `public/` that Vercel can serve, or `build-vercel.sh` exited non-zero (`uv` missing, etc.). Diagnose and re-push.

---

## Notes on style

- The reader page is self-contained (single HTML file with inline CSS + JS). Do NOT split CSS or JS into separate files — keeping it single-file matches the existing `kana-guide.html` pattern and means there's no extra deploy plumbing.
- CDN script tags pin major versions where useful (`@5`, `@1.2.0`, `@1.1.0`). Avoid mixing pinned and floating major versions on related libraries.
- The romaji rendering deliberately uses two libraries: wanakana is small and fast for the common pure-kana case; kuroshiro is heavy but the only way to get readings for kanji.
- The mora splitter is intentionally pure JS (~30 LOC) rather than relying on a library — wanakana's `tokenize()` doesn't group morae the way furigana rendering needs.
- Watch the `status` text closely during dev: it's the only place errors surface to the user.
