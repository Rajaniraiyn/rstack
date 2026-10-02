# Deliver

For an external renderer that already owns the final mix, verify its encoded output directly. Use the bundled mastering and mux steps only for separate video and audio intermediates.

## Master

```sh
python scripts/mix.py --music work/audio/stem-music.wav --fx work/audio/stem-fx.wav \
    --script work/vo-script.json --track wa --vo-dir work/vo --out work/final-wa.wav
python scripts/mix.py --music work/audio/stem-music.wav --fx work/audio/stem-fx.wav --out work/final.wav   # music only
```

Two-pass loudness normalization to −14 LUFS integrated with a −2 dB true-peak ceiling, 48 kHz stereo. AAC encoding can increase true peak. The ceiling leaves headroom, but measure the final encode rather than assuming it stays below −1 dBFS.

## Poster and mux

Pick the strongest *settled* frame, text fully in and nothing mid-transition, usually the hook once its last word has landed. Render it as a still, then:

```sh
python scripts/deliver.py --video work/video-wa.mp4 --audio work/final-wa.wav \
    --poster work/stills/t001.20.jpg --out launch-video/whatsapp/video.mp4
```

The poster replaces frame 0 rather than adding a frame, so duration and sync stay the same; platform thumbnail selection varies. The delivered opening frame is encoded as a real JPEG in `poster.jpg`, including when the input poster is PNG. The script prints duration, size, loudness, and true peak, and warns when the peak is above −1 dBFS or the file is over 25 MB. The size warning is a heuristic, not a platform limit; check the destination’s current requirements before raising `--crf` or changing resolution.

## Share copy

`share-copy.txt` per cut: one to three sentences, postable as is, specific, in the video's voice. No "excited to share", no emoji strings, no hashtags unless asked. First person for creator cuts; name, one-line claim, and link for product cuts. Every claim must be true (see [inspect.md](inspect.md)).

## Report

Tell the user, briefly:

- where each cut, poster, and share copy is, and its duration and size;
- the creative angle in one sentence;
- accuracy decisions that change how the video looks (for example why replies are on the right, or why a privacy line is worded carefully);
- what was verified (stills reviewed, speech recognition on the voice, loudness) and that they should listen once before posting;
- the output folder's git tracking status, if checked;
- material limitations, including any unavailable playback or listening check.
