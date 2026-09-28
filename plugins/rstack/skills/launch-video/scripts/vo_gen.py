# /// script
# requires-python = ">=3.10,<3.12"
# dependencies = [
#   "chatterbox-tts",
#   "setuptools<81",  # Chatterbox's Perth watermarker still imports pkg_resources
#   "numpy",
#   "soundfile",
# ]
# ///
"""Generate voiceover takes locally with Chatterbox (Resemble AI, MIT license).

Writes <out>/<id>_t<k>.wav for every line in the script (or only the ids you
name). Pick the winners with vo_check.py afterwards. Runs on Apple Silicon
(MPS), CUDA, or CPU; the first run downloads the model weights (a few GB).
Chatterbox embeds an imperceptible Perth watermark in its output; leave it on.

Usage:
  uv run vo_gen.py vo-script.json --out vo
  uv run vo_gen.py vo-script.json L11 X8 --takes 6 --out vo
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import numpy as np
import soundfile as sf


def trim(w: np.ndarray, sr: int, thr: float = 0.012) -> np.ndarray:
    win = int(0.01 * sr)
    envelope = np.convolve(np.abs(w), np.ones(win) / win, mode="same")
    idx = np.where(envelope > thr)[0]
    if len(idx) == 0:
        return w
    return w[max(0, idx[0] - int(0.04 * sr)): min(len(w), idx[-1] + int(0.09 * sr))]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("script")
    p.add_argument("ids", nargs="*", help="only these line ids")
    p.add_argument("--out", default="vo")
    p.add_argument("--takes", type=int)
    args = p.parse_args()

    script = json.loads(Path(args.script).read_text())
    voice = {"exaggeration": 0.5, "cfg_weight": 0.4, "temperature": 0.75, "takes": 4}
    voice.update(script.get("voice", {}))
    takes = args.takes or voice["takes"]
    lines = {l["id"]: l for t in script["tracks"].values() for l in t if "id" in l}
    if args.ids:
        lines = {k: v for k, v in lines.items() if k in args.ids}

    import torch
    from chatterbox.tts import ChatterboxTTS

    device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
    tts = ChatterboxTTS.from_pretrained(device=device)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for lid, line in lines.items():
        for k in range(takes):
            seed = 1000 + k * 17
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)
            # short punchy lines take a little more energy
            ex = voice["exaggeration"] + (0.05 if len(line["text"]) < 20 else 0.0)
            wav = tts.generate(line["text"], exaggeration=ex, cfg_weight=voice["cfg_weight"], temperature=voice["temperature"])
            w = trim(wav.squeeze(0).cpu().numpy().astype(np.float32), tts.sr)
            path = out / f"{lid}_t{k}.wav"
            sf.write(path, w, tts.sr)
            print(f"{path}  {len(w) / tts.sr:.2f}s", flush=True)


if __name__ == "__main__":
    main()
