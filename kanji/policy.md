---
module: meta
file: kanji-policy
lang_focus: meta
kanji_level: 0
last_updated: 2026-05-23
---

# Kanji Policy

## Recognition Only — No Handwriting, No Production

Recognition only. No handwriting practice, no RTK keyword-to-kanji production drilling. Kanji writing is a separate optional skill and is not a prerequisite for spoken fluency. The time cost of kanji writing practice would be better invested in listening and vocab for the conversational goal of this curriculum.

## No Isolated Kanji Study

Kanji are introduced only when the learner already knows a vocab word that uses them. This avoids the WaniKani problem of "learning readings out of context that don't stick" (documented across the donkuri immersion guide and the LearnKanji guide).

Every kanji entry in `kanji-master.json` must have at least one `vocab_using` reference to a word already known from audio/kana context before the kanji is introduced.

## Targets

- ~400 kanji by end of Module 08
- ~800 kanji by end of Module 12

For comparison: Genki I + Genki II cover approximately 317 kanji per japanesecomplete.com's analysis.

## Re-Evaluation Point

Re-evaluate the kanji strategy at the end of Module 08. If recognition is proceeding faster than expected, consider whether to expand to ~1000 kanji by end of Module 12 or to keep the pace conservative and invest time elsewhere.
