---
name: launch-video
description: Create a finished product launch, demo, or promo video with a storyboard, motion, sound, poster, and share copy. Use for launch videos, animated product explainers, /brag requests, or social cuts for Reels, TikTok, and Shorts.
license: MIT
compatibility: Rendering needs a chosen local toolchain. Bundled renderer needs Python 3.10+, Chrome or Chromium, and ffmpeg; Remotion needs its JS toolchain; fframes needs Rust and native libraries. Optional local voice checks need uv and model downloads.
---

# Launch video

Deliver a video that shows the real product, communicates one angle, and fits the requested channel. Keep ownership of the story, factual accuracy, review, and deliverables whichever renderer is used.

## Resolve the brief

Use the current project, supplied URL, brief, or assets. Ask only for missing decisions that affect the result. Default to one landscape cut at 1920x1080, 30 fps, about 20 seconds, and no voiceover. Use 1080x1920 for a requested vertical cut and 1080x1080 for square. Duration and formats follow the user's brief; do not generate every aspect ratio by default.

Read [references/inspect.md](references/inspect.md) to gather real UI, behavior, claims, and brand assets. Then use [references/story.md](references/story.md) to choose the hook and write a beat-timed storyboard in `plan.md`. Hold readable text after it settles, about 0.3 seconds per word as a starting point.

## Choose a renderer

Respect the user's engine and an existing project's toolchain. Otherwise choose with [references/engines.md](references/engines.md):

- Remotion for React compositions, reusable props, captions, and interactive Studio editing.
- fframes for Rust and SVG scenes, native inspection, and a suitable GPU or CPU backend.
- The bundled HTML renderer for a small deterministic clip when Python, Chrome, and ffmpeg are already available.
- Hyperframes for an existing Hyperframes composition or the user's requested route.

These alternatives are optional. Installing this skill does not install them. Keep a working engine unless a demonstrated requirement justifies migration. Benchmark a representative scene before claiming a speed advantage.

For continuous-camera motion or disconnected scene changes, read [references/motion-direction.md](references/motion-direction.md). For character explainers, generated clip sequences, prompt-only packages, or localization, read [references/generated-sequences.md](references/generated-sequences.md). [references/upstream-workflows.md](references/upstream-workflows.md) records comparable workflows and their integration limits.

## Build and review

Read [references/design.md](references/design.md) for layout, typography, and motion. Follow the product's brand rather than imposing a new palette. Read [references/ui-mocks.md](references/ui-mocks.md) when depicting a device, chat app, operating system, or other third-party UI.

For the bundled path, read [references/render.md](references/render.md), set up with [scripts/fetch_assets.py](scripts/fetch_assets.py), and adapt the [landscape](assets/templates/landscape.html) or [vertical chat](assets/templates/vertical-chat.html) template. Resolve helper paths from the installed skill directory, not the project's working directory.

Review rendered contact sheets across all scenes and transition midpoints, then key frames at full resolution. Fix text overflow, clipped elements, incorrect fonts, inaccurate UI, and awkward transitions. A still check cannot establish smooth motion; review a draft playback when the available tools permit it.

Use [references/sound.md](references/sound.md) for synthesized stems or licensed stock music with beat cues. Use [references/voiceover.md](references/voiceover.md) only when narration was requested. Confirm wording and timing with transcription, measure loudness, and check the final mix. Transcription does not establish natural delivery; disclose when no listening check was possible.

## Deliver

Use a new output folder or the user's chosen destination. Default to `launch-video/`, then a timestamped sibling for another iteration. Keep `plan.md` at the top, intermediates in `work/`, and a folder per requested cut containing `video.mp4`, `poster.jpg`, and `share-copy.txt`. Preserve previous deliverables and user edits.

Read [references/deliver.md](references/deliver.md) for mastering and final checks. An external renderer can encode its own audio; avoid adding the mix twice. Verify the delivered file's dimensions, fps, duration, audio streams, loudness, and size. Inspect the poster and share copy too.

Report paths, the angle, checks actually performed, and material limitations. Report git tracking status only after checking it. Deliver a render for a finished-video request; if the user requested only a preview or source, stop at that deliverable.

## Constraints

Use verified product facts and properly licensed media. Preserve voice consent and applicable watermark requirements. Follow existing authorization for paid services; an API key alone does not authorize spending. Keep local tools and existing connections available as alternatives.

Use [references/sound.md](references/sound.md) for licensed stock audio, cue timing, and optional audio-reactive motion. Source comparisons stay in [references/upstream-workflows.md](references/upstream-workflows.md); no external skill is bundled.
