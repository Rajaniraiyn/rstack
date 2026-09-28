#!/usr/bin/env python3
"""Synthesize a launch-video soundtrack from a JSON song spec (stdlib only).

Music and sound effects are written as one piece: effects are pitched to the
song's chords and share its reverb, and the music is sidechained to the kick.
Outputs float32 stereo WAV stems so a voiceover can duck the music but not
the effects:

  <out>/stem-music.wav   drums + bass + chords + arp + reverb
  <out>/stem-fx.wav      UI sounds, hits, risers
  <out>/soundtrack.wav   quick premix (no voiceover), peak-normalized

Usage:
  python synth.py song.json --out audio/
See ../assets/examples/song.json for every field. Runtime is roughly a
minute for a 20-second track on CPython.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import struct
from array import array
from pathlib import Path

SR = 44100
TAU = 2 * math.pi


def hz(m: float) -> float:
    return 440.0 * 2 ** ((m - 69) / 12)


def env(t: float, a: float, d: float) -> float:
    return t / a if t < a else math.exp(-(t - a) / d)


class Mix:
    def __init__(self, duration: float, seed: int = 11):
        self.n = int(SR * duration)
        z = lambda: [array("d", bytes(8 * self.n)), array("d", bytes(8 * self.n))]
        self.bus = {"drums": z(), "music": z(), "fx": z()}
        self.send = z()
        self.rng = random.Random(seed)

    def rnd(self) -> float:
        return self.rng.random() * 2 - 1

    def add(self, bus: str, t0: float, length: float, fn, gain: float, pan: float = 0.0, rev: float = 0.2):
        s0, n = int(t0 * SR), int(length * SR)
        gl, gr = gain * math.cos((pan + 1) * math.pi / 4), gain * math.sin((pan + 1) * math.pi / 4)
        L, R = self.bus[bus]
        SL, SR_ = self.send
        lo, hi = max(0, -s0), min(n, self.n - s0)
        for i in range(lo, hi):
            v = fn(i / SR)
            k = s0 + i
            L[k] += v * gl
            R[k] += v * gr
            if rev:
                SL[k] += v * gl * rev
                SR_[k] += v * gr * rev


# ---------------------------------------------------------------- voices


def sine_blip(m, d=0.05):
    f = hz(m)
    return lambda x: math.sin(TAU * f * x) * env(x, 0.002, d)


def pluck(m, bright=0.4):
    f = hz(m)
    return lambda x: (math.sin(TAU * f * x) + bright * math.sin(2 * TAU * f * x) * math.exp(-x * 14)) * env(x, 0.003, 0.14)


def kick(start=90.0, end=48.0, decay=0.13, click=0.15, mx=None):
    k = 35.0
    def fn(x):
        ph = TAU * (end * x + (start) * (1 - math.exp(-x * k)) / k)
        v = math.sin(ph) * env(x, 0.001, decay)
        if mx and x < 0.004:
            v += click * mx.rnd() * env(x, 0.0005, 0.004)
        return v
    return fn


def lp_noise(mx, cut):
    state = [0.0]
    def nxt():
        state[0] += cut * (mx.rnd() - state[0])
        return state[0]
    return nxt


def hp_noise(mx):
    prev = [0.0]
    def nxt():
        r = mx.rnd()
        v = r - prev[0]
        prev[0] = r
        return v
    return nxt


def whoosh(mx, t0, length, gain):
    st = [0.0]
    def fn(x):
        p = x / length
        c = 0.03 + 0.2 * math.sin(math.pi * p)
        st[0] += c * (mx.rnd() - st[0])
        return st[0] * math.sin(math.pi * p)
    mx.add("fx", t0, length, fn, gain, 0, 0.4)


# ---------------------------------------------------------------- song


def build(spec: dict) -> Mix:
    dur = spec["duration"]
    bpm = spec.get("bpm", 120)
    beat = 60.0 / bpm
    bar = beat * 4
    drop = spec.get("drop", 0.0)
    outro = spec.get("outro", dur)
    chords = spec.get("chords", [[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]])
    bars_per_chord = spec.get("bars_per_chord", 1)
    mx = Mix(dur, spec.get("seed", 11))

    def chord_at(t):
        idx = math.floor((t - drop) / (bar * bars_per_chord))
        return chords[idx % len(chords)]

    intro = spec.get("intro", {})
    # clock ticks on each beat before the drop
    if intro.get("ticks", True) and drop > 0:
        i = 0
        while i * beat < drop - 0.01:
            m = 76 if i % 2 else 81
            mx.add("fx", i * beat, 0.12, sine_blip(m, 0.018), 0.09, 0.3 if i % 2 else -0.3, 0.3)
            i += 1
    # word hits: sub boom + noise + root note, each a step louder
    hits = intro.get("hits", [])
    for j, t in enumerate(hits):
        g = 0.7 + 0.3 * (j / max(1, len(hits) - 1))
        mx.add("drums", t, 0.9, kick(60, 40, 0.28), 0.42 * g, 0, 0.1)
        nz = lp_noise(mx, 0.35)
        mx.add("fx", t, 0.3, lambda x, nz=nz: nz() * env(x, 0.001, 0.05), 0.12 * g, 0, 0.5)
        root = chords[0][0]
        mx.add("music", t, 1.0, lambda x, r=root: (math.sin(TAU * hz(r - 12) * x) + 0.3 * math.sin(TAU * hz(r) * x)) * env(x, 0.005, 0.35), 0.1 * g, 0, 0.3)
    # riser into the drop
    if intro.get("riser"):
        a, b = intro["riser"]
        length = b - a
        nz = lp_noise(mx, 0.02)
        st = [0.0]
        def rise_noise(x):
            p = x / length
            st[0] += (0.02 + 0.5 * p * p) * (nz() * 3 - st[0])
            return st[0] * p
        mx.add("fx", a, length, rise_noise, 1.1, 0, 0.5)
        ph = [0.0]
        base = chords[0][0]
        def rise_tone(x):
            p = x / length
            ph[0] += TAU * hz(base + 12 * p * p) / SR
            return (math.sin(ph[0]) + 0.3 * math.sin(2 * ph[0])) * p * 0.6
        mx.add("fx", a, length, rise_tone, 0.16, 0, 0.6)
    # quiet pad under the intro
    if drop > 0:
        for j, m in enumerate(chords[0]):
            f = hz(m)
            mx.add("music", 0, drop, lambda x, f=f: (math.sin(TAU * f * x) + 0.2 * math.sin(2 * TAU * f * x)) * min(1, x / 1.5) * min(1, (drop - x) / 0.05), 0.012, (j - 1) * 0.4, 0.6)

    # groove: drop -> outro
    kicks = []
    t = drop
    while t < outro - 0.01:
        kicks.append(t)
        mx.add("drums", t, 0.4, kick(90, 48, 0.13, 0.15, mx), 0.5, 0, 0.03)
        beat_in_bar = round((t - drop) / beat) % 4
        if beat_in_bar in (1, 3):
            nz = lp_noise(mx, 0.55)
            clap = lambda x, nz=nz: nz() * (env(x, 0.001, 0.012) + 0.6 * env(max(0, x - 0.012), 0.001, 0.012) + 0.5 * env(max(0, x - 0.024), 0.001, 0.07))
            mx.add("drums", t, 0.3, clap, 0.16, 0.1, 0.35)
        hn = hp_noise(mx)
        mx.add("drums", t + beat / 2, 0.06, lambda x, hn=hn: hn() * env(x, 0.0005, 0.018), 0.05, 0.35, 0.15)
        t += beat
    if drop > 0:
        hn = hp_noise(mx)
        mx.add("fx", drop, 1.6, lambda x: hn() * env(x, 0.001, 0.5), 0.06, 0, 0.5)  # crash
    # bass: eighths on the root, octave bounce
    t, k = drop, 0
    while t < outro - 0.01:
        f = hz(chord_at(t)[0] - 24 + (12 if k % 4 == 3 else 0))
        mx.add("music", t, 0.24, lambda x, f=f: (math.sin(TAU * f * x) + 0.35 * math.sin(2 * TAU * f * x) + 0.12 * math.sin(3 * TAU * f * x)) * env(x, 0.004, 0.12), 0.12, 0, 0.02)
        t += beat / 2
        k += 1
    # chords: detuned pad, one per chord span
    span = bar * bars_per_chord
    b = 0
    while drop + b * span < outro:
        t0 = drop + b * span
        ch = chords[b % len(chords)]
        for j, m in enumerate(list(ch) + [ch[0] + 12]):
            f = hz(m)
            L = span + 0.1
            def pad(x, f=f, L=L):
                a = min(1, x / 0.02) * min(1, (L - x) / 0.1)
                v = 0.0
                for d in (-0.0018, 0.0, 0.0017):
                    ph = TAU * f * (1 + d) * x
                    v += math.sin(ph) + 0.33 * math.sin(2 * ph) + 0.14 * math.sin(3 * ph)
                return v * a
            mx.add("music", t0, L, pad, 0.02, (1 if j % 2 else -1) * 0.45, 0.4)
        b += 1
    # arp
    pat = spec.get("arp", [0, 1, 2, 3, 2, 1, 2, 3])
    i = 0
    while drop + i * beat / 2 < outro - 0.01:
        t = drop + i * beat / 2
        ch = chord_at(t)
        tones = [ch[0], ch[1], ch[2], ch[0] + 12]
        mx.add("music", t, 0.6, pluck(tones[pat[i % len(pat)]] + 12), 0.045 if i % 4 == 0 else 0.03, ((i % 3) - 1) * 0.4, 0.35)
        i += 1

    # outro: hit, bloom, motif
    if outro < dur:
        mx.add("drums", outro, 1.5, kick(70, 38, 0.45), 0.45, 0, 0.2)
        hn = hp_noise(mx)
        mx.add("fx", outro, 2.5, lambda x: hn() * env(x, 0.001, 0.7), 0.05, 0, 0.6)
        bloom = spec.get("outro_chord", [53, 60, 64, 69, 72])
        for j, m in enumerate(bloom):
            f = hz(m)
            mx.add("music", outro + j * 0.04, dur - outro, lambda x, f=f: (math.sin(TAU * f * x) + 0.25 * math.sin(2 * TAU * f * x)) * min(1, x / 0.03) * math.exp(-x / 1.6), 0.05, (j - 2) * 0.3, 0.7)
        for tm, m in spec.get("outro_motif", []):
            mx.add("fx", tm, 1.2, sine_blip(m, 0.3), 0.035, 0.2, 0.7)

    # sound effects
    for ev in spec.get("sfx", []):
        sfx(mx, ev, chords)

    mx.kicks = kicks
    return mx


def sfx(mx: Mix, ev: dict, chords):
    kind, t = ev["type"], ev["t"]
    g = ev.get("gain", 1.0)
    root = chords[0][0]
    if kind == "whoosh":
        whoosh(mx, t, ev.get("len", 0.35), 0.18 * g)
    elif kind == "typing":
        n = int(ev.get("len", 1.4) / ev.get("rate", 0.065))
        for i in range(n):
            nz = lp_noise(mx, 0.5)
            mx.add("fx", t + i * ev.get("rate", 0.065) + mx.rnd() * 0.012, 0.03, lambda x, nz=nz: nz() * env(x, 0.0005, 0.005), 0.035 * g, 0.2, 0.1)
    elif kind == "send":
        whoosh(mx, t - 0.05, 0.3, 0.16 * g)
        mx.add("fx", t, 0.4, sine_blip(root + 24, 0.07), 0.05 * g, 0.2, 0.4)
        mx.add("fx", t + 0.05, 0.4, sine_blip(root + 31, 0.07), 0.035 * g, 0.2, 0.4)
    elif kind == "pop":
        m = ev.get("note", root + 24)
        mx.add("fx", t, 0.3, sine_blip(m, 0.05), 0.04 * g, -0.2, 0.35)
        mx.add("fx", t + 0.04, 0.3, sine_blip(m + 7, 0.05), 0.022 * g, -0.2, 0.35)
    elif kind == "click":
        hn = hp_noise(mx)
        mx.add("fx", t, 0.02, lambda x: hn() * math.exp(-x * 500), 0.03 * g, 0, 0.1)
        mx.add("fx", t, 0.4, sine_blip(ev.get("note", root + 20), 0.08), 0.05 * g, 0, 0.35)
    elif kind == "chime":  # success: rising chord tones
        for j, m in enumerate(ev.get("notes", [root + 24, root + 27, root + 31, root + 36])):
            mx.add("fx", t + j * 0.06, 0.8, sine_blip(m, 0.18), 0.035 * g, (j - 1.5) * 0.2, 0.5)
    elif kind == "chord":  # soft landing for a card or preview
        for j, m in enumerate(ev.get("notes", [root, root + 7, root + 12, root + 15])):
            mx.add("fx", t + j * 0.02, 1.2, sine_blip(m + 12, 0.3), 0.03 * g, (j - 1.5) * 0.3, 0.6)
    elif kind == "hit":
        mx.add("fx", t, 0.8, kick(70, 45, 0.2), 0.18 * g, 0, 0.1)
        nz = lp_noise(mx, 0.3)
        mx.add("fx", t, 0.25, lambda x: nz() * env(x, 0.001, 0.04), 0.1 * g, 0, 0.5)
    elif kind == "buzz":  # phone vibration + notification ding
        for dt in (0.0, 0.18):
            mx.add("fx", t + dt, 0.14, lambda x: (1 if math.sin(TAU * 165 * x) >= 0 else -1) * 0.5 * min(1, x / 0.01) * min(1, (0.14 - x) / 0.02), 0.05 * g, 0, 0.05)
        mx.add("fx", t + 0.02, 0.6, sine_blip(root + 31, 0.1), 0.06 * g, 0.1, 0.4)
        mx.add("fx", t + 0.14, 0.8, sine_blip(root + 36, 0.16), 0.05 * g, 0.1, 0.5)
    elif kind == "rewind":  # tape rewind with stutter
        length = ev.get("len", 1.2)
        ph, st = [0.0], [0.0]
        def rw(x):
            p = x / length
            ph[0] += TAU * hz(root + 36 - 30 * p) / SR
            st[0] += 0.08 * (mx.rnd() - st[0])
            stutter = 0.6 + 0.4 * (1 if math.sin(TAU * (8 + 10 * p) * x) >= 0 else -1)
            return (math.sin(ph[0]) * 0.5 + st[0] * 2) * stutter * math.sin(math.pi * p)
        mx.add("fx", t, length, rw, 0.09 * g, 0, 0.3)
    else:
        raise ValueError(f"unknown sfx type: {kind}")


# ---------------------------------------------------------------- mixdown


def reverb(x: array, off: int) -> array:
    n = len(x)
    out = array("d", bytes(8 * n))
    for d in (1557, 1617, 1491, 1422, 1277, 1356):
        d += off
        buf = [0.0] * d
        idx, f = 0, 0.0
        for i in range(n):
            y = buf[idx]
            f = y * 0.7 + f * 0.3
            buf[idx] = x[i] + f * 0.84
            idx = idx + 1 if idx + 1 < d else 0
            out[i] += y / 6
    for d in (556, 441, 225):
        d += off
        buf = [0.0] * d
        idx = 0
        for i in range(n):
            b = buf[idx]
            y = -out[i] + b
            buf[idx] = out[i] + b * 0.5
            idx = idx + 1 if idx + 1 < d else 0
            out[i] = y
    return out


def write_wav_f32(path: Path, left, right):
    n = len(left)
    data = array("f", [0.0]) * (2 * n)
    data[0::2] = array("f", left)
    data[1::2] = array("f", right)
    raw = data.tobytes()
    header = b"RIFF" + struct.pack("<I", 36 + len(raw)) + b"WAVEfmt " + struct.pack("<IHHIIHH", 16, 3, 2, SR, SR * 8, 8, 32) + b"data" + struct.pack("<I", len(raw))
    path.write_bytes(header + raw)


def render(spec: dict, out: Path):
    mx = build(spec)
    n = mx.n
    duck = array("d", [1.0]) * n
    for k in mx.kicks:
        s0 = int(k * SR)
        for i in range(min(int(0.3 * SR), n - s0)):
            v = 1 - 0.55 * math.exp(-i / SR / 0.09)
            if v < duck[s0 + i]:
                duck[s0 + i] = v
    rv = [reverb(mx.send[0], 0), reverb(mx.send[1], 23)]
    music, fx = [], []
    for c in range(2):
        d, m, f, r = mx.bus["drums"][c], mx.bus["music"][c], mx.bus["fx"][c], rv[c]
        music.append(array("d", (d[i] + (m[i] + r[i] * 0.8) * duck[i] for i in range(n))))
        fx.append(f)
    out.mkdir(parents=True, exist_ok=True)
    write_wav_f32(out / "stem-music.wav", *music)
    write_wav_f32(out / "stem-fx.wav", *fx)
    dur = spec["duration"]
    pre = []
    peak = 1e-9
    for c in range(2):
        ch = array("d", (math.tanh((music[c][i] + fx[c][i]) * 1.4) * min(1, i / SR / 0.01) * min(1, (dur - i / SR) / 0.8) for i in range(n)))
        peak = max(peak, max(abs(v) for v in ch))
        pre.append(ch)
    g = 0.89 / peak
    write_wav_f32(out / "soundtrack.wav", *(array("d", (v * g for v in ch)) for ch in pre))
    print(f"wrote {out/'stem-music.wav'}, {out/'stem-fx.wav'}, {out/'soundtrack.wav'}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("song", help="song spec JSON")
    p.add_argument("--out", default="audio")
    args = p.parse_args()
    render(json.loads(Path(args.song).read_text()), Path(args.out))


if __name__ == "__main__":
    main()
