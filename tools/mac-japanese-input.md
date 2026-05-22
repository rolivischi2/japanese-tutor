---
module: meta
file: mac-japanese-input
lang_focus: tooling
kanji_level: 0
last_updated: 2026-05-22
---

# macOS Japanese Input Setup

Enable Japanese (Romaji) input via System Settings → Keyboard → Input Sources, bind a keyboard shortcut to toggle the input source, and set the recommended display fonts (Hiragino Sans and Yu Mincho).

TODO: Step-by-step:
1. System Settings → Keyboard → Input Sources → click "+" → search "Japanese" → add "Japanese - Romaji"
2. Enable "Show Input menu in menu bar" for easy switching

TODO: Keyboard shortcut to toggle input source:
- System Settings → Keyboard → Keyboard Shortcuts → Input Sources
- Recommended binding: Ctrl+Space or Cmd+Space (check for conflicts with Spotlight)

TODO: Romaji-to-kana input rules:
- Type romaji; press Space to convert to kanji candidates; press Enter to confirm
- Double consonant for sokuon: tt → って, kk → っか
- Long vowels: type the vowel twice (ou, uu, etc.) — or use ー for katakana
- ん: type "nn" before a vowel, or "n" before a consonant

TODO: Recommended fonts for Japanese text rendering:
- Body text: Hiragino Sans (system default, excellent legibility)
- Reading/formal text: Yu Mincho (serif; install via Font Book if not present)

TODO: VS Code / editor setup for Japanese — install a Japanese font fallback in editor settings.

TODO: Optional: AquaSKK or ATOK for power users who want kana-based input (not needed for this curriculum).
