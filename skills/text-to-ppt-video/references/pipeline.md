# Text to PPT Video Pipeline

Use this pipeline when the final deliverable is MP4/WebM. The required stack is:

- ffmpeg capability through system `ffmpeg` or Python `imageio-ffmpeg`
- Whisper through CLI `whisper` or Python `openai-whisper`
- Python `moviepy` for the default MP4 encode path
- Remotion or HyperFrames/HeyGen-style HTML rendering when that renderer is available

GIF output is only a quick visual proof. Do not treat GIF as the final result for this skill.

## Token-Efficient File Contract

Keep large artifacts on disk and pass file paths between tools:

- `scenes.json`: compact page-to-script scene plan
- `audio.wav`: ffmpeg-normalized narration
- `whisper.json`: Whisper segments
- `timing.json`: one row per page with `startMs`, `endMs`, `durationMs`, `script`
- `render-props.json`: renderer input combining scenes and timing
- `final.mp4` or `final.webm`: encoded video

Codex should inspect summaries, row counts, durations, and representative snippets, not paste entire transcripts.

## 1. Tool Check

```bash
scripts/check_toolchain.sh
```

Require Python packages `moviepy`, `imageio-ffmpeg`, `openai-whisper`, `gTTS` when using the default local path. System `ffmpeg`, `ffprobe`, `whisper`, Remotion, or HyperFrames are preferred when available but not required for the Python fallback.

## 2. Scene Plan

Create one scene per slide/page:

```json
{
  "title": "Deck title",
  "scenes": [
    {
      "page": 1,
      "title": "Slide title",
      "metric": "95%",
      "body": "Short on-slide message",
      "bar": 95,
      "script": "Full narration for page 1."
    }
  ]
}
```

Do not put long narration in visible slide text. Keep it in `script`.

## 3. Audio Normalize With ffmpeg

For supplied narration:

```bash
python scripts/create_timed_narration.py out/timing.json --output out/audio.wav --work-dir out/narration-work --engine gtts
```

For supplied narration, normalize with system ffmpeg or `imageio-ffmpeg`.

Inspect duration:

```bash
python -c 'from moviepy import AudioFileClip; c=AudioFileClip("out/audio.wav"); print(c.duration); c.close()'
```

## 4. Whisper Timing

```bash
python -m whisper out/audio.wav --model tiny --language ko --output_format json --output_dir out
```

Use a smaller model only when speed is more important than timing quality.

## 5. Build Page Timing JSON

If source narration already exists, run Whisper first and then build timing:

```bash
python scripts/build_video_timing.py scenes.json out/audio.json --output out/timing.json --hold-ms 350 --min-scene-ms 1200
```

If a timing JSON already exists, use it as the source of truth and do not regenerate it unless the audio changed.

The script maps Whisper segment timing to the 1:1 page/script scene plan. It outputs:

```json
{
  "page": 1,
  "startMs": 0,
  "endMs": 6200,
  "durationMs": 6200,
  "title": "Slide title",
  "script": "Full narration for page 1.",
  "segmentStart": 0,
  "segmentEnd": 3
}
```

## 6A. Default Python Route

Use this route when Remotion/HyperFrames are not installed:

```bash
python scripts/render_video_frames.py scenes.json out/timing.json --output-dir out/frames --format wide --fps 10
python scripts/png_frames_to_mp4.py out/frames --output out/video.mp4 --fps 10
python scripts/mux_audio_to_mp4.py out/video.mp4 out/audio.wav --output out/final.mp4 --fps 10
```

This route uses `moviepy + imageio-ffmpeg` and keeps timing exactly aligned to `timing.json`.

## 6B. Remotion Route

Use Remotion when React components, precise frame math, chart interpolation, or MP4/WebM rendering are preferred.

Renderer mapping:

- one scene per `<Sequence>`
- `durationInFrames = Math.ceil(durationMs / 1000 * fps)`
- `from` frame comes from cumulative timing
- chart metric uses count-up interpolation
- gauge uses one `scaleX` bar fill only
- narration audio is one global audio track
- captions use Whisper segment timings

Recommended render command:

```bash
npx remotion render src/index.ts TextToPptVideo out/final.mp4 --props=out/render-props.json
```

## 6C. HyperFrames / HeyGen-Style HTML Route

Use HyperFrames/HeyGen-style HTML when the user wants HTML-authored scenes, GSAP timelines, captions, voiceover, or a HeyGen-compatible video workflow.

Renderer mapping:

- root composition duration equals final audio duration
- each page scene uses `data-start` and `data-duration` from `timing.json`
- GSAP timelines animate only visual properties
- audio is a separate track
- no infinite loops
- captions are timed from Whisper segments

Render through the available HyperFrames/HeyGen CLI, then encode or normalize with ffmpeg if needed.

## 7. Encode And Verify

Verify:

```bash
python -c 'from moviepy import VideoFileClip; c=VideoFileClip("out/final.mp4"); print(c.duration, c.fps, c.size, c.audio is not None); c.close()'
```

## Fallback

If the required toolchain is not installed, stop after producing `scenes.json` and explain which required tool is missing. Use `scripts/render_lightweight_video.py` only as a local preview, not as the skill's final video path.
