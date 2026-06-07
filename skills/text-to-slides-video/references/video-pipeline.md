# Text to Slides Video Pipeline

## Routes

### gif-preview

Use this route for deterministic testing without ffmpeg:

```bash
python scripts/render_motion_preview.py scenes.json --output preview.gif --format wide --fps 10
```

This route produces an animated GIF with metric count-up, bar fill, and scene transitions. It is a proof of motion and story timing, not a final high-fidelity video master.

### html-motion

Use `text-to-slides` rules to build responsive HTML:

- one `.slide` per scene
- `data-duration` per scene
- `data-count-to`, `data-prefix`, `data-suffix` for counters
- `--value` for bars
- responsive CSS plus Remotion metadata

### remotion-video

Use when Remotion and ffmpeg are available:

1. Convert each scene to a React component.
2. Use `<Sequence>` per scene.
3. Map `duration` milliseconds to frames.
4. Map counters to `interpolate(frame, ...)`.
5. Map bars to `scaleX(...)`.
6. Render MP4/WebM through Remotion.

## Shared Scene Schema

```json
{
  "title": "Deck/video title",
  "source": "user-provided script",
  "scenes": [
    {
      "eyebrow": "Short section label",
      "title": "One message",
      "metric": "95%",
      "body": "Readable support sentence",
      "bar": 95,
      "duration": 2400
    }
  ]
}
```

## Motion Timing

- 0-25%: eyebrow and title enter
- 20-85%: metric count-up and bar fill
- 85-100%: final hold
- add 500-700ms hold between scenes when exporting GIF
- Do not add a separate white sweep rectangle over the gauge; it reads as a second moving chart. Animate only the main filled bar unless the user explicitly asks for a shine effect.

## Fallback Policy

- If ffmpeg is unavailable: produce GIF preview.
- If Remotion is unavailable: produce responsive HTML or GIF preview.
- If browser rendering is blocked: validate scene JSON and generated file metadata.
