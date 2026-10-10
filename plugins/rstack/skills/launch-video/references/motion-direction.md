# Motion direction and continuity

Read this when a clip feels like unrelated cards, when the brief requests a continuous camera, or when motion should explain a relationship. Choose the visual idea before the transition technique. For open briefs, consider a few genuinely different concepts internally; involve the user when a consequential direction is unresolved or a concept review was requested. Do not add a mandatory approval round to an already authorized render.

## Plan meaningful movement

Give each storyboard beat an observable purpose, focus, action, readable hold, and handoff. A handoff can preserve an object, spatial anchor, gesture, direction, or causal consequence. For example, a submitted document can become the result panel that explains what changed. A deliberate cut is also valid when it clarifies contrast or changes context; continuity is a choice, not a universal score to maximize.

| Beat | What the viewer should understand | Motion and focus | Settled/readable interval | Handoff or deliberate cut |
| --- | --- | --- | --- | --- |
| Submit | The user starts a real operation | Visible input, then follow the result | Hold the actual outcome | Keep the result as the next explanation’s anchor |

Vary pacing with the information being conveyed. Fast emphasis needs contrast with readable rest. Keep the causal action visible where it matters. Do not enforce a fixed cadence, camera shake, aspect ratio, effect count, or minimum shot-length ratio across every brand and audience.

## Inspect motion, not just frames

Review a draft around each handoff at normal speed and inspect nearby frames for jumps, lost subjects, unintended overlaps, and broken tracking. Check that the visual story remains comprehensible without narration when silent viewing matters. A static contact sheet cannot demonstrate smooth movement; measured pixel motion cannot establish narrative quality.

For procedural scenes, seek the same time after different seek histories and compare stable rendered output after assets load. Remove uncontrolled clocks, random state, and accumulating simulation state. Verify important screen bounds after camera transforms, including focus targets and captions. Fonts and assets must resolve before layout measurements.

If rapid travel strobes, first reconsider distance, speed, output fps, and whether the action needs that move. Temporal supersampling can help when supported: evaluate multiple scene states over the shutter interval, then composite samples with correct color handling. It costs extra renders and can smear text. Spatial CSS blur is a different effect. The bundled renderer currently captures one state per frame; it does not implement shutter sampling, continuity scoring, or onetake’s probe API. Do not pass another renderer’s options to it.

Render a representative draft before expensive final settings. Use requested delivery dimensions and frame rate rather than an automatic 4K/60 upgrade. Recheck critical motion on the final encode, where compression and frame-rate conversion can change it. Human playback remains necessary for judging rhythm; report unavailable playback clearly.

[onetake](https://github.com/feitangyuan/onetake) informed continuity, procedural motion, and review methods. See [upstream-workflows.md](upstream-workflows.md) for provenance and licensing.
