---
module: meta
file: 04-long-vowels-and-sokuon
lang_focus: pronunciation
kanji_level: 0
last_updated: 2026-05-22
---

# Long Vowels and Sokuon (Geminate Consonants)

## Long Vowels

TODO: Explain phonemic vowel length in Japanese — doubling the duration of a vowel changes meaning. Roland has a strong advantage here (Hungarian distinguishes 7 short/long vowel pairs phonemically). Key risk: Hungarian long vowels also shift quality; Japanese long vowels are pure duration extension with no quality change.

## Minimal Pairs: Long Vowels

TODO: Write out these minimal pairs with meaning contrast and pronunciation note:
- おばさん (aunt) vs おばあさん (grandmother)
- ゆき (snow/courage name) vs ゆうき (courage)
- Note: these pairs are pre-loaded in `pronunciation/09-minimal-pairs.csv` with contrast_type = vowel_length.

## Sokuon — Geminate Consonants (っ)

TODO: Explain the sokuon: a "silent" mora that doubles the following consonant. The key is to hold the closure (stop consonants) or fricative for exactly one extra mora before releasing. Roland's advantage: Hungarian has geminate consonants (e.g. *vissza*, *meggy* vs *megy*); Swiss German also preserves consonant length.

## Minimal Pairs: Sokuon

TODO: Write out these minimal pairs with meaning contrast:
- きて (come, te-form of くる) vs きって (stamp)
- さか (slope) vs さっか (writer)
- Note: these pairs are pre-loaded in `pronunciation/09-minimal-pairs.csv` with contrast_type = sokuon.

## Common Mistake: Devoiced Short Vowels vs Long Vowels

TODO: Note the potential confusion: devoiced /u/ and /i/ (whispered) are NOT the same as deleted. The mora duration is preserved even when the vowel is devoiced. Contrast this with genuine vowel length. Example: すき has a full mora for す even though the /u/ is devoiced.

## Drilling Methodology

TODO: Recommend using `pronunciation/09-minimal-pairs.csv` rows with contrast_type = vowel_length and sokuon as the primary drill source. Clap one beat per mora while saying each word to internalise duration.
