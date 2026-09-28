---
name: launch-video
description: "Make short, polished launch and promo videos for a project, product, or website: landscape, vertical, and square cuts with motion, a mixed soundtrack, optional human-sounding voiceover, a poster frame, and share copy, all rendered locally from HTML. Use when the user says \"make a launch video\", \"brag about this\", \"/brag\", \"promo video\", \"demo video\", \"make a vertical version\", \"Reels / TikTok / Shorts cut\", \"add a voiceover\", or wants to show off something they built."
license: MIT
compatibility: Needs Python 3.10+, Chrome or Chromium, and ffmpeg. Voiceover also needs uv plus a few GB for local Chatterbox and Whisper models, or a TTS API key.
metadata:
  trigger: launch video, brag, promo video, demo video, product video, vertical video, reels, tiktok, shorts, voiceover, show off, announce
---

# Launch video

You make the whole video yourself: story, visuals, sound, voice, render. Each scene is an HTML page whose `render(t)` is a pure function of time; a stdlib renderer drives headless Chrome frame by frame, a small synth writes music and sound effects in one key, an optional local TTS voice is checked by speech recognition because you cannot listen, and ffmpeg masters and muxes. The result should feel like a modern, slick launch video: nothing on screen or in the soundtrack that does not earn its place, and nothing that reads as AI slop.

## Options

Read options from flags or plain language. Ask only when a missing choice would change the video.

| Option | Default |
|---|---|
| Input | the current project; or a URL / domain; ask if neither |
| Focus | the whole product; or the feature, release, or angle the user names |
| Tone | inferred; see [references/story.md](references/story.md) |
| Formats | landscape 1920×1080; vertical 1080×1920; square 1080×1080; 30 fps |
| Duration | about 20 s (15–25) |
| Voiceover | off; on when asked, with local TTS unless an API key is available |
| Platform variants | one per chat app or channel the user names (for example a WhatsApp and a Telegram cut) |

## Output

Write deliverables to `launch-video/` in the current directory, or `launch-video-YYYY-MM-DD-HHmmss/` if it exists. One subfolder per cut (`landscape/`, `vertical/`, `whatsapp/`, …), each with `video.mp4`, `poster.jpg`, and `share-copy.txt`; one `plan.md` at the top; every intermediate (pages, stills, stems, takes) in `work/`. Never overwrite an earlier iteration; each round gets its own timestamped folder so the user can compare. Tell the user the output folder is untracked and should be ignored or moved before committing.

## Workflow

1. **Inspect.** Gather real material and verify how the product actually behaves before designing anything. [references/inspect.md](references/inspect.md)
2. **Plan.** Answer the brief questions, pick the angle and hook, and write `plan.md` with a beat-timed storyboard. [references/story.md](references/story.md)
3. **Design.** Neutral palette with one restrained brand tint, real type, Lucide icons, no emoji, no glow blobs. [references/design.md](references/design.md). Any device, chat app, OS surface, or third-party UI follows [references/ui-mocks.md](references/ui-mocks.md).
4. **Build.** Set up `work/` with `scripts/fetch_assets.py`, start from a template in `assets/templates/`, and replace every product-specific string, time, and component. [references/render.md](references/render.md)
5. **Check stills.** Contact sheets of every scene and every transition (`scripts/render.py sheet`). Look at them, fix overflow, collisions, clipped text, wrong fonts, and muddy crossfades, and look again.
6. **Render** each cut to `work/` (`scripts/render.py video`).
7. **Sound.** Write a song spec from the storyboard and run `scripts/synth.py`: music and effects in one key, stems kept separate. [references/sound.md](references/sound.md)
8. **Voiceover** (when asked). Script lines to fit their slots, generate takes, pick them with speech recognition, and fix what fails. [references/voiceover.md](references/voiceover.md)
9. **Mix, master, deliver.** `scripts/mix.py` ducks the music under the voice and masters to −14 LUFS; `scripts/deliver.py` muxes, bakes the poster in as frame 0, and verifies. Write share copy and report. [references/deliver.md](references/deliver.md)

For a quick music-only cut, steps 8 and part of 9 fall away: master the stems with `mix.py` and no script.

## Alternate pathways

The default path above builds everything with this skill's scripts. The original `/brag` skills, vendored in [references/brag/](references/brag/README.md), cover other routes; take one when it fits better, and keep this skill's accuracy, design, and voiceover checks either way:

- **Hyperframes composition** ([references/brag/brag.md](references/brag/brag.md)) when Hyperframes and its skills are installed or the user asks for it.
- **Stock music with beat sync** ([references/brag/references/audio.md](references/brag/references/audio.md)): analyze any track with `scripts/brag/analyze_music_cues.py` and snap the storyboard to its cues instead of synthesizing.
- **Kokoro narration** as a lighter local voice than Chatterbox.
- **Slim** ([references/brag/slim.md](references/brag/slim.md)): one quick cut with whatever tools the machine has, when these scripts cannot run.

## Creative laws

- **Short.** 15–25 seconds; 18–22 is the sweet spot.
- **Clear to a stranger.** After one viewing, someone who has never heard of it knows what it does, who it is for, and how to get it.
- **The hook is everything.** The first two seconds decide whether anyone keeps watching. Plan the hook first, and make frame 0 postable.
- **Show the thing.** Reuse the real UI, copy, logo, data, and flows from the source. Prefer the working product doing its job over a landing page describing it. Small illustrative UI text is fine; invented claims, numbers, testimonials, and reviews are not.
- **Specific.** It must feel made for this exact project, in its own words. No generic SaaS language.
- **True.** Every screen behaves the way the real product and platform behave. Check the code or docs; see [references/inspect.md](references/inspect.md).
- **Readable.** Pace comes from motion and cuts, not from pulling text early. Any line meant to be read stays settled about 0.3 s per word.
- **Alive.** Typing, clicks, messages landing, camera pushes, and beats beat static slides.
- **Every frame postable.** Any frozen frame should be worth sharing.

## Iterating

Treat feedback as a new round in a new folder. Keep what the user liked (say so), change what they named, and re-check everything the change touches. "Feels like AI" or "slop" means [references/design.md](references/design.md) was not followed closely enough: palette, emoji, icons, glows, generic type, fake-looking UI. "Make it real" means [references/ui-mocks.md](references/ui-mocks.md). New platforms or formats reuse the same story with each platform's true behavior.

## Guardrails

- Never invent product facts, numbers, or quotes. Real diffs, real test output, real release notes, real UI strings beat plausible ones.
- Do not imitate a real person's voice or likeness, and do not use a voice clone without that person's consent. Keep the TTS engine's watermark on.
- Brand marks of third parties (GitHub, WhatsApp, Telegram) appear only as they would on screen in real use, not as endorsement.
- Ask before paid API calls (TTS, stock media). Local tools first.
- You cannot hear audio. Verify voice with speech recognition and loudness with measurements, and say in the report that the user should listen once before posting.

## Scripts

All run from any directory; paths are relative to this skill.

| Script | Does |
|---|---|
| [scripts/fetch_assets.py](scripts/fetch_assets.py) | set up `work/`: kit, Lucide icons, brand glyphs, Geist fonts, starter templates |
| [scripts/render.py](scripts/render.py) | stills, contact sheets, and video from a `render(t)` page (stdlib, headless Chrome) |
| [scripts/synth.py](scripts/synth.py) | soundtrack from a song spec: music and fx stems (stdlib) |
| [scripts/vo_gen.py](scripts/vo_gen.py) | voice takes with local Chatterbox (`uv run`) |
| [scripts/vo_check.py](scripts/vo_check.py) | pick takes and audit mixes with Whisper (`uv run`) |
| [scripts/mix.py](scripts/mix.py) | voice chain, ducking, automation, two-pass loudness master (stdlib + ffmpeg) |
| [scripts/deliver.py](scripts/deliver.py) | mux, poster as frame 0, verify duration and loudness |
| [scripts/brag/analyze_music_cues.py](scripts/brag/analyze_music_cues.py) | tempo, beat grid, and strong cues for a stock track (`uv run`; vendored from /brag) |

Examples: [assets/examples/song.json](assets/examples/song.json), [assets/examples/vo-script.json](assets/examples/vo-script.json). Templates: [assets/templates/landscape.html](assets/templates/landscape.html), [assets/templates/vertical-chat.html](assets/templates/vertical-chat.html).

## Reference files

- [references/inspect.md](references/inspect.md): gathering material and verifying behavior
- [references/story.md](references/story.md): brief, angle, hook, shapes, tones, storyboard, copy
- [references/design.md](references/design.md): palette, type, icons, motion, layout, anti-slop checks
- [references/ui-mocks.md](references/ui-mocks.md): iOS, WhatsApp, Telegram, lock screen, desktop, GitHub, terminal
- [references/render.md](references/render.md): page contract, kit, camera, stills, pitfalls
- [references/sound.md](references/sound.md): song spec, effects in key, levels
- [references/voiceover.md](references/voiceover.md): writing for voice, engines, take picking, pronunciation
- [references/deliver.md](references/deliver.md): mix, master, poster, share copy, report
- [references/brag/README.md](references/brag/README.md): the vendored `/brag` and `/brag-slim` skills (MIT) and when to use them
