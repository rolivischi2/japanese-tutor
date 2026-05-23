---
module: meta
file: 06-ai-conversation-prompts
lang_focus: meta
kanji_level: 0
last_updated: 2026-05-23
---

# AI Conversation Prompts

## Overview

TODO: Explain when and how to use AI as a conversation partner. Three modes: (1) open-ended conversation partner, (2) tutor prep, (3) structured correction. Available from Module 03 onward (before that, grammar base is too thin).

## Template 1: Conversation Partner

TODO: Write out the conversation-partner system prompt template:
- "Act as a Japanese friend with kind patience. Use plain form. Speak at the level of someone who has finished Module N of my curriculum (file attached). If I make a grammar mistake, repeat my sentence back in correct Japanese using ね, then continue naturally. Do not give English unless I ask."
- Add guidance on which module number to specify at each stage.

## Template 2: Tutor Prep

TODO: Write out the tutor-prep prompt template:
- "Given the topic [X], produce 10 example questions a tutor might ask me in plain Japanese, and 5 prompt answers using only grammar from Modules 00–[current]."
- Suggest running this in the 10 minutes before each tutor lesson, using the current module's `dialogues.md` as context.

## Template 3: Structured Correction

TODO: Write out the structured-correction prompt template:
- Paste a Japanese paragraph produced in self-talk.
- "Produce a corrected version of the following paragraph + a 5-bullet mistake summary, using only grammar from Modules 00–[current]. Preserve my intended meaning as much as possible."
- Note: paste the corrected version into `grammar-reference/common-mistakes.md` and add SRS cards for flagged errors.

## Cross-References

TODO: Link to `output-practice/ai-conversation-prompts.md` for the full list of prompts with module tags, and `pedagogy/02-input-vs-output-balance.md` for the weekly minute allocation.
