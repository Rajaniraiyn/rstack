# Deliver

## Master

```sh
python scripts/mix.py --music work/audio/stem-music.wav --fx work/audio/stem-fx.wav \
    --script work/vo-script.json --track wa --vo-dir work/vo --out work/final-wa.wav
python scripts/mix.py --music work/audio/stem-music.wav --fx work/audio/stem-fx.wav --out work/final.wav   # music only
```

Two-pass loudness normalization to −14 LUFS integrated with a −2 dB true-peak ceiling, 48 kHz stereo. AAC encoding can push the true peak up by up to about 1 dB; the ceiling leaves room so the delivered file stays at or below −1 dBFS.

## Poster and mux

Pick the strongest *settled* frame, text fully in and nothing mid-transition, usually the hook once its last word has landed. Render it as a still, then:

```sh
python scripts/deliver.py --video work/video-wa.mp4 --audio work/final-wa.wav \
    --poster work/stills/t001.20.jpg --out launch-video/whatsapp/video.mp4
```

The poster replaces frame 0 rather than adding a frame, so duration and sync stay the same and every platform's thumbnail shows it; it is also saved as `poster.jpg` beside the video. The script prints duration, size, loudness, and true peak, and warns when the peak is above −1 dBFS or the file is over 25 MB (raise `--crf`).

## Share copy

`share-copy.txt` per cut: one to three sentences, postable as is, specific, in the video's voice. No "excited to share", no emoji strings, no hashtags unless asked. First person for creator cuts; name, one-line claim, and link for product cuts. Every claim must be true (see [inspect.md](inspect.md)).

## Report

Tell the user, briefly:

- where each cut, poster, and share copy is, and its duration and size;
- the creative angle in one sentence;
- accuracy decisions that change how the video looks (for example why replies are on the right, or why a privacy line is worded carefully);
- what was verified (stills reviewed, speech recognition on the voice, loudness) and that they should listen once before posting;
- that the output folder is untracked;
- one line offering the next useful iteration (another tone, format, platform, or voice).
