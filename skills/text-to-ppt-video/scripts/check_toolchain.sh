#!/usr/bin/env bash
set -u

check() {
  if command -v "$1" >/dev/null 2>&1; then
    printf 'ok: %s -> %s\n' "$1" "$(command -v "$1")"
  else
    printf 'missing: %s\n' "$1"
  fi
}

check node
check npx
check ffmpeg
check ffprobe
check whisper

if command -v npx >/dev/null 2>&1; then
  if npx --yes remotion --version >/dev/null 2>&1; then
    printf 'ok: remotion via npx\n'
  else
    printf 'missing: remotion via npx\n'
  fi
fi

python="${PYTHON:-python3}"
"$python" - <<'PY'
import importlib.util

for name in ["moviepy", "imageio_ffmpeg", "whisper", "gtts", "PIL"]:
    if importlib.util.find_spec(name):
        print(f"ok: python package {name}")
    else:
        print(f"missing: python package {name}")

try:
    import imageio_ffmpeg
    print(f"ok: imageio ffmpeg -> {imageio_ffmpeg.get_ffmpeg_exe()}")
except Exception as error:
    print(f"missing: imageio ffmpeg ({error})")
PY
