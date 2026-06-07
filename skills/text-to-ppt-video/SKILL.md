---
name: text-to-ppt-video
description: "Turn text, markdown, presentation scripts, Korean drafts, slide outlines, or narration into synchronized motion-slide video files using ffmpeg + Whisper + Remotion or HyperFrames/HeyGen-style HTML rendering. Use when Codex must create MP4/WebM video from text with page-to-script timing JSON, captions, narrated slide timing, chart motion, or token-efficient local media processing."
---

# Text to PPT Video

## Overview

Create a synchronized video-style file from text. Despite the historical name, this skill outputs a video asset first, with `ffmpeg + Whisper` as the timing layer and Remotion or HyperFrames/HeyGen-style HTML as the motion renderer.

Use `text-to-ppt` for editable PPTX. Use this skill when the user asks for a video file, motion preview, MP4, WebM, GIF, animated slides, or text-to-video.

## Required Toolchain

1. `ffmpeg` capability: use system `ffmpeg` when available, otherwise Python `imageio-ffmpeg`.
2. `Whisper`: use CLI `whisper` when available, otherwise Python `openai-whisper`.
3. `moviepy` / Remotion / HyperFrames: encode or render motion slides from scene JSON and timing JSON.

If any required tool is missing, run `scripts/check_toolchain.sh`, report the missing item, and stop before pretending the final MP4/WebM exists. GIF is only a quick proof artifact, not the final output for this skill.

## Workflow

1. Convert source text into compact `scenes.json`; preserve one object per slide/page.
2. Put each page's full narration in `script`; keep slide text short.
3. Generate or ingest narration audio.
4. Normalize narration with ffmpeg.
5. Transcribe normalized audio with Whisper.
6. Build `timing.json` from Whisper segments and `scenes.json` using `scripts/build_video_timing.py`.
7. Render motion slides with the available renderer using the timing JSON:
   - one page equals one scene/sequence
   - `startMs`, `endMs`, and `durationMs` come from timing JSON
   - captions come from Whisper segments when requested
8. Encode final MP4/WebM with `moviepy + imageio-ffmpeg` or renderer-native ffmpeg and verify metadata.
9. Use chart motion by default when the script has metrics or ROI claims:
   - metric count-up
   - slow bar fill
   - no separate white sweep overlay on gauges
   - panel/text entrance
   - final hold for readability

For exact commands and branch choices, read `references/pipeline.md`.

## Relationship To Other Skills

- `text-to-ppt`: editable PPTX and Google Slides upload.
- `text-to-slides`: responsive HTML slides and Remotion-ready web scenes.
- `text-to-slides-video`: video scene planning and motion-slide previews.
- `text-to-gif`: compact GIFs for metric highlights.

Use one shared story spine when the user asks for multiple formats.

## Scene Schema

Preferred schema is page-to-script 1:1:

```json
{
  "page": 1,
  "title": "Slide title",
  "metric": "95%",
  "body": "On-slide summary",
  "script": "Full narration for this page"
}
```

Timing JSON shape:

```json
{
  "page": 1,
  "startMs": 0,
  "endMs": 6200,
  "durationMs": 6200,
  "title": "Slide title",
  "script": "Full narration for this page"
}
```

## Token Optimization Rules

- Do not paste full Whisper transcripts into the chat unless the user asks.
- Save transcripts, scene plans, captions, timing JSON, and render props as files.
- Use local scripts to transform large JSON artifacts.
- Load only the relevant reference file for the selected renderer:
  - Remotion: read Remotion best-practices and `references/pipeline.md`.
  - HyperFrames/HeyGen-style HTML: read HyperFrames skills and `references/pipeline.md`.
- Summarize verification outputs instead of pasting full ffprobe or transcript JSON.

## Verification Checklist

- output file exists and is non-empty
- ffprobe reports non-zero duration
- dimensions match requested format
- each source slide/page has a corresponding scene unless the user asks for a compressed teaser
- each timing row has `page`, `startMs`, `endMs`, `durationMs`, and `script`
- scene transitions follow Whisper-derived timing
- chart motion is visible and slow enough to read
- gauges use one filling bar only, no separate moving white overlay
- representative frame is visually readable
