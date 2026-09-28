# Design

The goal is a video a designer would have made, not one a model generated. Most "AI slop" in video comes from the same handful of habits; avoid them by default.

## Palette

- **Neutral ink** does the work: stage `#09090b`, app surfaces `#0f0f12` → `#1c1c20`, hairline borders at 8–14% white, text `#ededef`, secondary `#a1a1aa`, tertiary `#6b6b74`. These are the kit's defaults in [../assets/kit/kit.css](../assets/kit/kit.css).
- **One restrained tint** from the brand: take the brand color and pull it toward the text color until it is calm (a saturated magenta became `#e2a6ec`). Set `--tint`. Use it on at most one word or one indicator per frame.
- Even when the brand itself looks generic or loud, keep only that tint; the rest stays neutral.
- Semantic colors only where the real UI uses them: green and red for diffs and passing tests, platform colors inside platform UI.
- Light themes work the same way: paper, ink, one tint.

## Never

- Emoji anywhere in ad copy, cards, or feature rows. Use icons. (Emoji inside a mocked chat are fine only if the real message would contain them; usually leave them out.)
- Glow blobs, lens flares, colored radial gradients behind everything, pink flash frames, film grain as decoration.
- Gradient text, gradient buttons, glassmorphism cards stacked on colored backgrounds.
- Generic 3D shapes, abstract "AI" swooshes, stock-photo people, fake dashboards with invented charts.
- Bouncy overshoot on everything, blur-in type, spinning logos.
- Centered-everything layouts with no hierarchy.

## Type

- Ad type: **Geist** 600, tight tracking (−0.04 em), line height ≈ 1. Kickers in **Geist Mono** 500 caps with +0.14 em tracking. Code in Geist Mono.
- Inside a device, use the platform's system font (`system-ui` renders SF Pro in headless Chrome on macOS). Never ship a serif fallback; check stills.
- Sizes: landscape headlines 120–210 px; vertical headlines 90–150 px; body in UI at the UI's real size scaled by the device factor.
- Left-aligned editorial headlines read more designed than centered ones; center only single short lines.

## Icons

- **Lucide** (ISC) for every UI and feature icon, stroke 1.5–2, sized consistently, in the text color. `fetch_assets.py --icons name,…` pulls them; names at https://lucide.dev/icons.
- Brand glyphs (GitHub, WhatsApp, Telegram) from **simple-icons** (CC0), only where the real UI shows them.
- The product's own logo from its source, drawn as SVG through `window.LOGO`.
- Icon tiles: a 1 px bordered rounded square on a raised surface, icon centered. No colored icon backgrounds unless the real UI has them.

## Motion

- **Masked line reveals** for headlines (each line rises out of a clip), **stamps** for words on the beat (appear at full size with a two-frame settle), **enter** (short rise and fade) for cards and rows.
- **Camera** on app windows: push toward the part that matters, hold while it is read, pull back. Ease in and out; never zoom past legibility.
- **Hard cuts on the beat** between scenes. Where a transition is needed, stagger it (old content out, then new content in) or dip through the background; a plain crossfade between two busy layouts makes a muddy double exposure.
- Typing at a believable speed with a caret; messages landing with a small rise; buttons pressed with a slight scale-down on click; a real cursor path.
- Nothing moves while it is meant to be read.

## Layout checks

On every contact sheet, check: text inside its box at every frame, no line wider than the frame, no collisions between caption and device, consistent margins (72 px on vertical, 160 px on landscape), one focal point per frame, and contrast of secondary text on the darkest surface.
