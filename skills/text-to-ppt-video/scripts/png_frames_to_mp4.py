#!/usr/bin/env python3
"""Encode PNG frames to MP4 with MoviePy/imageio-ffmpeg."""

from __future__ import annotations

import argparse
from pathlib import Path

from moviepy import ImageSequenceClip


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frames_dir", type=Path)
    parser.add_argument("--output", "-o", type=Path, required=True)
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--bitrate", default="2500k")
    args = parser.parse_args()

    frames = sorted(args.frames_dir.glob("frame-*.png"))
    if not frames:
        raise SystemExit(f"No frames found in {args.frames_dir}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    clip = ImageSequenceClip([str(path) for path in frames], fps=max(1, args.fps))
    clip.write_videofile(
        str(args.output),
        codec="libx264",
        audio=False,
        fps=max(1, args.fps),
        bitrate=args.bitrate,
        preset="medium",
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
        logger=None,
    )
    clip.close()
    print(f"Wrote {args.output} from {len(frames)} frames at {args.fps}fps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
