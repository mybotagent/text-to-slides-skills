---
name: text-to-ppt
description: Create editable PowerPoint decks from plain text, markdown, outlines, notes, pasted articles, Korean drafts, or speaker scripts. Use when Codex needs to turn text-only input into a structured PPTX with slide titles, bullets, speaker notes, source lines, consulting-style charts or card-like slides, and a professional 16:9 layout. Pair with text-to-slides when the user also needs responsive HTML, Remotion animation, video, or web slide output.
---

# Text to PPT

## Overview

Convert user-provided text into an editable PowerPoint deck. Use a disciplined sequence: clarify only what is necessary, turn the source into a slide plan, generate a PPTX, then verify the file and layout.

If the user asks for multiple formats, create one shared story spine first, then export the PPTX with this skill, responsive HTML with `text-to-slides`, motion-slide video previews with `text-to-slides-video`, and short animated metric GIFs with `text-to-gif`.

## Workflow

### 1. Ask Only Required Questions

For a simple request like "이 텍스트로 PPT 만들어줘", proceed with defaults instead of stopping:

- audience: general business
- slide count: 6-10 slides for ordinary text, 10-15 for long articles or lectures
- format: 16:9 widescreen PPTX
- style: clean consulting-style deck
- language: preserve the input language

Ask before writing only when the answer materially changes the deck:

- exact slide count
- audience or purpose
- required template or brand
- whether to include source/footer
- whether the user wants a chart-heavy deck, card-news deck, or lecture deck

### 2. Plan Before Building

Create a short text plan first for non-trivial decks:

```text
=== PPT 기획안 ===
장수: 8
스타일: consulting
출처 표기: Source: user-provided text

1. [Cover] Title
2. [Key message] Main takeaway
3. [Evidence] Supporting points
...
=== 기획안 끝 ===
```

If the user has asked for immediate execution or the request is routine, create the plan internally and proceed.

When pairing with `text-to-slides`, keep this plan as the source of truth for both outputs. Do not independently rewrite the slide order for PPTX and HTML unless the format requires a deliberate adaptation.

### 3. Normalize to Deck JSON

Use `scripts/text_to_ppt_plan.py` to convert text or markdown into deck JSON:

```bash
python scripts/text_to_ppt_plan.py input.md --output deck.json --title "Deck Title"
```

Then edit the JSON if needed. Prefer action titles that state the insight, not generic topic labels.

### 4. Build the PPTX

Use the Node script with `pptxgenjs`:

```bash
NODE_PATH=/path/to/node_modules node scripts/build_pptx.cjs deck.json --output deck.pptx
```

The script creates editable slides with:

- title slide
- section labels
- insight titles
- bullet layouts
- speaker notes
- source/footer text
- light or dark theme

### 5. Verify Quality

Always verify:

- PPTX file exists and is non-empty
- slide count matches the plan
- no slide has more than 5 bullets unless intentionally dense
- long paragraphs are moved to notes
- titles and body text are readable
- source/footer appears when specified

If a rendering tool is available, render the PPTX and inspect for overflow, unreadable text, or excessive empty space. Revise and regenerate if any slide fails.

## Style Rules

Default to a consulting/report style unless the user asks otherwise:

- Use grayscale with one accent color, default red `#c0392b`.
- No emoji, decorative icons, gradients, shadows, or ornamental rounded cards.
- Make slide titles pass the "So what?" test.
- Quantify claims when numbers exist in the source.
- Keep every slide focused on one message.
- Include `Source:` at the bottom when source information is known.
- Avoid empty lower-half slides; add explanatory text, a comparison, or split the structure.

For stricter guidance, read `references/consulting-style.md`.

## Resources

- `scripts/text_to_ppt_plan.py`: Convert plain text or markdown into deck JSON.
- `scripts/build_pptx.cjs`: Build an editable PPTX from deck JSON with `pptxgenjs`.
- `scripts/check_text_to_ppt_toolchain.sh`: Check Node and PPTX generation dependencies.
- `references/deck-json.md`: Deck JSON schema and examples.
- `references/consulting-style.md`: Consulting-style writing, layout, and validation rules.
- Pair with `../text-to-slides` when the requested deliverable includes responsive HTML, card news, Remotion, animation, video, or web preview.
- Pair with `../text-to-slides-video` when the requested deliverable includes a video-ready slide sequence, Remotion handoff, or motion preview.
- Pair with `../text-to-gif` when the requested deliverable includes a short looping GIF, metric animation, or chart motion preview.
