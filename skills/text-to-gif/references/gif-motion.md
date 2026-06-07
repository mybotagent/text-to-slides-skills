# GIF Motion Defaults

Use these defaults for metric or chart GIFs.

## Scene Structure

Each scene should carry one message:

```json
{
  "eyebrow": "Token Efficiency",
  "title": "Wiki calls are 20x lighter than raw document loading",
  "metric": "20x",
  "body": "60K raw tokens vs 3K curated Wiki tokens",
  "bar": 95,
  "duration": 900
}
```

## Motion Rules

- Animate metrics from 0 to the final number over the first 60-70% of the scene.
- Animate bars from 0 to `bar` percentage over the first 70% of the scene.
- Fade the title and body in before or alongside the metric.
- Hold the completed frame long enough to read.
- Avoid too many moving objects; one metric and one bar per scene is enough.
- Use 10-14 fps unless the user asks for smoother animation.
- Keep the GIF under a practical size by limiting frames and dimensions.

## Pillow Implementation Notes

- Render each frame as RGB or P mode and save with `save_all=True`.
- Use a simple cubic ease-out for count-up and bar fill.
- Use system fonts when possible; fall back to Pillow default if unavailable.
- For Korean text, prefer macOS fonts such as `/System/Library/Fonts/AppleSDGothicNeo.ttc` or `/System/Library/Fonts/Supplemental/Arial Unicode.ttf` when readable.

## Remotion Mapping

If converting to Remotion later:

- each scene becomes a `<Sequence>`
- metric count-up maps to `interpolate(frame, [start, end], [0, target])`
- bar fill maps to `scaleX(progress * value / 100)`
- scene duration maps from milliseconds to frames
