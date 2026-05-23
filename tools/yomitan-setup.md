---
module: meta
file: yomitan-setup
lang_focus: tooling
kanji_level: 0
last_updated: 2026-05-23
---

# Yomitan Setup

Yomitan is the **on-hover Japanese pop-up dictionary** at the centre of this curriculum's reading workflow. Hover any Japanese word in your browser → see kana reading, English gloss, pitch accent, and a one-click "+" to send it to Anki for mining.

It is **on-hover by design** — that is the point. Persistent furigana over every kanji on every page (the "overlay" model) makes you read the kana instead of the kanji. Yomitan forces a micro-quiz: try the word first, hover only if you fail. That is the pedagogy this repo commits to.

---

## TL;DR — install path

1. Install the Yomitan extension in Chrome, Firefox, or Edge.
2. Import 4 dictionaries: Jitendex, KANJIDIC, Kanjium pitch accent, JPDB frequency.
3. Install AnkiConnect in Anki, then wire Yomitan → Anki.
4. Hover any Japanese word. Press `+` to mine it.

Total time: ~20 minutes the first time.

---

## 1. Install the extension

Yomitan is open source — canonical source: <https://github.com/yomidevs/yomitan>.

| Browser | How to install |
|---|---|
| **Chrome / Edge / Brave** | Chrome Web Store → search **"Yomitan"** → *Add to Chrome*. |
| **Firefox** | addons.mozilla.org → search **"Yomitan"** → *Add to Firefox*. |
| **Safari** | Not officially supported. Use **10ten Japanese Reader** instead (see §6). |

After install: click the Yomitan toolbar icon → **Settings**. This opens the dashboard in a tab — everything below happens there.

---

## 2. Import dictionaries

Yomitan ships with no dictionaries; you add them. Get these four:

| # | Dictionary | What it does | Where |
|---|---|---|---|
| 1 | **Jitendex** | Primary J→E gloss (modern JMdict fork). | <https://jitendex.org> — download the latest `.zip` |
| 2 | **KANJIDIC (English)** | Per-kanji readings + meanings + stroke count. | Linked from Yomitan's dictionary list / GitHub README |
| 3 | **Kanjium pitch accent** | Pitch accent overlay — **REQUIRED for this curriculum**. | Linked from Yomitan's dictionary list |
| 4 | **JPDB v2 frequency** | Frequency rank — helps decide what to mine. | <https://jpdb.io> exports / Yomitan dict list |

**To import each one:**
1. Yomitan dashboard → **Dictionaries** → *Configure installed and enabled dictionaries*.
2. **Import** → select the downloaded `.zip` (no need to unzip).
3. Wait for indexing (~20 s for Jitendex on a recent Mac).
4. Tick the **Enabled** box.

Recommended display order at the top of the popup: **Jitendex → Kanjium → KANJIDIC → JPDB**.

---

## 3. Anki bridge (AnkiConnect)

Mining = one-click "save this word to Anki for review." Setup:

1. In **Anki desktop**: *Tools → Add-ons → Get Add-ons…* → paste add-on code **`2055492159`** (AnkiConnect) → *Install* → restart Anki.
2. Leave Anki running. Yomitan talks to it over `http://127.0.0.1:8765`.
3. Yomitan dashboard → **Anki** → toggle **Enable Anki integration** ON.
4. Configure:
   - **Card template:** start with the **Lapis** card model (or donkuri's fork). Both are community standards designed for Yomitan's field set (expression, reading, gloss, sentence, audio, pitch).
   - **Deck:** your mining deck (e.g. `Learner::Mining`) — create it in Anki first (deck name with `::` makes it a sub-deck).
   - **Note type:** the Lapis note type after you import it.
   - **Field bindings:** map Yomitan's `{expression}` `{reading}` `{glossary}` `{sentence}` `{audio}` `{pitch-accents}` to the matching Lapis fields.
5. Hover a word → press `+` → it appears in your mining deck after Anki syncs.

Optional: install the **Local Audio Server** companion (linked from Yomitan docs) to bake offline NHK / Forvo pitch audio into mined cards.

---

## 4. Daily-use cheatsheet

Once wired, the workflow is four interactions:

| Key / action | Does |
|---|---|
| **Hover word with `Shift` held** | Opens the popup over the word under your cursor. (No-modifier hover is configurable in *Settings → General → Scan input modifier*.) |
| **Mouse-wheel inside popup** | Walks forward / back through entries — Yomitan parses the *whole sentence*, not one word. |
| **Click `+` (or `Alt+e`)** | Mines the current entry to your mining deck. |
| **Click `🔊`** | Plays the word's audio. |
| **`Esc`** | Dismisses the popup. |

Drill the muscle memory of **try → hover → mine**. Hovering *before* trying is the crutch trap — same anti-pattern as romaji-on-every-kana.

---

## 5. Sentence-mining workflow (Module 03+)

From Module 03 onward, daily reading is 5–10 min of light native material — NHK News Web Easy, a tweet, a YouTube comment. The rule:

1. Read a sentence with no hover. Note where you stall.
2. Hover the word that broke comprehension. **One hover per stall.**
3. If it looks worth keeping (recognisable kanji, frequency rank under ~10 k, useful for daily life) → `+`.
4. Otherwise: keep reading. Not everything needs mining.

Target: ~5 mined words per session, not 25. Cards you saw once and never again belong in `suspended`.

---

## 6. Optional: 10ten Japanese Reader (Safari + auto-furigana)

If you're on Safari, or you want a furigana-everywhere mode for material you'd otherwise close (a Wikipedia article, a long forum thread, signage on your phone), install **10ten Japanese Reader** alongside Yomitan:

- Available for Chrome / Firefox / Safari.
- Has the same on-hover popup as Yomitan, plus a toggleable **"add furigana to all kanji on page"** mode — that is the literal "overline the spelling" feature you originally asked about.

**Caveat — this is crutch mode.** Auto-furigana short-circuits kanji recognition because your eye drops to the kana. Use it deliberately, not by default:

- ✅ Reading a news article today that you'd otherwise abandon.
- ✅ Real-world signage / menus on a phone in Japan.
- ❌ Anything that is meant to be **study material**: NHK Easy, Comprehensible Japanese transcripts, mined sentences, Module dialogues.

Turn it **off** at the end of the session. Default state: off.

---

## 7. Troubleshooting

- **Popup doesn't appear** — *Settings → General → Scan input modifier*: default is `Shift + hover`. Also confirm the page isn't a PDF or `chrome://` URL; Yomitan can't run on either.
- **"Anki connection failed"** — Anki desktop must be running with AnkiConnect installed. On macOS with strict firewall settings, allow Anki to bind `localhost:8765`.
- **Pitch accent missing from popup** — Kanjium dictionary isn't imported or isn't enabled. Re-check §2.
- **Mining creates blank cards** — field bindings in §3 step 4 aren't mapped. Re-open *Anki* tab in the Yomitan dashboard, map each `{…}` field.
- **Wrong reading for a word** — Yomitan's morphological parser is usually correct, but kanji with multiple readings (上, 行, 生) can mis-parse in isolation. Hover the whole sentence; scroll inside the popup to find the right segmentation.

---

## What this file does NOT replace

- The curriculum. Yomitan accelerates *reading*; you still need active recall (Anki), output (tutor sessions or AI conversation), and pitch drilling (Kotu / Dogen).
- Stroke-order practice for kana — that lives in [`modules/00-writing-systems/kana-guide.html`](../modules/00-writing-systems/kana-guide.html).
- It is *not* a furigana injector by default. That role belongs to 10ten in its narrow §6 use case.
