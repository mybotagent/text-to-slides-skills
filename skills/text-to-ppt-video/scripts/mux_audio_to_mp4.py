#!/usr/bin/env python3
"""Mux a video-only MP4 and narration audio into a final MP4."""

from __future__ import annotations

import argparse
from pathlib import Path

from moviepy import AudioFileClip, VideoFileClip


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("audio", type=Path)
    parser.add_argument("--output", "-o", type=Path, required=True)
    parser.add_argument("--fps", type=int, default=10)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    video = VideoFileClip(str(args.video))
    audio = AudioFileClip(str(args.audio))
    final = video.with_audio(audio).with_duration(min(video.duration, audio.duration))
    final.write_videofile(
        str(args.output),
        codec="libx264",
        audio_codec="aac",
        fps=max(1, args.fps),
        bitrate="2500k",
        audio_bitrate="128k",
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
        logger=None,
    )
    final.close()
    audio.close()
    video.close()
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
