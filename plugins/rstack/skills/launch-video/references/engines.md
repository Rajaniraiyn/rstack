# Video engines

Checked against the linked upstream documentation and skills on 3 October 2026. Resolve current package versions, flags, and native requirements before setup. This reference is routing and handoff guidance, not a bundled implementation of those frameworks.

## Choose from requirements

| Engine | Fits | Costs and limits |
| --- | --- | --- |
| Remotion | Existing React app, reusable compositions and props, captions, Studio editing | JS dependencies and browser rendering; confirm licensing for intended use |
| fframes | Rust/SVG composition, native frame inspection and strips, suitable GPU rendering | Rust build and FFmpeg/Skia native dependencies; first-build cost and backend availability |
| Bundled HTML | Short custom clip with an installed browser and ffmpeg | Sequential frame capture; no Studio or built-in timeline editor |
| Hyperframes | Existing HTML/GSAP composition or requested framework | Framework setup; follow its current validator and rendering contract |

Respect an explicit choice. For an existing video project, use its lockfile and commands. For a new project, consider the user's editing needs and available toolchain. Time a representative scene at the requested dimensions and fps before proposing a migration for performance. Render time alone excludes setup and compile cost.

## Remotion

Use the [official skills](https://www.remotion.dev/docs/ai/skills) and [source repository](https://github.com/remotion-dev/skills) for current implementation details. Discover before installing:

```sh
bunx --bun skills add remotion-dev/skills --list
```

If installation is part of the task, select the relevant upstream skill through the CLI. R Stack does not copy Remotion's APIs or router into this directory. If no skill is installed, the official docs remain sufficient.

In an existing project, use its package manager and pinned CLI. Model scenes as compositions with explicit dimensions, fps, frame duration, and props. Drive motion from frame state with Remotion primitives rather than wall-clock timers. Keep packages on compatible versions and wait for fonts and media.

Examples, from the [render CLI](https://www.remotion.dev/docs/cli/render) and [still CLI](https://www.remotion.dev/docs/cli/still). Replace the entry point and composition ID with the project's real values; pass both to avoid an interactive picker:

```sh
bunx --bun remotion still src/index.ts Launch work/hook.png --frame=30
bunx --bun remotion render src/index.ts Launch work/video.mp4 --codec=h264
```

Use a props file when necessary, which avoids platform-specific inline JSON quoting. Sample scene boundaries and transition midpoints in frames. Studio supplies interactive review; export the MP4 when the requested deliverable is a finished video. Upstream skills may default to preview, so keep the user's requested outcome explicit in the composition brief.

## fframes

Use the [official project](https://github.com/dmtrKovalenko/fframes), its [skill](https://github.com/dmtrKovalenko/fframes/blob/main/skills/fframes-video/SKILL.md), and [API docs](https://docs.rs/fframes/latest/fframes/). Discover from either source:

```sh
bunx --bun skills add https://fframes.studio --list
bunx --bun skills add dmtrKovalenko/fframes --list
```

Check Rust, the generator, FFmpeg libraries, and backend requirements using the current README. Prefer an existing pinned project. For new work, use `cargo fframes new` only after choosing the output folder and verifying installed help. Use the supported CPU backend when GPU requirements cannot be met; do not assume GPU rendering works in a headless environment.

Represent the video as scenes returning SVG from frame state. Prepare media and expensive data outside per-frame rendering. Use the generated project's CLI in release mode. These examples follow the upstream skill; confirm commands against the installed release:

```sh
cargo run --release -- timeline
cargo run --release -- inspect
cargo run --release -- strip -n 12
cargo run --release -- frame 1s
cargo run --release -- render -o work/video.mp4
cargo run --release -- audio analyze
```

Open strips and full-size frames to check them. Inspection catches some missing assets and canvas overflow, but it does not prove text fits its own box. Preview tests motion and sound where available. If snapshot tests create a baseline, inspect it before treating it as approved. Measure actual rendering performance rather than repeating upstream speed claims.

## Hyperframes and the bundled path

Use [Hyperframes upstream](https://github.com/heygen-com/hyperframes) when that engine is selected. The [vendored /brag route](brag/README.md) supplies historical planning context; current framework docs govern its API and commands. Hyperframes and fframes are separate projects.

For bundled HTML, follow [render.md](render.md). Its deterministic `render(t)` contract is specific to that renderer and should not be forced onto an external framework.

## Shared delivery contract

Pass the selected engine the storyboard, real assets and claim sources, aspect ratio, fps, duration, captions, and audio ownership. The engine returns source, rendered frames for review, and an intermediate or final video.

If the engine already mixes and masters audio, verify that output directly. Otherwise render a silent intermediate and use the bundled mix and delivery helpers. Never mux a second soundtrack over an already mixed one by accident. Keep a settled poster beside the video; replacing frame zero is optional and does not control every platform's thumbnail selection.

Record engine version, commands, checks, and limitations in the plan. A documented route is not an end-to-end certification of every machine or backend.
