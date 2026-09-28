#!/usr/bin/env python3
"""Mix a voiceover over the music and fx stems, then master to a loudness target.

Stdlib Python plus ffmpeg. The music ducks under each spoken line with eased
ramps and swells back in the gaps; the fx duck only a little so UI sounds stay
crisp. The voice gets a high-pass, a touch of presence, gentle compression,
level matching, and a little room so it sits in the music's space. Music
automation (keyframes in dB) and the end fade never touch the voice mid-word.

Without --script it simply masters the stems (music-only cut).

Usage:
  python mix.py --music audio/stem-music.wav --fx audio/stem-fx.wav \
      --script vo-script.json --track wa --vo-dir vo --out final-wa.wav
Automation and duck depths come from the script's "mix" block (see
../assets/examples/vo-script.json); flags override them.
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from array import array
from pathlib import Path

SR = 44100


def ffmpeg() -> str:
    import os
    found = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    if not found:
        sys.exit("ffmpeg not found; install it or set FFMPEG=/path/to/ffmpeg")
    return found


def read_f32(path: Path, channels: int, filters: str | None = None) -> array:
    cmd = [ffmpeg(), "-v", "error", "-i", str(path)]
    if filters:
        cmd += ["-af", filters]
    cmd += ["-ac", str(channels), "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, check=True, capture_output=True).stdout
    a = array("f")
    a.frombytes(raw)
    return array("d", a)


def db(x: float) -> float:
    return 10 ** (x / 20)


def lines_for(script: dict, track: str) -> list[dict]:
    tracks = script["tracks"]
    by_id = {l["id"]: l for t in tracks.values() for l in t if "id" in l}
    return [by_id[l["ref"]] if "ref" in l else l for l in tracks[track]]


def room(x: array) -> array:
    """Short Schroeder room for the voice bus."""
    n = len(x)
    out = array("d", bytes(8 * n))
    for d in (1116, 1188, 1277, 1356):
        buf = [0.0] * d
        idx, f = 0, 0.0
        for i in range(n):
            y = buf[idx]
            f = y * 0.6 + f * 0.4
            buf[idx] = x[i] + f * 0.72
            idx = idx + 1 if idx + 1 < d else 0
            out[i] += y / 4
    for d in (556, 225):
        buf = [0.0] * d
        idx = 0
        for i in range(n):
            b = buf[idx]
            y = -out[i] + b
            buf[idx] = out[i] + b * 0.5
            idx = idx + 1 if idx + 1 < d else 0
            out[i] = y
    return out


def ramp_env(n: int, spans, depth_db: float, pre=0.12, post=0.35, att=0.14, rel=0.45) -> array:
    """Gain curve: 0 dB outside speech, depth_db under it, cosine ramps."""
    g = array("d", bytes(8 * n))  # 0..1 amount of duck
    for s, e in spans:
        a0, a1 = s - pre - att, s - pre
        r0, r1 = e + post, e + post + rel
        for i in range(max(0, int(a0 * SR)), min(n, int(r1 * SR) + 1)):
            t = i / SR
            up = min(1.0, max(0.0, (t - a0) / att))
            down = min(1.0, max(0.0, (r1 - t) / rel))
            v = min(up, down)
            if v > g[i]:
                g[i] = v
    for i in range(n):
        g[i] = db(depth_db * (0.5 - 0.5 * math.cos(math.pi * g[i])))
    return g


def interp(t: float, keys) -> float:
    if t <= keys[0][0]:
        return keys[0][1]
    for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
        if t <= t1:
            return v0 + (v1 - v0) * (t - t0) / max(1e-9, t1 - t0)
    return keys[-1][1]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--music", required=True)
    p.add_argument("--fx", required=True)
    p.add_argument("--script", help="voiceover script JSON (omit for a music-only master)")
    p.add_argument("--track", help="which track of the script to use")
    p.add_argument("--vo-dir", default="vo")
    p.add_argument("--out", required=True, help="mastered WAV (48 kHz, 16-bit)")
    p.add_argument("--lufs", type=float, default=-14.0)
    p.add_argument("--tp", type=float, default=-2.0, help="true-peak ceiling; AAC encoding can overshoot it by up to ~1 dB")
    p.add_argument("--duck-db", type=float)
    p.add_argument("--fx-duck-db", type=float)
    p.add_argument("--voice-db", type=float)
    p.add_argument("--fade-out", type=float)
    args = p.parse_args()

    script = json.loads(Path(args.script).read_text()) if args.script else {}
    cfg = {"duck_db": -9.5, "fx_duck_db": -3.5, "voice_db": 1.5, "fx_db": -1.5, "fade_out": 1.4, "music_automation": []}
    cfg.update(script.get("mix", {}))
    for key in ("duck_db", "fx_duck_db", "voice_db", "fade_out"):
        if getattr(args, key) is not None:
            cfg[key] = getattr(args, key)

    music = read_f32(Path(args.music), 2)
    fx = read_f32(Path(args.fx), 2)
    n = min(len(music), len(fx)) // 2
    dur = n / SR

    # ---- voice bus
    vo = array("d", bytes(8 * n))
    spans = []
    if args.script:
        if not args.track:
            sys.exit("--track is required with --script")
        chain = "highpass=f=85,equalizer=f=4000:t=q:w=1.2:g=2,acompressor=threshold=-22dB:ratio=2.5:attack=4:release=90"
        for line in lines_for(script, args.track):
            w = read_f32(Path(args.vo_dir) / f"{line['id']}.wav", 1, chain)
            voiced = [v for v in w if abs(v) > 0.01] or [1e-9]
            rms = math.sqrt(sum(v * v for v in voiced) / len(voiced))
            k = db(-19) / max(rms, 1e-9)
            s = int(line["start"] * SR)
            for i, v in enumerate(w):
                if s + i < n:
                    vo[s + i] += v * k
            spans.append((line["start"], line["start"] + len(w) / SR))
            if len(w) / SR > line.get("max", 1e9) - line["start"] + 0.05:
                print(f"warning: {line['id']} runs {len(w)/SR:.2f}s, slot is {line['max'] - line['start']:.2f}s", file=sys.stderr)
        for (a0, a1), (b0, _) in zip(spans, spans[1:]):
            if a1 > b0:
                print(f"warning: lines overlap at {b0:.2f}s", file=sys.stderr)
    rv = room(vo) if spans else vo

    # ---- automation
    duck_m = ramp_env(n, spans, cfg["duck_db"]) if spans else None
    duck_fx = ramp_env(n, spans, cfg["fx_duck_db"], pre=0.05, post=0.1, att=0.05, rel=0.2) if spans else None
    keys = cfg["music_automation"]
    fade = cfg["fade_out"]
    gv, gfx = db(cfg["voice_db"]), db(cfg["fx_db"])
    room_g = db(-21)
    out = array("f", [0.0]) * (2 * n)
    for i in range(n):
        t = i / SR
        auto = db(interp(t, keys)) if keys else 1.0
        f = min(1.0, t / 0.03) * min(1.0, (dur - t) / fade) if fade > 0 else 1.0
        dm = duck_m[i] if duck_m else 1.0
        df = duck_fx[i] if duck_fx else 1.0
        tail = min(1.0, (dur - t) / 0.06)
        v = vo[i] * gv * tail
        r = rv[i] * room_g * gv * tail if spans else 0.0
        for c in range(2):
            m = music[2 * i + c] * dm * auto + fx[2 * i + c] * df * gfx
            x = m * f + v + r * (0.9 if c == 0 else 0.85)
            out[2 * i + c] = math.tanh(x * 1.2) / 1.2

    # ---- master: two-pass loudnorm
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "mix.f32"
        raw.write_bytes(out.tobytes())
        src = ["-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw)]
        base = f"aformat=channel_layouts=stereo,loudnorm=I={args.lufs}:TP={args.tp}:LRA=11"
        probe = subprocess.run([ffmpeg(), "-hide_banner", *src, "-af", base + ":print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
        m = json.loads(probe[probe.rindex("{"): probe.rindex("}") + 1])
        measured = f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}"
        subprocess.run([ffmpeg(), "-y", "-v", "error", *src, "-af", f"{base}:{measured}:linear=true,aresample=48000", "-ac", "2", "-c:a", "pcm_s16le", args.out], check=True)
    print(f"{args.out}  lines={len(spans)}  spans={[(round(a, 2), round(b, 2)) for a, b in spans]}")


if __name__ == "__main__":
    main()
