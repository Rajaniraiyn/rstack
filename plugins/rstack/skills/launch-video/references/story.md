# Story

## Angle and hook

Pick one angle a stranger gets in one viewing, then plan the hook before anything else. Useful hook options:

- **The product's own funny truth.** A real UI string, a real behavior, a real number. ("Committing at 2am?" from the app's own late-night greeting; "Ship it and sleep." from its night greeting.)
- **The payoff first, then rewind.** Open on the finished result (a merged PR, a sent reply), then "Here's how." and rewind the UI.
- **A notification that could really arrive.** Lock screen, phone buzzes, the result lands. Only when the platform would notify (see [inspect.md](inspect.md)).
- **A relatable situation.** "Out for dinner." then the thing still happened.

First-person creator voice ("I shipped this PR from dinner") suits vertical social cuts; a warm narrator or no voice suits landscape.

## Shape

Hook (2–3 s) → reveal or setup (2–4 s) → 2–3 sharp highlights → punchline and outro (2–4 s). A starting shape, not a template. For a product doing a job: ask → work → result → why it is different → name and link.

Put the name, a clear one-line claim, and where to get it (URL, "free", license) in the last three seconds.

## Beat grid

Pick a tempo first (120 bpm makes a beat every 0.5 s and a bar every 2 s) and snap scene cuts, word stamps, message arrivals, and card entrances to beats. Put the drop where the product first appears, usually 3–4 s in, and plan the music's downbeats around it. Record every time in the storyboard; the song spec and the voiceover script reuse them.

## Tones

Presets are defaults; freeform direction ("fake Series A launch from 2016") refines or overrides them.

| Tone | Feel | Pacing and transitions |
|---|---|---|
| `default` | punchy, playful, clean | 4–5 scenes; soft transitions |
| `polished` | serious, elegant, restrained | 3–4 scenes, long holds; soft fades |
| `hooky` | social-first, beat-synced, bold type | 5–6 scenes on the beat; hard cuts and camera pushes |
| `yc-parody` | deadpan startup launch, played straight | 4–5 scenes, one claim each; hard cuts |
| `chaotic` | fast, loud, all caps | 6–8 scenes, some under 2 s; zoom cuts |
| `deadpan` | calm, dry, nothing is a joke | 3–4 scenes, big empty space; slow fades |
| `cinematic` | trailer scale, epic claims | 4–5 scenes, big type; dramatic wipes |
| `app-store` | clean feature cards | 4–6 scenes; smooth slides |

## Formats

- **Landscape 16:9:** app windows with a camera that pushes into the part that matters (the composer while typing, the diff, the terminal), then pulls back.
- **Vertical 9:16:** caption on top (kicker + two-line headline), device below; it must read muted. Keep key text out of the bottom ~250 px and right ~120 px where platform UI overlays sit.
- **Square 1:1:** one idea per frame, centered, larger type.

Same story, different framing: the vertical cut is not the landscape cut shrunk.

## Copy

- Use the product's own words. No generic SaaS language ("streamline your workflow", "supercharge", "unlock", "seamless").
- One idea per headline, two lines at most, a single tinted word at most.
- Kickers in mono caps (`01 — ASK`, `02 — WORK`, `03 — SHIP`) give structure without extra words.
- Numbers only when real, and then specific ("91 passed", "+19 −27").
- Read the finished copy aloud in your head at 0.3 s per word against the scene durations.

## Plan file

Write `plan.md`: what it is, who it is for, angle, hook, highlights, punchline, tone, formats, accuracy decisions, the real material used, and a storyboard table with scene start/end times, purpose, focus/action, readable hold, audio, and the intended handoff or cut. Use [motion-direction.md](motion-direction.md) for continuity planning and [generated-sequences.md](generated-sequences.md) when shots are generated independently. For a round of feedback, add a "What changed" section at the top.
