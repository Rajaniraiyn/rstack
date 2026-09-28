# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "faster-whisper",
#   "rapidfuzz",
#   "numpy",
#   "soundfile",
# ]
# ///
"""Check voiceover with speech recognition: pick the best takes, or audit a mix.

You cannot listen, so Whisper listens for you. `pick` transcribes every take
(<vo>/<id>_t<k>.wav, from any TTS engine), keeps takes whose words match the
script (fuzzy score >= 90) and that fit their slot, and copies the winner to
<vo>/<id>.wav. `check` transcribes a finished mix or a slice of it; add --bed
to hear a take over the music the way a viewer will.

Usage:
  uv run vo_check.py pick vo-script.json --vo vo
  uv run vo_check.py check final-wa.wav
  uv run vo_check.py check final-wa.wav --start 19.9 --len 2.2 --model medium.en
  uv run vo_check.py check vo/X9_t0.wav --bed audio/stem-music.wav --at 20.05 --duck -9.5
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from rapidfuzz import fuzz

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def words(n: int) -> str:
    """Spell an integer below 10,000 the way a script would write it for the voice."""
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])
    if n < 1000:
        return ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + words(n % 100))
    return words(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + words(n % 1000))


def norm(s: str) -> str:
    """Compare what was said, not how it was written: '2am' == 'two a.m.', '91' == 'ninety-one'."""
    s = s.lower().replace(",", "")
    s = re.sub(r"\b([a-z])\.\s?(?=[a-z]\.)", r"\1", s)  # a.i. -> ai, a.m. -> am
    s = re.sub(r"(\d)([a-z])", r"\1 \2", s)  # 2am -> 2 am
    s = s.replace(".", " ")
    s = re.sub(r"\b\d{1,4}\b", lambda m: words(int(m.group())), s)
    s = s.replace("-", " ")
    s = re.sub(r"[^a-z0-9' ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def model(size: str):
    from faster_whisper import WhisperModel
    return WhisperModel(size, device="cpu", compute_type="int8")


def transcribe(m, path, prompt=None) -> str:
    segs, _ = m.transcribe(str(path), beam_size=5, language="en", initial_prompt=prompt)
    return " ".join(s.text.strip() for s in segs).strip()


def cmd_pick(args):
    script = json.loads(Path(args.script).read_text())
    lines = {l["id"]: l for t in script["tracks"].values() for l in t if "id" in l}
    if args.ids:
        lines = {k: v for k, v in lines.items() if k in args.ids}
    vo = Path(args.vo)
    m = model(args.model)
    report_path = vo / "report.json"
    report = json.loads(report_path.read_text()) if report_path.exists() else {}
    for lid, line in lines.items():
        slot = line["max"] - line["start"]
        takes = sorted(vo.glob(f"{lid}_t*.wav"))
        if not takes:
            print(f"{lid}: no takes found")
            continue
        best = None
        for take in takes:
            info = sf.info(str(take))
            dur = info.frames / info.samplerate
            heard = transcribe(m, take)
            score = fuzz.ratio(norm(heard), norm(line["text"]))
            # words that must be heard exactly, e.g. a product name ("Bot" is often heard as "bought")
            missing = [w for w in line.get("must", []) if norm(w) not in norm(heard).split()]
            ok = score >= 90 and dur <= slot + 0.02 and not missing
            cost = (0 if ok else 1000) + (100 - score) * 2 + abs(dur - 0.8 * slot) * 10
            print(f"{'OK ' if ok else '-- '}{take.name}  {dur:.2f}/{slot:.2f}s  score={score:.0f}  heard: {heard}{'  missing: ' + ', '.join(missing) if missing else ''}", flush=True)
            if best is None or cost < best[0]:
                best = (cost, take, dur, score, heard, ok)
        _, take, dur, score, heard, ok = best
        shutil.copy(take, vo / f"{lid}.wav")
        report[lid] = {"take": take.name, "dur": round(dur, 2), "slot": round(slot, 2), "score": round(score), "heard": heard, "ok": ok}
    report_path.write_text(json.dumps(report, indent=1))
    bad = [k for k, v in report.items() if k in lines and not v["ok"]]
    print("\nall lines pass" if not bad else f"\nneeds attention (rewrite, re-time, or more takes): {', '.join(bad)}")


def cmd_check(args):
    path = Path(args.audio)
    tmp = None
    if args.start is not None or args.bed:
        w, sr = sf.read(str(path), always_2d=True)
        w = w.mean(axis=1)
        if args.start is not None:
            w = w[int(args.start * sr): int((args.start + (args.len or 3.0)) * sr)]
        if args.bed:
            b, bsr = sf.read(args.bed, always_2d=True)
            b = b.mean(axis=1)
            if bsr != sr:  # crude but adequate for an intelligibility check
                b = np.interp(np.arange(0, len(b), bsr / sr), np.arange(len(b)), b)
            s = int((args.at or 0.0) * sr)
            bed = b[s: s + len(w)] * 10 ** (args.duck / 20)
            w = w[: len(bed)] + bed
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(tmp.name, w.astype(np.float32), sr)
        path = Path(tmp.name)
    m = model(args.model)
    segs, _ = m.transcribe(str(path), beam_size=5, language="en", initial_prompt=args.prompt)
    for s in segs:
        print(f"{s.start + (args.start or 0):6.2f}-{s.end + (args.start or 0):6.2f}  {s.text.strip()}")
    if args.expect:
        heard = transcribe(m, path, args.prompt)
        print(f"\nmatch {fuzz.ratio(norm(heard), norm(args.expect)):.0f}/100 against: {args.expect}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("pick")
    a.add_argument("script")
    a.add_argument("ids", nargs="*")
    a.add_argument("--vo", default="vo")
    a.add_argument("--model", default="small.en")
    b = sub.add_parser("check")
    b.add_argument("audio")
    b.add_argument("--start", type=float)
    b.add_argument("--len", type=float)
    b.add_argument("--bed", help="music stem to lay under the audio")
    b.add_argument("--at", type=float, help="where in the bed the audio starts (s)")
    b.add_argument("--duck", type=float, default=-9.5, help="bed level in dB")
    b.add_argument("--expect")
    b.add_argument("--prompt", help="Whisper initial prompt, e.g. the product name spelled correctly")
    b.add_argument("--model", default="small.en")
    args = p.parse_args()
    cmd_pick(args) if args.cmd == "pick" else cmd_check(args)


if __name__ == "__main__":
    main()
