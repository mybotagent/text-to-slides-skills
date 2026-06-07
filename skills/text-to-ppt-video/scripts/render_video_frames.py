#!/usr/bin/env python3
"""Render PNG frames from scene JSON and timing JSON."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from render_lightweight_video import FORMATS, render_frame


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenes_json", type=Path)
    parser.add_argument("timing_json", type=Path)
    parser.add_argument("--output-dir", "-o", type=Path, required=True)
    parser.add_argument("--format", choices=FORMATS.keys(), default="wide")
    parser.add_argument("--fps", type=int, default=10)
    args = parser.parse_args()

    deck = json.loads(args.scenes_json.read_text(encoding="utf-8"))
    timing_doc = json.loads(args.timing_json.read_text(encoding="utf-8"))
    scenes = deck.get("scenes", [])
    timing = timing_doc.get("timing", [])
    if len(scenes) != len(timing):
        raise SystemExit(f"Scene/timing mismatch: {len(scenes)} scenes vs {len(timing)} timing rows")

    fps = max(4, min(30, args.fps))
    frame_ms = 1000 / fps
    size = FORMATS[args.format]
    args.output_dir.mkdir(parents=True, exist_ok=True)

    frame_index = 0
    for scene, row in zip(scenes, timing):
        duration = int(row["durationMs"])
        count = max(1, math.ceil(duration / frame_ms))
        for i in range(count):
            progress = i / max(1, count - 1)
            image = render_frame(scene, progress, size)
            image.save(args.output_dir / f"frame-{frame_index:05d}.png")
            frame_index += 1

    metadata = {"frames": frame_index, "fps": fps, "width": size[0], "height": size[1]}
    (args.output_dir / "frames.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {frame_index} frames to {args.output_dir} at {size[0]}x{size[1]} {fps}fps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
