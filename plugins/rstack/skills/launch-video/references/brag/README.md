# /brag (vendored)

The original `/brag` and `/brag-slim` skills by Shunit Haviv Hakimi, vendored verbatim from https://github.com/latent-spaces/brag at commit `c893c5ed52aed84e3e2ee56787de869fccdae6b0` under the MIT license ([LICENSE](LICENSE)). `launch-video` grew out of `/brag-slim`; these files are kept as alternate pathways, not as the default.

| File | What it is |
|---|---|
| [brag.md](brag.md) | the full `/brag` skill: plan here, compose and render with Hyperframes |
| [slim.md](slim.md) | `/brag-slim`: the model builds the whole video with whatever tools the machine has, no bundled assets |
| [references/step-1-inspect.md](references/step-1-inspect.md) | inspection and the nine-question planning rubric |
| [references/step-2-plan.md](references/step-2-plan.md) | angle, storyboard, and plan format |
| [references/step-3-compose.md](references/step-3-compose.md) | the composition brief handed to Hyperframes |
| [references/audio.md](references/audio.md) | music selection, beat and cue sync, SFX, Kokoro narration |
| [references/step-4-deliver.md](references/step-4-deliver.md) | validate, render, poster, share copy |
| [references/tones.md](references/tones.md) | full definitions of the seven tone presets |

The cue analyzer is vendored at `scripts/brag/analyze_music_cues.py` (only an inline dependency header was added so `uv run` installs librosa).

## Not vendored

- The bundled music (five "Happy Beats / Business Moves" tracks from https://ende.app/en), their cue presets, and the SFX packs under `skills/brag/assets/` upstream: about 15 MB, and the upstream README asks to verify the music license before redistributing. Fetch them from the upstream repository when a run needs them.
- The docs site and example videos.

When `brag.md` says `<skill-dir>/assets/...` or `<skill-dir>/scripts/...`, those paths refer to the upstream repository, not to `launch-video`.

## When to take these pathways

- **Hyperframes (`brag.md`):** the user has Hyperframes and its skills installed, asks for it, or wants its composition, linting, and render tooling. `launch-video` keeps ownership of the story, accuracy, design rules, and voiceover checks; Hyperframes owns composition and rendering.
- **Stock music with beat sync:** the user wants a produced track rather than a synthesized one. Beat-grid the track with `uv run scripts/brag/analyze_music_cues.py track.mp3 --output-json cues.json --output-md cues.md` (tempo, beat grid, strong cues in the first 20–25 s) and snap the storyboard to its cues instead of a fixed 120 bpm grid. Check the track's license first.
- **Kokoro narration:** a lighter local voice than Chatterbox (Apache 2.0, runs on CPU), as `audio.md` describes. Its takes still go through `vo_check.py pick`.
- **Slim (`slim.md`):** a quick single-cut video with no setup, or an environment where the `launch-video` scripts cannot run. Its creative laws and tones are the same ones `launch-video` builds on.
