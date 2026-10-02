# Voiceover

A voiceover must sound like a person talking, not a narrator reading. Use speech recognition to check wording and timing. Use listening tools when available; otherwise disclose that delivery and naturalness need a listening check.

## Write for the voice

- Lines are short, spoken, and conversational, with contractions. First person for creator-style vertical cuts ("I just texted my own WhatsApp."), a warm narrator for landscape ("Hand it off.").
- Say what the screen cannot, or say the screen's words on the beat. Never read a paragraph the viewer is also reading.
- Spell everything as it should be spoken: "two a.m." not "2am", "ninety-one" not "91", "Abacus A.I." not "AbacusAI". The checker normalizes both sides, so matches still pass.
- Give each line a slot: `start` and `max` (latest end) from the storyboard. Leave a breath between lines, and let the music swell in the gaps.
- Split long lines rather than rushing them; a line that overruns its slot by more than ~0.2 s should be rewritten, not sped up.
- If recognition or listening reveals a misheard product name, isolate it or add a pause before the troublesome word. Keep natural phrasing when it already works.

The script format is [../assets/examples/vo-script.json](../assets/examples/vo-script.json): tracks per cut, lines with `id`, `start`, `max`, `text`, optional `must` (words that must be heard exactly, such as the product name), and `{"ref": id}` to reuse a line across cuts so it is generated once.

## Engines

- **Local, default:** Chatterbox (Resemble AI, MIT). `uv run scripts/vo_gen.py script.json --out work/vo` writes `<id>_t<k>.wav` takes. It uses Apple Silicon MPS, CUDA, or CPU; the first run downloads a few GB. It embeds an imperceptible Perth watermark; leave it on. If it fails with `pkg_resources` errors, the pinned `setuptools<81` in the script header is missing.
- **API, when authorized:** ElevenLabs, OpenAI, or another TTS service. Use existing spending authorization or obtain it when missing, check the provider's current docs for model and voice names, and write takes with the same naming (`<id>_t<k>.wav`) so the checker can pick them.
- Use a stock or designed voice. Do not clone a real person's voice without their consent.

Starting settings for the bundled workflow, to adjust against actual wording and delivery: `exaggeration` 0.5 (0.55 for short punchy lines), `cfg_weight` 0.4, `temperature` 0.75, generate additional takes only where the available takes fail wording, timing, or listening checks.

## Pick takes with speech recognition

```sh
uv run scripts/vo_check.py pick work/vo-script.json --vo work/vo
```

Whisper transcribes every take; a take passes when its words match (fuzzy score ≥ 90 after normalizing numbers and acronyms), every `must` word is heard exactly, and it fits its slot. The best passing take is copied to `<id>.wav` and summarized in `report.json`. For lines that fail: rewrite, re-time, or generate more takes for just those ids.

## Check the mix, not only the takes

A take that passes alone can fail under music. After mixing:

```sh
uv run scripts/vo_check.py check work/final-wa.wav
uv run scripts/vo_check.py check work/final-wa.wav --start 19.9 --len 2.2 --model medium.en --expect "Abacus A.I. Bot."
uv run scripts/vo_check.py check work/vo/X9_t0.wav --bed work/audio/stem-music.wav --at 20.05
```

Whole-track transcripts can drift on a word because of the sentence before it; transcribe the slice alone with the larger `medium.en` model before rewriting. If the larger model still mishears it, a viewer might too: rephrase and regenerate.

## Mix

`scripts/mix.py` puts each line at its start time and processes the voice (85 Hz high-pass, a light 4 kHz presence lift, level match to −19 dBFS RMS, 2.5:1 compression, a little room). The music ducks about −9.5 dB under speech with eased ramps (in 0.14 s before a line, out 0.45 s after), effects only about −3.5 dB. Music automation from the script's `mix.music_automation` (keyframes in dB) handles the rest: hold the intro a little lower so the drop lands, pull back briefly before the outro, then bloom. The end fade never cuts the voice mid-word.
