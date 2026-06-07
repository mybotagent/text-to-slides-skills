---
name: text-to-slides-video
description: Turn text, scripts, outlines, Korean drafts, metric narratives, or slide plans into motion-slide video assets. Use when Codex needs to summarize text into a video-ready slide spine, create responsive HTML/Remotion-style scenes, add default chart motion, produce a GIF motion preview when ffmpeg/Remotion are unavailable, or prepare a path from text-to-slides HTML into MP4/WebM/GIF.
---

# Text to Slides Video

## Overview

Create video-ready motion slides from text. Inherit the content and layout discipline of `text-to-slides`: responsive HTML structure, shared story spine, Remotion metadata, and default chart motion for metrics.

## Workflow

1. Summarize the input into a concise story spine.
2. Create 3-7 video scenes from the spine.
3. Choose output route:
   - `html-motion`: responsive HTML scene deck, best for Remotion handoff.
   - `gif-preview`: deterministic animated GIF proof using Python/Pillow.
   - `remotion-video`: high-fidelity MP4/WebM when Remotion and ffmpeg are available.
4. Apply default chart motion to metrics, bars, KPI tables, and comparisons.
5. Verify the output by checking dimensions, frame count or duration, readability, and final metric values.

## Required Text-to-Slides Carryover

When building a video scene deck, reuse the same rules from `../text-to-slides`:

- Use one shared story spine for PPT, HTML, GIF, and video variants.
- Preserve Remotion metadata such as `data-duration`, `data-remotion-width`, `data-remotion-height`, and `data-fps`.
- Use responsive web layout for HTML previews; do not hardcode fixed `1920px` browser layouts.
- Add chart motion by default when numbers or charts exist.
- Keep final values readable without animation.

Read these references as needed:

- `../text-to-slides/references/responsive-html.md`
- `../text-to-slides/references/chart-motion.md`
- `references/video-pipeline.md`

## Default Motion

Use the same visual grammar for all routes:

- metric count-up
- slow bar fill without a separate sweep overlay
- panel fade/slide entrance
- row or claim stagger
- final hold on each scene
- `prefers-reduced-motion` for HTML previews

## Tool Choice

Default to `gif-preview` for testing because this project may not have ffmpeg or Remotion installed. Use Remotion/ffmpeg only when available or explicitly requested.

If ffmpeg is missing, do not block. Produce the GIF preview, state that MP4 export requires ffmpeg or a Remotion render environment, and leave the scene JSON/HTML ready for later conversion.

## Quick Start

```bash
python scripts/render_motion_preview.py scenes.json --output preview.gif --format wide --fps 10
```

Scene JSON:

```json
{
  "title": "LLM Wiki ROI",
  "scenes": [
    {
      "eyebrow": "Opening Metric",
      "title": "LLM Wiki lowers knowledge-management cost",
      "metric": "95%",
      "body": "Token usage reduction versus raw document loading",
      "bar": 95,
      "duration": 2400
    }
  ]
}
```

## Verification Checklist

- scene JSON is valid
- output GIF/video exists and is non-empty
- preview has multiple frames or video has non-zero duration
- dimensions match selected format
- key text and final metric values are readable
- chart motion appears by default for numeric scenes
- if browser/ffmpeg/Remotion verification is blocked, report the limitation
