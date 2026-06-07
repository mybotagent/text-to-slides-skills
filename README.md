# Text-to-Slides Skills

Local Codex skills for turning Korean or English presentation text into slide decks, responsive HTML slides, GIF previews, and timed MP4 slide videos.

## Skills

- `skills/text-to-ppt`: create editable PowerPoint decks from text.
- `skills/text-to-slides`: create responsive HTML slide or card-news output.
- `skills/text-to-gif`: create compact animated GIFs from metric-focused text.
- `skills/text-to-slides-video`: create motion-slide preview videos from slide scripts.
- `skills/text-to-ppt-video`: create timed MP4/WebM slide videos from page-script JSON.

## Text to PPT Video

The main video pipeline is in `skills/text-to-ppt-video`. It keeps timing data in JSON so every slide page maps 1:1 to narration.

Default local route:

1. Build `scenes.json` with one object per slide/page.
2. Build or reuse `timing.json` with `page`, `startMs`, `endMs`, `durationMs`, and `script`.
3. Generate timed narration with `create_timed_narration.py`.
4. Render PNG frames from the timing JSON with `render_video_frames.py`.
5. Encode frames to MP4 with `png_frames_to_mp4.py`.
6. Mux narration into the MP4 with `mux_audio_to_mp4.py`.
7. Run Whisper and keep the transcript JSON as verification evidence.

The Python path uses `moviepy`, `imageio-ffmpeg`, `openai-whisper`, and `gTTS`. System `ffmpeg`, Remotion, or HyperFrames can be used when available, but the Python route works without a global ffmpeg install.

## Sample Output

Final sample video:

```text
outputs/manual-llm-wiki-roi-ppt-video/text-to-ppt-video/llm-wiki-roi-video-with-audio.mp4
```

Timing and Whisper verification:

```text
outputs/manual-llm-wiki-roi-ppt-video/text-to-ppt-video/llm-wiki-roi-whisper-timing.json
outputs/manual-llm-wiki-roi-ppt-video/text-to-ppt-video/whisper/llm-wiki-roi-narration.json
```

Verified sample properties:

- duration: `35.35s`
- size: `1280x720`
- fps: `10`
- audio track: present

## Quick Check

```bash
PYTHONPATH=.codex/python-packages \
PYTHON=/Users/sanghee/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
skills/text-to-ppt-video/scripts/check_toolchain.sh
```

Compile scripts:

```bash
PYTHONPATH=.codex/python-packages \
/Users/sanghee/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
-m py_compile skills/text-to-ppt-video/scripts/*.py
```

## Notes

- `.codex/` is ignored because it contains local Python packages and model/tool caches.
- Intermediate frame, narration, and Whisper cache folders are ignored.
- Final sample media and compact JSON evidence are kept under `outputs/`.
