# Japanese Conversational-Mastery Knowledge Base — Repository Blueprint

## TL;DR
- **Build a hybrid repo that pairs a polite-first Genki-style grammar spine (Modules 00–06) with an aggressive early introduction of plain form (Module 06, not Module 11) and Krashen-style comprehensible-input listening from week 1** — this is the configuration with the best empirical track record for adult self-learners chasing spoken fluency rather than JLPT certification.
- **Kana-first for ~2 weeks, then no-kanji modules 00–03, then context-tied kanji from Module 04 onward** mapped 1:1 to vocab already in your SRS — this matches the "recognition over production" goal and avoids the WaniKani-style isolated-kanji trap that wastes time for a conversational learner.
- **Tool stack: Anki + Kaishi 1.5k deck + Yomitan + Migaku-style mining + Kotu/Dogen pitch-accent training + Comprehensible Japanese (Yuki) and Nihongo con Teppei for input + 1-on-1 tutor sessions for output**, all glued together by versioned Markdown/JSON files in a single repo Claude Code can extend deterministically.

---

## 1. Executive Summary — Pedagogical Rationale

### 1.1 The conversational-mastery goal changes everything

Almost every standard Japanese curriculum (Genki I/II, Minna no Nihongo, Tobira) was designed for a 2-year university classroom whose dominant assessment is JLPT-style reading and writing. They share three biases that actively slow adult conversational learners:

1. **Polite ます-form is taught first and plain form is delayed by ~6 months** (Genki introduces plain non-past around Lesson 8, plain past around Lesson 9). Real spoken Japanese between friends, family, and colleagues-after-hours is overwhelmingly plain form, so learners who only know ます-form sound stiff and — more critically — fail to **understand** native speakers, because almost every relative clause and subordinate clause uses plain form regardless of register.
2. **Reading and kanji absorb disproportionate time** for someone whose goal is talking. The Japanese Complete comparative analysis (hake_hayashi, japanesecomplete.com, 2019) calculates that "after 2 years of study with Genki I and Genki II, one will know about 320 kanji, 250 verbs, 1700+ nouns, and be sensitive to about 260 unique grammar points" — heavy on nouns and reading, light on verbal automaticity.
3. **Pitch accent is barely mentioned.** Most textbooks teach you to sound like a robot reading a kana chart.

The repo therefore makes three opinionated departures from textbook orthodoxy:

- **Polite-first but plain-form-fast.** Modules 01–05 use ます/です so the learner can use what they learn in tutor sessions immediately. Module 06 introduces plain forms aggressively, and from Module 07 onward everything is taught in *both* registers simultaneously, with the casual register marked as primary for listening comprehension and the polite register marked as primary for output.
- **Comprehensible input from Day 1.** Nihongo con Teppei *Beginners* and Yuki's *Comprehensible Japanese* (cijapanese.com) are added to the daily routine in Module 00, not at the end. The brain needs hours of audio exposure before output is forced.
- **Pitch accent is taught from Module 00**, not deferred. Many learners' L1s impose first-syllable intensity stress unless explicitly trained — this is by far the single biggest accent-killer.

### 1.2 Why these specific module boundaries

The 13-module structure follows the "verb-form complexity ladder" that emerges from comparing Genki I/II, Minna I/II, Tobira, Tae Kim, and Cure Dolly. It maps directly to JLPT N5→N4→N3 surface coverage without using JLPT as the organising principle. The ordering deviates from Genki in three places worth flagging:

- **Existence verbs (あります/います) before adjectives.** Genki agrees. Minna agrees. Cure Dolly's "Organic Japanese" framework explicitly grounds the whole grammar in the が-marked existence/identity contrast, which means an early, deep treatment pays compounding interest.
- **Te-form as its own module (05).** Te-form is the load-bearing pillar of the entire grammar. Tofugu calls it "grammatical glue that holds everything together"; the SLJ FAQ catalogues 11+ distinct grammatical uses. It deserves a dedicated 4–6 week module rather than being scattered across three Genki chapters.
- **Plain forms (Module 06) before sentence-ending particles (Module 07).** You cannot use よ/ね/な/かな naturally without knowing plain form, because polite-form + な sounds wrong.

### 1.3 L1 transfer — pronunciation prognosis

L1 transfer is real and should be addressed early. Every learner brings a different phonological starting kit: some features of their first language will be strong advantages for Japanese, others will be traps.

This curriculum ships with two example L1-transfer files:

- `pronunciation/07-hungarian-transfer-notes.md` — for Hungarian L1 speakers (advantages: phonemic geminate consonants, phonemic vowel length, alveolar tap [ɾ]; traps: Japanese /e/ and /u/, pitch-accent intensity transfer)
- `pronunciation/08-german-swiss-transfer-notes.md` — for German / Swiss-German speakers (advantages: Swiss German consonant length, [ç] for ひ; traps: uvular /r/ for German speakers)

Forkers with other L1s should add their own file using the same structure: vowel-inventory comparison, consonant traps, and prosody/pitch-accent contrasts with citations to phonological literature where available.

The two bundled files can serve as models regardless of the reader's own L1. The core principle applies universally: drill pitch accent from week 1, since most L1s impose intensity-based stress that overrides Japanese pitch if left unchecked.

---

## 2. Directory Tree

```
japanese-kb/
├── README.md
├── INDEX.md
├── CLAUDE.md                              # conventions for Claude Code
├── ROADMAP.md                             # 6 + 12-month plan
├── progress/
│   ├── progress.md                        # rolling log
│   ├── weekly-checkin-template.md
│   ├── milestones.md
│   └── tutor-lesson-log.md
├── pedagogy/
│   ├── 00-philosophy.md
│   ├── 01-polite-vs-plain-strategy.md
│   ├── 02-input-vs-output-balance.md
│   ├── 03-srs-strategy.md
│   ├── 04-shadowing-protocol.md
│   ├── 05-self-talk-protocol.md
│   └── 06-ai-conversation-prompts.md
├── pronunciation/
│   ├── 00-overview.md
│   ├── 01-mora-and-timing.md
│   ├── 02-the-five-vowels.md
│   ├── 03-tricky-consonants.md            # り、つ、ふ、ひ、し、ち、じ
│   ├── 04-long-vowels-and-sokuon.md
│   ├── 05-pitch-accent-intro.md
│   ├── 06-pitch-accent-four-patterns.md
│   ├── 07-hungarian-transfer-notes.md
│   ├── 08-german-swiss-transfer-notes.md
│   ├── 09-minimal-pairs.csv
│   └── 10-pitch-drills.json
├── modules/
│   ├── 00-writing-systems/
│   ├── 01-copula-basics/
│   ├── 02-existence-and-location/
│   ├── 03-adjectives/
│   ├── 04-verbs-present-polite/
│   ├── 05-te-form/
│   ├── 06-past-and-plain-forms/
│   ├── 07-casual-and-sentence-particles/
│   ├── 08-potential-volitional-conditional/
│   ├── 09-giving-receiving/
│   ├── 10-passive-causative/
│   ├── 11-keigo-conversational/
│   └── 12-advanced-conversation/
├── vocab/
│   ├── README.md
│   ├── schema.json
│   ├── tier-1-core-300.csv
│   ├── tier-2-expand-700.csv
│   ├── tier-3-fluency-1500.csv
│   ├── greetings-and-fixed-phrases.csv
│   ├── numbers-and-counters.csv
│   ├── time-expressions.csv
│   ├── pitch-accent-overlay.csv
│   └── anki-export/
│       ├── core-300.apkg.notes.md
│       └── export-instructions.md
├── kanji/
│   ├── README.md
│   ├── schema.json
│   ├── policy.md
│   ├── order.md
│   ├── kanji-by-module.csv
│   ├── kanji-master.json
│   └── mnemonics/
│       └── mnemonic-template.md
├── grammar-reference/
│   ├── particles-index.md
│   ├── conjugation-tables.md
│   ├── irregularities-cheatsheet.md
│   ├── common-mistakes.md
│   └── glossary.md
├── listening/
│   ├── README.md
│   ├── resources-by-level.md
│   ├── podcast-rotation.md
│   ├── youtube-rotation.md
│   ├── shadowing-targets.md
│   └── drama-and-anime.md
├── output-practice/
│   ├── self-talk-prompts.md
│   ├── tutor-prep-templates.md
│   ├── ai-conversation-prompts.md
│   └── dialogue-bank.md
└── tools/
    ├── anki-setup.md
    ├── yomitan-setup.md
    ├── migaku-setup.md
    ├── kotu-and-dogen.md
    ├── ipad-pencil-handwriting.md
    └── mac-japanese-input.md
```

Each `modules/NN-*` folder contains: `00-overview.md`, one `.md` per grammar concept, `dialogues.md`, `exercises.md`, `self-talk.md` (M01+), `kanji-introduced.md` (M04+), and `module-vocab.json`.

---

## 3. File-by-File Content Outlines

### 3.1 Root-level meta files

**`README.md`** — One-page orientation. *What this repo is*: a 13-module Japanese curriculum aimed at conversational mastery, not JLPT. *Who it's for*: any adult learner focused on conversational competence. *How to use it*: pick the active module from `INDEX.md`, follow `00-overview.md`, do exercises, log in `progress/progress.md`. *Daily routine*: 15 min Anki + 20 min current-module + 20 min listening + 10 min shadowing/output ≈ 65 min/day. *Dependencies*: Anki, Yomitan, Kaishi 1.5k, uv, optional Migaku.

**`INDEX.md`** — Linear table: Module → status (locked/active/done) → estimated weeks → key grammar points → cumulative vocab/kanji counts → milestone unlocked.

**`CLAUDE.md`** — The Claude Code contract:
- **Markdown frontmatter**: every `.md` file starts with `--- module: 04 file: 02-masu-form lang_focus: grammar kanji_level: 0-30 last_updated: YYYY-MM-DD ---`.
- **Example sentence format**: three lines — kana, kanji-with-furigana (only if kanji has been introduced), English gloss. Romaji forbidden except in `pronunciation/`.
- **Vocab JSON schema** (see §3.6).
- **Kanji JSON schema** (see §3.7).
- **Linking rules**: every grammar point cross-links every example word to its vocab entry by `id`.
- **Furigana convention**: HTML `<ruby>漢字<rt>かんじ</rt></ruby>` or the Markdown shorthand `{漢字|かんじ}`.
- **Claude Code permissions**: may scaffold new module folders, add vocab rows, regenerate `kanji-by-module.csv` from `kanji-master.json`. Must NOT rewrite `pedagogy/*` files without explicit prompt.
- **Validation**: `python tools/validate.py` checks vocab JSON conforms to schema and every example uses only kanji from prior modules.

**`ROADMAP.md`** — See §5.

### 3.2 `progress/`

**`progress.md`** — Append-only log: date, module, what was studied, Anki retention rate, lesson notes.

**`weekly-checkin-template.md`** —
```
## Week of YYYY-MM-DD
- Module:
- Hours studied:
- Anki: new cards / total reviews / retention %
- Listening: hours + sources
- Output: minutes of self-talk / tutor session / AI chat
- New vocab mined:
- Win of the week:
- Friction:
- Next week focus:
```

**`milestones.md`** — Concrete observable milestones:
- M1 (end M00): read any kana text aloud at >40 mora/min with no chart.
- M2 (end M01): introduce yourself unprepared for 60 seconds.
- M3 (end M03): describe a room and three people in it.
- M4 (end M04): describe daily schedule (~10 sentences) unprepared.
- M5 (end M05): ask for things in a shop, give instructions, describe what someone is doing.
- M6 (end M06): narrate yesterday for 2 minutes; understand plain-form subordinate clauses in audio.
- M7 (end M07): 5-min casual conversation on a familiar topic with a patient native.
- M8 (end M08): express wants, hypotheticals, possibilities.
- M9 (end M09): describe favours given/received without direction confusion.
- M10 (end M10): understand passive in news headlines.
- M11 (end M11): survive restaurant/train/hotel in Japan recognising staff keigo.
- M12 (end M12): 10+ min unprepared conversation with natural aizuchi.

**`tutor-lesson-log.md`** — One row per lesson: date, tutor, topics, mistakes flagged, homework. Claude Code can inject flagged mistakes into a review queue deck.

### 3.3 `pedagogy/`

**`00-philosophy.md`** — Four operating principles:
1. Comprehensible input from day 1 (Krashen i+1).
2. Output constrained until Module 04, then expanded aggressively.
3. SRS is for vocab and kanji recognition, **not** for grammar (acquired through reading + listening + targeted drills).
4. Pitch accent is learnt as perception skill first, production second.

**`01-polite-vs-plain-strategy.md`** — Explicit treatment of the debate. Position: polite-first in M01–M05 because it lets the learner use what they know in tutor sessions immediately; plain-form crash course in M06 because by then they have enough exposure to recognise it everywhere. Plain form *for input* from day 1 via Comprehensible Japanese videos. Concrete rule: from M06, every new structure is shown in side-by-side polite/plain tables.

**`02-input-vs-output-balance.md`** — Recommended weekly minutes by module: M00–01 input 80% / output 20%; M02–04 70/30; M05–07 60/40; M08+ 50/50. The Migaku editorial position that learners should "graduate from textbooks as soon as possible" aligns with the M05–M06 inflection.

**`03-srs-strategy.md`** — Anki configuration recipe: new cards/day = 10 (M00–04), then 15; max reviews/day = 200; FSRS scheduler default. Two decks: `Japanese::Core` (Kaishi 1.5k + module-vocab) and `Japanese::Mining` (Yomitan-added). One kanji deck `Japanese::Kanji` (recognition only; "what does this kanji mean?" prompt; reading on back). Suspend mined cards seen only once in 2 weeks of immersion. Burying related cards: ON.

**`04-shadowing-protocol.md`** — 10 min/day from Module 02 onward. Source: Comprehensible Japanese (beginner playlist). 5-step protocol: (1) listen once, eyes closed; (2) listen with transcript; (3) shadow with transcript at ~0.5s delay; (4) shadow without transcript; (5) record own voice and compare. The 10-min-daily / Argüelles-interpreter origin is well-documented in shadowing literature (Kanjidon, FluentU).

**`05-self-talk-protocol.md`** — 30 daily prompts (commute, today's lunch, work issue, weekend plan, weather opinion) graded by module. The learner records themselves in Voice Memo for 60s, transcribes into `output-practice/self-talk-prompts.md`.

**`06-ai-conversation-prompts.md`** — Three prompt templates:
- **Conversation partner**: "Act as a Japanese friend with kind patience. Use plain form. Speak at the level of someone who has finished Module N of my curriculum (file attached). If I make a grammar mistake, repeat my sentence back in correct Japanese using ね, then continue naturally. Do not give English unless I ask."
- **Tutor prep**: "Given the topic [X], produce 10 example questions a tutor might ask me in plain Japanese, and 5 prompt answers using only grammar from Modules 00–06."
- **Structured correction**: paste a Japanese paragraph; AI produces a corrected version + 5-bullet mistake summary.

### 3.4 `pronunciation/`

**`00-overview.md`** — Map of the track; 15 min/week M00–01, dropping to 10 min/week thereafter, plus 5 min/day shadowing.

**`01-mora-and-timing.md`** — Mora as the unit of duration. Clap-one-beat-per-mora drilling. Drill words: にっぽん (4 beats), おばあさん (5), きって (3). The moraic nasal ん, geminate marker っ, and long vowels each count as one beat.

**`02-the-five-vowels.md`** — IPA values + L1-transfer notes (see §1.3 and `pronunciation/07-` / `pronunciation/08-` for examples). Drills for the /u/ trap (compressed, not protruded): record yourself saying すみません without rounding lips.

**`03-tricky-consonants.md`** — For each of り, つ, ふ, ひ, し, ち, じ: IPA, mouth diagram (text description), 6 minimal-pair drills, L1-transfer note (see `pronunciation/07-` and `pronunciation/08-` for examples). Special handling for ふ (substitute labiodental [f] is a common error for many L1 speakers).

**`04-long-vowels-and-sokuon.md`** — Minimal pairs: おばさん/おばあさん, ゆき/ゆうき, きて/きって, さか/さっか, いえ/いいえ. Pre-loaded into `09-minimal-pairs.csv`.

**`05-pitch-accent-intro.md`** — Three reasons pitch matters more than textbooks admit: (1) understandability gap on phone/noisy environments; (2) lexical minimal pairs (橋 hashi LH vs 箸 hashi HL vs 端 hashi LH+drop on particle); (3) much harder to relearn later. The Wikipedia pitch-accent article states "incorrect pitch accent is a characteristic of a 'foreign accent' in Japanese."

**`06-pitch-accent-four-patterns.md`** — Heiban (平板, flat, no drop), Atamadaka (頭高, drop after mora 1), Nakadaka (中高, drop somewhere in middle), Odaka (尾高, drop only on following particle). Dictionary notation: 0 = heiban, n = drop after mora n. The heiban/odaka isolation-ambiguity fact (they sound identical until a particle follows). MieruTone's training framework explicit.

**`07-hungarian-transfer-notes.md`** — Detailed phonological prognosis for Hungarian L1 speakers, with drills. Emphasis on suppressing first-mora intensity (Hungarian fixed-stress interference per Szeredi 2010). Drill: pronounce はし three ways (HL, LH, LH+drop) with deliberately equal loudness on every mora.

**`08-german-swiss-transfer-notes.md`** — Detailed phonological prognosis for German / Swiss-German speakers, with drills. Swiss German alveolar trill /r/ is closer to ら than Standard German uvular /ʁ/. German [ç] in *ich* is an exact match for Japanese ひ.

**`09-minimal-pairs.csv`** — Schema: `word_a, word_a_meaning, word_b, word_b_meaning, contrast_type (vowel_length|sokuon|pitch|consonant), audio_a_filename, audio_b_filename, module_first_useful`. ~120 rows.

**`10-pitch-drills.json`** — Pre-built drills: each of the four patterns × 20 example words with mora count, drop position, particle behaviour. Anki-importable.

### 3.5 `modules/` — Per-module content highlights

#### Module 00 — Writing Systems
- Hiragana before katakana. Order: vowels → consonant rows (one/day for 5 days) → dakuten/handakuten/yōon (3 days) → katakana (7 days).
- Mnemonics: reference Tofugu's free hiragana mnemonics rather than reinventing.
- Practice goal: 40 mora/min sight-reading by end of week 2 (drill in realkana.com or Anki kana deck).
- Katakana loanword traps: ー marker, the 3-mora limit pattern in Japanised English, small vowels for foreign sounds (ファ, ティ, ウィ). No kanji.

#### Module 01 — Copula Basics
- **です** as polite copula: identity statement, not "to be" (Tae Kim's distinction).
- **じゃない / ではない / じゃありません / ではありません** — register table.
- **は** as topic marker (not subject). Use Cure Dolly's framing: は presents a topic; the underlying が-marked subject may be elided.
- **か** for questions.
- **の** for possession and noun-modification.
- **これ / それ / あれ / どれ** — partial preview (full in M02).
- Dialogues: 自己紹介, asking about photos, identifying objects.
- Common mistake: ✗ いきますです (using です with verbs). Flag and forbid.
- 60–80 vocab. No kanji.

#### Module 02 — Existence & Location
- **あります** (inanimate) vs **います** (animate). Edge cases: plants, robots, vehicles ("います for taxis you're waiting for" — agency-based intuition).
- **に** (existence/static) vs **で** (action location). Drill: ほんやで ほんを かいます vs ほんやに ほんが あります.
- **が あります／います** — は vs が contrast.
- Position words (うえ、した、まえ、うしろ、なか、そと、よこ、となり、ちかく、あいだ). Note noun status: テーブルのうえ, not テーブルうえ.
- Full こそあど: これ/それ/あれ/どれ, この/その/あの/どの, ここ/そこ/あそこ/どこ, こちら/そちら/あちら/どちら, こんな/そんな/あんな/どんな.
- ~80 vocab. No kanji.

#### Module 03 — Adjectives
- **い-adjectives**: built-in present tense (たかい = "is high"); negative たかくない; do NOT add です-equivalent inflection (✗ たかいだ).
- **な-adjectives**: behave like nouns; require だ/です; modify with な (きれいな はな).
- **いい → よい** irregularity, past よかった, negative よくない.
- **きれい** and **ゆうめい** look like い-adjectives but are な-adjectives — flag.
- Comparatives: より, のほうが, いちばん.
- ~80 vocab. No kanji.

#### Module 04 — Verbs (present polite) and First Kanji
- **Verb groups** with modern terminology: Group 1 (godan / u-verbs), Group 2 (ichidan / ru-verbs), Group 3 (irregular: する, くる). Identification rule: i/e-row-before-る for Group 2; godan ends in u/tsu/ru/ku/gu/su/nu/bu/mu.
- **ます / ません / ました / ませんでした**.
- Object **を**; direction **へ** vs **に**; **から / まで**; **で** as means/instrument.
- Time expressions; days of the week with こん/せん/らい/さ prefixes.
- Counters: 5 generic + 5 specific (人, つ, 個, 本, 枚, 時, 分, 円, 回, 歳).
- **First kanji (~30)**: 一二三四五六七八九十百千万 (numbers); 日月火水木金土 (days); 人, 私, 何, 行, 食, 飲, 見, 聞, 来, 大, 小. Each tied to vocab the learner already knows.
- ~120 vocab.

#### Module 05 — Te-form
- The 8-pattern conjugation table by Group 1 ending; いく → いって is the one godan exception.
- Group 2: replace る with て. Irregulars: して, きて.
- Uses taught in order: (1) sequencing; (2) ～てください request; (3) ～ています progressive; (4) ～てもいい permission; (5) ～てはいけません prohibition; (6) ～ている resultant state for ある/しる/もつ/けっこんする; (7) ～てあげる/くれる/もらう preview (full in M09); (8) ～てしまう / ちゃう; (9) ～ておく / とく; (10) ～てみる; (11) ～ていく / てくる direction.
- Common mistake: ✗ いく → いいて, → ✓ いって.
- **Motion-verb trap**: いっています ≠ "going" but "has gone and is still there". For "is going right now", use いくところです.
- ~150 vocab. ~25 new kanji.

#### Module 06 — Past Tense & Plain Forms
- **Plain non-past = dictionary form**; plain negative = ない-form; plain past = た-form (parallels te-form rules); plain past negative = なかった.
- だ vs です. だ is dropped or replaced with な before certain endings (な-adj before noun; なんだ for explanation).
- ない-form irregularity: ある → ない (not ✗ あらない).
- い-adj past: たかかった (not ✗ たかいだった). Negative past: たかくなかった.
- な-adj/noun past: しずかだった, がくせいだった.
- **Register-switching exercises** in both directions: take 10 polite sentences → plain; take 10 plain dialogues from Comprehensible Japanese → polite.
- The gateway module to native input.
- ~150 vocab. ~30 new kanji.

#### Module 07 — Casual Speech & Sentence-Ending Particles
- ね — seeking shared feeling/agreement; falling tone.
- よ — giving new information; soft falling tone.
- よね — info + check.
- な / なあ — masculine, reflective, talking to self; attaches to plain.
- かな — "I wonder if…"
- か — in casual often dropped; rising intonation alone suffices.
- の — questioning/explanatory ending in casual.
- んだ / なんだ — explanatory.
- Contractions: ～てしまう → ～ちゃう; ～ておく → ～とく; ～ては → ～ちゃ; ～なくては → ～なくちゃ; ～ない → ～ん; ～れば → ～りゃ.
- Particle drop (は, を, に sometimes dropped in fast casual).
- Gendered speech: わ (feminine softener), ぜ/ぞ (masculine assertive), かしら (feminine wondering). Contemporary speech is more fluid than older textbooks suggest.
- Common mistake: ねよ flows wrongly; よね is the natural combination.
- ~120 vocab. ~30 new kanji.

#### Module 08 — Potential / Volitional / Conditional
- Potential: Group 2 → られる; Group 1 → -eru column (飲む → 飲める); する → できる; くる → こられる. Note ら抜き (Group 2 られる → れる in casual).
- Object marker shift: を often → が with potential (日本語が話せる).
- Volitional: -masu → -mashō; plain Group 2 → よう, Group 1 → -ou (行こう); する → しよう; くる → こよう. +とおもう = "I think I'll…"; +とする = "about to…".
- たい-form: い-adjective behaviour; subject restriction (own desires only; 3rd person uses たがる or そう).
- Four conditionals: たら, ば, なら, と — explicit contrast table:
  - たら: general "when/if", widest applicability, often default.
  - ば: hypothetical, often fixed lexical patterns; ～さえすれば.
  - なら: contextual "if it's the case that…"; topic-like.
  - と: automatic, generic, scientific — A always → B.
- ~150 vocab. ~30 new kanji.

#### Module 09 — Giving / Receiving
- **uchi / soto** framework first (Tofugu's framing).
- あげる: I-or-uchi → soto, or soto → soto.
- くれる: soto → I-or-uchi.
- もらう: I-or-uchi ← anyone. に (direct contact) vs から (institution).
- Honorific tier: さしあげる (rarely used modernly; flag social risk), くださる (ubiquitous; ください is its imperative), いただく (most useful for a foreigner).
- ～てあげる / くれる / もらう as favours. ～てあげる toward someone of higher status sounds presumptuous; use ～させていただく in business.
- ~80 vocab. ~20 new kanji.

#### Module 10 — Passive / Causative / Causative-Passive
- Passive: Group 2 → られる; Group 1 → -areru.
- Direct passive ("X was V-ed") vs **suffering / adversative passive** (uniquely Japanese): 雨にふられた "I was rained on"; 子供になかれた "the child cried on me" (feeling-affected-by).
- Causative: Group 2 → させる; Group 1 → -aseru. Two readings ("make X do" / "let X do") disambiguated by に vs を on the causee.
- Causative-passive: -aserareru / -saserareru, often contracted to -sareru. "I was made to do X." Very common in venting/complaint speech.
- ~100 vocab. ~25 new kanji.

#### Module 11 — Conversational Keigo
- Goal: **comprehension** of keigo from shop staff, train announcements, hotel, restaurants — and **production** of just enough to navigate polite-stranger interactions.
- 尊敬語 (sonkeigo). Key irregulars: いらっしゃる (= いる/くる/いく), なさる (= する), めしあがる (= たべる/のむ), おっしゃる (= いう), ごらんになる (= みる), ぞんじる (= しる).
- 謙譲語 (kenjōgo). Irregulars: まいる, いたす, いただく, もうす, はいけんする.
- Templates: お/ご + verb-stem + する (humble) / になる (respectful).
- Shop-staff phrases to **recognise but not produce**: いらっしゃいませ, よろしいでしょうか, おまちください, おたばこのほうは, ～でございます, おそれいりますが.
- ~120 vocab. ~25 new kanji.

#### Module 12 — Advanced Conversational Nuance
- **Aizuchi** (back-channels): うん, はい, そうですね, ええ, なるほど, ほんと(に), まじで, へえ. Critical — silence reads as disagreement/inattention.
- **Onomatopoeia**: ぎおんご (giongo: わんわん, ざあざあ) vs ぎたいご (gitaigo: きらきら, わくわく, どきどき).
- Common idioms: 気になる/気にする/気がする (different! ki ni naru = bothers/curious; ki ni suru = mind/worry; ki ga suru = have a feeling), 仕方がない, よろしく.
- Modern slang: やばい (wide semantic field), えぐい, めっちゃ, ガチ, ウケる.
- Regional preview (Kansai-ben): だ → や (そや, ほんま), い-adj past たかかった → たこうた, negative ない → へん.
- Discourse markers: えーと, あのー, まあ, でも, やっぱり.
- Soft language / hedging: ～かもしれない, ～と思う, ～じゃないかな, ～みたい, ～っぽい.
- Open module — Claude Code may extend with new topics ad hoc.

### 3.6 `vocab/`

**`schema.json`** — JSON Schema (draft-07) per entry:
```json
{
  "id": "string (slug, e.g. 'taberu')",
  "kana": "string",
  "kanji": "string|null",
  "reading": "string (hiragana with okurigana)",
  "pos": "noun|verb-godan|verb-ichidan|verb-irregular|i-adj|na-adj|adv|particle|conj|interj|counter",
  "transitivity": "tr|intr|null",
  "english": ["string"],
  "pitch_accent": { "pattern": "heiban|atamadaka|nakadaka|odaka", "drop_after_mora": 0 },
  "example_sentences": [{ "kana": "...", "kanji": "...|null", "english": "..." }],
  "module_introduced": 0,
  "tier": 1,
  "frequency_rank_bccwj": null,
  "notes": null,
  "tags": []
}
```

**`tier-1-core-300.csv`** — 300 highest-priority conversational words:
- All ~46 greetings / fixed phrases (おはよう, こんにちは, こんばんは, さようなら, ありがとう, すみません, ごめんなさい, おねがいします, いただきます, ごちそうさま, etc.).
- ~30 pronouns + demonstratives.
- ~40 numbers, days, time.
- ~50 most common verbs (JLPT N5 verb subset).
- ~30 i-adjectives + ~20 na-adjectives.
- ~40 family / body / food / house.
- ~20 question words, conjunctions, frequency adverbs.
- ~20 particles (they need pitch accent + SRS too).
- Sourced by intersecting (a) JLPT N5 list (~800 words; trimmed aggressively to ~250 most conversational), (b) Kaishi 1.5k frequency-ordered deck (donkuri's modern Tango/Core successor), (c) BCCWJ spoken-corpus top words.

**`tier-2-expand-700.csv`** — JLPT N4-ish + remaining Kaishi 1.5k + topical buckets: work (15 IT / office terms), hobbies, feelings, opinions, travel.

**`tier-3-fluency-1500.csv`** — Tango N3 deck + BCCWJ top 3500. Brings total to ~2500 — the practical conversational-fluency floor.

**`pitch-accent-overlay.csv`** — for every Tier 1+2 word, pattern + drop-after-mora. Sourced from NHK Accent Dictionary lookups or the open Kanjium accent database.

**`anki-export/export-instructions.md`** — How to regenerate Anki decks from CSVs. A Python script `tools/export_to_anki.py` (Claude Code to author) converts each tier into `.apkg` files. Note type: front = kana (with audio), back = kanji form + English + pitch graph + example sentence + module tag.

### 3.7 `kanji/`

**`policy.md`** —
- **Recognition only**, no handwriting, no RTK keyword-to-kanji production. Kanji writing is a separate optional skill, not a prerequisite for spoken fluency.
- **No isolated kanji study.** Kanji are introduced only when the learner already knows a vocab word using them. This avoids the WaniKani problem of "learning readings out of context that don't stick" (documented across the donkuri immersion guide and the LearnKanji guide).
- **Target**: ~400 kanji by end of Module 08; ~800 by end of Module 12. (Compare: Genki I+II = ~317 per japanesecomplete.com.)

**`order.md`** — Justification: drive by vocab frequency, not JLPT level or radical complexity. Start with high-frequency vocab-grounded kanji. Use Tofugu/Wanikani radical mnemonics where they help, skip the SRS-per-radical step. Re-evaluate at end of Module 08.

**`kanji-master.json`** — Array of entries:
```json
{
  "kanji": "食",
  "meaning_primary": "eat / food",
  "meaning_secondary": ["meal"],
  "on_yomi": ["ショク", "ジキ"],
  "kun_yomi": ["た.べる", "く.う", "く.らう"],
  "stroke_count": 9,
  "radicals": ["食"],
  "mnemonic": "A roof (𠆢) over a good (良) meal — eating.",
  "vocab_using": ["taberu", "shokuji", "shokudou", "yuushoku"],
  "example_sentence": { "kanji": "ばんごはんを食べました。", "kana": "ばんごはんを たべました。", "english": "I ate dinner." },
  "module_introduced": 4,
  "notes": "First introduced as た from たべる."
}
```

**`kanji-by-module.csv`** — Flat denormalised, sorted by introduction order. Columns: order, kanji, primary_meaning, on, kun, module.

**`mnemonics/mnemonic-template.md`** — Guidance: visual, short, weird is better; reuse stock characters (e.g. "the developer" = 人; "the cafe" = 口).

### 3.8 `grammar-reference/`

- **`particles-index.md`** — Alphabetical: は, が, を, に, へ, で, と, から, まで, より, の, も, や, か, ね, よ, わ, ぞ, ぜ, さ, な, ばかり, だけ, しか, ほど, くらい, など, でも, さえ, こそ, って, ったら. Each: core function, examples, common mistakes, module of introduction.
- **`conjugation-tables.md`** — Master tables: copula (です/だ across 8 forms), godan, ichidan, irregulars, i-adj, na-adj, across non-past/past/negative/te/conditional/potential/volitional/passive/causative.
- **`irregularities-cheatsheet.md`** — いく → いって; ある → ない; いい → よかった/よくない; する → して/した/しない; くる → きて/きた/こない; だ → な/で/じゃ.
- **`common-mistakes.md`** — Running catalogue built from tutor sessions + AI corrections. Append-only.
- **`glossary.md`** — Terminology: mora, particle, copula, godan, ichidan, te-form, sokuon, dakuten, yōon, plain form, polite form, honorific, humble, transitive (他動詞), intransitive (自動詞), aspect, copular vs verbal sentence, topic vs subject.

### 3.9 `listening/`

**`resources-by-level.md`** — Tiered with explicit module gating:
- **From Module 00 (Day 1)**: *Comprehensible Japanese* (Yuki, cijapanese.com) — Complete Beginner playlist. Per Tofugu's review: "Yuki uses simple drawings and pictures to illustrate her points. She speaks slowly and clearly, repeating important words and using synonyms." The single most important early-input resource.
- **From M01–02**: *Nihongo con Teppei for Beginners* — ~4-min episodes, daily life.
- **From M04**: *Game Gengo* (YouTube) — gaming-themed grammar, suits a software developer.
- **From M05**: *Japanese with Shun* podcast (N5–N3) with transcripts.
- **From M06**: *YUYU Nihongo Podcast* (Yusuke); *Comprehensible Japanese* Intermediate (528 videos at ~JLPT N3 level per the CIJapanese site); *Sayuri Saying* (YouTube, natural shadowing material).
- **From M07**: drama — recommended starter 凪のお暇 (*Nagi no Oitoma*) for slow naturalistic dialogue, or *Midnight Diner: Tokyo Stories*. Avoid anime as primary input until later — stylised speech and masculine-coded sentence-final particles distort output.
- **From M08–09**: native-pace interest podcasts (e.g. *Rebuild.fm* for technical learners).
- **From M10+**: NHK *News Web Easy* → NHK News.
- **Avoid until late**: Terrace House (heavy contractions), variety shows, 関西弁 content.

**`podcast-rotation.md`** — Weekly: 4 episodes at current level + 1 episode one level up (i+1) + 1 re-listen of last week's hardest.

**`youtube-rotation.md`** — Channels with subs + difficulty rating: Comprehensible Japanese, Japanese with Shun, Onomappu, Daily Japanese with Naoko, Kaname Naito, ToKini Andy (when wanting English explanations), Dogen (pitch accent), Game Gengo.

**`shadowing-targets.md`** — Specific episodes/segments per module.

**`drama-and-anime.md`** — Curated list with difficulty + caveats.

### 3.10 `output-practice/`

**`self-talk-prompts.md`** — 100 prompts graded by module; each tagged with grammar it exercises. E.g. for M06: "Describe yesterday morning to night using ～ました and then plain past."

**`tutor-prep-templates.md`** — Before each tutor lesson: 10-min prep where the learner reads the next module's `dialogues.md`, generates 5 tutor questions, lists 3 concepts to correct.

**`ai-conversation-prompts.md`** — See §3.3.

**`dialogue-bank.md`** — Recurring scenarios: ordering coffee, dentist, bank account, tech meetup introduction, explaining software development to non-technical person, declining politely, complimenting, complaining about weather, Swiss vs Japanese food, Hungary.

### 3.11 `tools/`

**`anki-setup.md`** — Mac install from apps.ankiweb.net. Install AnkiConnect (add-on code 2055492159 — required for Yomitan), Japanese Support, FSRS scheduler on, Heatmap optional. Recommended add-ons: AutoReorder, Batch Editing, Edit Field During Review, Kanji Grid.

**`yomitan-setup.md`** — Install Yomitan in Safari/Firefox/Chrome/Edge (Yomitan is officially supported on the latter three). Recommended dictionaries: JMdict (Jitendex), KANJIDIC, Kanjium pitch accent, JPDB frequency. Enable Anki integration pointed at the `Japanese::Mining` deck with the Lapis card model (or donkuri's fork). Optional: Local Audio Server for offline pitch audio.

**`migaku-setup.md`** — Optional sentence-mining from Netflix/YouTube/Crunchyroll. Subscription noted; Yomitan + ManabiDojo for Crunchyroll is a free alternative.

**`kotu-and-dogen.md`** — Kotu.io has a free minimal-pair pitch test. Dogen's Patreon is the de-facto standard for pitch-accent production training; per Dogen's current Patreon page (patreon.com/cw/dogen): "Sign up for the $15 tier here to access my Japanese Phonetics series and Natsumi Sensei's Group lessons!" Schedule: 10 min/day Kotu.io perception training during Module 00–03; switch to Dogen lessons starting Module 04.

**`mac-japanese-input.md`** — System Settings → Keyboard → Input Sources → add Japanese (Romaji). Romaji-to-kana rules. Bind a keyboard shortcut to switch input source. Recommended fonts: Hiragino Sans (system default) and Yu Mincho.

**`ipad-pencil-handwriting.md`** — Optional. Position: handwriting not required for conversational mastery. If desired, Procreate or GoodNotes with Kanji Study app stroke-order reference. Skip until at least Module 06.

---

## 4. Tool Recommendations Summary

| Category | Primary | Secondary | When |
|---|---|---|---|
| SRS | **Anki** | — | Day 1 |
| Beginner vocab deck | **Kaishi 1.5k** | Tango N5/N4 | Day 1 |
| Mining | **Yomitan + AnkiConnect** | Migaku ($) | Module 03 onward |
| Grammar reference | **Tae Kim** + Cure Dolly *Unlocking Japanese* | Tofugu, Bunpro | All modules |
| Textbook (cross-reference) | **Genki I/II** | — | All modules; second opinion |
| Pitch perception | **Kotu.io** | **MieruTone** | Module 00 |
| Pitch production | **Dogen Patreon** ($15/mo, *Japanese Phonetics* tier) | — | Module 04 |
| Beginner input | **Comprehensible Japanese (Yuki)** | Nihongo con Teppei | Day 1 |
| Intermediate input | **YUYU Nihongo Podcast**, **Game Gengo** | Sayuri Saying | Module 05 |
| Output | **1-on-1 tutor** (iTalki or similar marketplace) | AI conversation partner | All modules |
| AI conversation | **Claude / ChatGPT** with curriculum-aware prompt | — | Module 03 |
| Pop-up dictionary | **Yomitan** | jisho.org | All modules |
| Mobile review | **AnkiMobile** ($24.99 one-time, iOS) | AnkiDroid (free) | Day 1 |
| Browser reading | **ttsu Reader** for epubs | — | Module 06 |
| Frequency overlay | **JPDB.io** | BCCWJ frequency dict | Module 04 |

**Do NOT use:**
- **WaniKani** — overpriced, teaches kanji readings out of context, slow. Use mined kanji + recognition-only flashcards instead.
- **Duolingo Japanese** — poor pedagogy, romaji-heavy, useless for conversational goal.
- **Rosetta Stone** — same problems as Duolingo.
- **Anime as primary input** before Module 07 — stylised speech, register-distorting.

---

## 5. Roadmap

### 5.1 Six-month plan (~7 hours/week, ~60 min/day with one rest day)

| Month | Module(s) | Primary outcomes | Listening targets | Anki state |
|---|---|---|---|---|
| 1 | M00 → M01 | Fluent kana sight-reading; self-introduction 60 s | Comprehensible Japanese Complete Beginner, 4× 5-min/wk | Hiragana deck retired; Kaishi 1.5k at 300 |
| 2 | M02 → early M03 | Existence + location + start adjectives; describe a room | + Nihongo con Teppei Beginners, 5× 4-min/wk | ~600 Kaishi |
| 3 | finish M03 → M04 | Verbs polite; first 30 kanji; daily schedule | + Game Gengo 1×/wk | ~900 Kaishi + 30 kanji |
| 4 | M05 | Te-form mastery; instructions, ongoing actions | + Japanese with Shun 2×/wk | ~1100 + 55 kanji + 30 mined |
| 5 | M06 | Plain forms; narrate yesterday; understand casual native input | + YUYU 1×/wk; first casual-form CIJ dialogues | ~1300 + 85 kanji + 80 mined |
| 6 | M07 | Casual speech + particles; first 5-min natural conversation; switch tutor sessions mostly to plain form | Kaname Naito 1×/wk; first drama — start *Nagi no Oitoma* slowly | Kaishi finished + ~120 kanji + ~150 mined |

**End-of-6-month checkpoint:** The learner can (a) hold a 5-min conversation in plain form on familiar topics with a forgiving native, (b) understand ~60% of *Nihongo con Teppei* main podcast, (c) read pure-kana children's content fluently, (d) recognise ~120 kanji in vocab context, (e) have an active vocab of ~1500–1700 words. Approximately strong JLPT N5 / weak N4 on paper, with notably stronger spoken/listening skills than a typical N5 passer.

### 5.2 Twelve-month plan

| Month | Module(s) | Primary outcomes |
|---|---|---|
| 7 | M08 | Potential, volitional, four conditionals |
| 8 | M09 | Giving/receiving with uchi/soto intuition |
| 9 | Consolidation + mining month | No new module. Push Anki mining from drama + podcasts. Tutor mostly Japanese plain/polite mix. Target: 2000 unique words. |
| 10 | M10 | Passive + causative; comprehension breakthrough for news |
| 11 | M11 | Survival keigo (shop / train / restaurant / hotel / clinic) |
| 12 | M12 | Aizuchi, onomatopoeia, hedging, slang preview. Open-ended; Claude Code extends on demand. |

**End-of-12-month checkpoint:** The learner can (a) hold a 15-min unprepared conversation on varied topics, (b) understand ~70% of native-adult podcasts, (c) follow a slice-of-life drama at 0.85× speed with Japanese subs, (d) recognise ~600+ kanji in context, (e) produce both polite and plain registers, (f) survive a 2-week independent trip to Japan. Roughly JLPT N3-grammar / weak-N3-reading / strong-N4-listening — but with notably better spoken Japanese than a typical paper-N3 holder.

### 5.3 Triggers that change the plan

- Anki mature-card retention drops below 85% for 2 weeks → halve new cards/day, don't advance modules.
- Tutor reports over-translation from English → push input ratio +10% and skip output sessions for a week.
- Pitch-accent self-recordings still sound flat at end of Module 03 → escalate Dogen from M04 to M02.
- Learner reaches end of Module 07 ahead of schedule → run M08–M10 in parallel (they don't strongly depend on each other).
- Japan trip booked → prioritise Module 11 (keigo recognition) regardless of current module.

---

## 6. What to Hand to Claude Code

Deliverable: this document plus the following explicit instructions in `CLAUDE.md`:

1. **Scaffold the entire directory tree** above as empty files with frontmatter populated and TODOs in each section.
2. **Populate `vocab/tier-1-core-300.csv`** from the intersection of JLPT N5 vocab + Kaishi 1.5k first 300 cards. Use `schema.json`. Add pitch accent from the Kanjium dictionary.
3. **Populate Module 00 fully** (kana drills, mnemonics referenced not duplicated, minimal-pair drills) — the only module 100% built at scaffold time. All later modules are filled in chapter-by-chapter as the learner advances.
4. **Author `tools/validate.py`** that checks: every kanji in any module's `dialogues.md` exists in `kanji-master.json` with `module_introduced` ≤ that module's number; every vocab `id` referenced from kanji entries exists in a tier CSV.
5. **Author `tools/export_to_anki.py`** to produce three `.apkg` files (`tier-1`, `tier-2`, `tier-3`) and a `kanji.apkg` from the CSV/JSON sources.

This produces a self-extending repo: when the learner finishes Module N, they ask Claude Code "build Module N+1's drills and dialogues based on the overview" and Claude Code reads the conventions in `CLAUDE.md` and produces consistent content.

---

## Recommendations

1. **Start now.** Today, install Anki and the Kaishi 1.5k deck. Single highest-ROI action; happens before the repo is even scaffolded.
2. **In parallel with tutor lessons, add Comprehensible Japanese (Yuki) as daily passive listening.** 10 min/day during commute or cooking. Frame: "let your ears catch up to your mouth."
3. **Tell your tutor your plan.** Show them Module 01's overview. Ask them to drill copula and は in plain conversation for 2–3 weeks rather than rushing ahead.
4. **Schedule pitch-accent perception training from week 1.** 10 min/day on Kotu.io minimal-pair test. Single most-cited "thing I wish I'd done earlier" by intermediate Japanese learners.
5. **At end of Module 05 (~month 4), trial Migaku for 1 week.** If sentence mining from Netflix is comfortable, subscribe; otherwise stay with Yomitan + ManabiDojo.
6. **At end of Module 06, switch tutor session register to predominantly plain form.** This is the gear shift toward real conversational ability. Tell the tutor explicitly.
7. **Plan a 10-day trip to Japan around month 9–10.** Real high-stakes immersion at this point compresses ~3 months of progress into 10 days, and Module 11's keigo content is directly applicable.

## Caveats

- **The plan assumes consistent ~60 min/day, six days/week.** Slips compound; the plan tolerates ±25% time variance per week before modules stretch by more than a week.
- **Pitch accent claims are based on standard Tokyo dialect.** Most native Japanese speakers, including Tokyo natives, have minor regional variation; the goal is "recognisably native-like", not "indistinguishable from a Tokyo native".
- **The L1-specific phonology mappings in `pronunciation/07-` and `pronunciation/08-` are contrastive analysis, not empirical study.** No single published paper covers every L1-to-Japanese transfer combination; the prognoses are well-founded inferences from independently described L1 and L2 systems (Wikipedia phonology articles, Siptár & Törkenczy 2000, Szeredi 2010, Tar 2017) plus general L2-prosody-transfer findings. Treat them as hypotheses to test in the first month.
- **JLPT vocabulary lists are unofficial.** The JLPT explicitly does not publish word lists; the "800-word N5 list" cited widely (e.g. by JLPTSensei, MLC Meguro's 802-word PDF, italki, Tanos.co.uk) is a community-curated approximation. The repo treats it as a useful frequency proxy, not gospel.
- **Some sources cited (Migaku blog, jobsinjapan.com, talkpal.ai, JLPT Samurai, JLPTPrep) are commercial content marketing.** Their pedagogical claims align with academic consensus and other community resources, but treat individual numerical claims with appropriate scepticism.
- **Cure Dolly's "Organic Japanese" is controversial.** The Tatsumoto critique (tatsumoto-ren.github.io) argues her framework is itself another foreign abstraction. The repo uses Cure Dolly's framing selectively (uchi/soto, が as the unifying particle) where it clarifies, but defaults to mainstream descriptions otherwise.
- **The 12-month outcome is realistic but not guaranteed.** The US State Department's Foreign Service Institute classifies Japanese as a Category IV "super-hard language" and budgets 88 weeks / 2,200 class hours for English-speaking diplomats to reach General Professional Proficiency (ILR S-3/R-3) under full-time immersive conditions. The 12-month part-time roadmap aims at *conversational* proficiency (closer to ILR S-2), which is meaningfully lower than FSI's S-3 target — touching JLPT N2-level structures will require another 12–24 months beyond this plan.