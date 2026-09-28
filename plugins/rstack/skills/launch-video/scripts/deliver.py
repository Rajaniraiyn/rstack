#!/usr/bin/env python3
"""Mux the rendered video with the mastered audio, bake the poster in as frame 0, verify.

Frame 0 is replaced (not prepended), so duration and sync are unchanged and
every platform's auto-thumbnail shows the poster. Prints duration, size,
loudness, and true peak so the report can state them.

Usage:
  python deliver.py --video work/video.mp4 --audio work/final.wav --poster work/stills/t001.20.jpg --out launch-video/landscape/video.mp4
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


def ffmpeg() -> str:
    found = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    if not found:
        sys.exit("ffmpeg not found; install it or set FFMPEG=/path/to/ffmpeg")
    return found


def duration(path: str) -> float:
    err = subprocess.run([ffmpeg(), "-hide_banner", "-i", path], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--video", required=True)
    p.add_argument("--audio", required=True)
    p.add_argument("--poster", help="settled still to use as frame 0 (also saved as poster.jpg next to the output)")
    p.add_argument("--out", required=True)
    p.add_argument("--crf", type=int, default=20, help="raise to shrink the file (grainy footage eats bitrate)")
    args = p.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [ffmpeg(), "-y", "-v", "error", "-i", args.video]
    if args.poster:
        cmd += ["-i", args.poster, "-i", args.audio, "-filter_complex", "[1:v][0:v]scale2ref[p][v];[v][p]overlay=enable='eq(n,0)'[o]", "-map", "[o]", "-map", "2:a"]
        shutil.copy(args.poster, out.parent / "poster.jpg")
    else:
        cmd += ["-i", args.audio, "-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "libx264", "-crf", str(args.crf), "-preset", "slow", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-shortest", str(out)]
    subprocess.run(cmd, check=True)

    dv, da, do = duration(args.video), duration(args.audio), duration(str(out))
    if abs(dv - da) > 0.05:
        print(f"warning: video {dv:.2f}s and audio {da:.2f}s differ; output is {do:.2f}s", file=sys.stderr)
    stats = subprocess.run([ffmpeg(), "-hide_banner", "-i", str(out), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", stats)[-1]
    peak = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", stats)[-1]
    size = out.stat().st_size / 1e6
    print(f"{out}  {do:.2f}s  {size:.1f} MB  {lufs} LUFS  true peak {peak} dBFS")
    if float(peak) > -1.0:
        print("note: true peak above -1 dBFS after AAC; re-master with mix.py --tp -2.5.", file=sys.stderr)
    if size > 25:
        print("note: over 25 MB; some chat apps reject it. Re-run with a higher --crf.", file=sys.stderr)


if __name__ == "__main__":
    main()
