# Design

## Palette

- The [kit palette](../assets/kit/kit.css) uses stage `#09090b`, app surfaces `#0f0f12` to `#1c1c20`, borders at 8–14% white, text `#ededef`, secondary `#a1a1aa`, and tertiary `#6b6b74`.
- Mix the brand color toward the text color to reduce saturation, then set `--tint`. Use it on at most one word or indicator per frame.
- Preserve an established brand palette when the brief calls for it. The neutral kit is a fallback, not a replacement for the product's identity.
- Semantic colors only where the real UI uses them: green and red for diffs and passing tests, platform colors inside platform UI.
- Light themes work the same way: paper, ink, one tint.

## Defaults to avoid

- Emoji anywhere in ad copy, cards, or feature rows. Use icons. (Emoji inside a mocked chat are fine only if the real message would contain them; usually leave them out.)
- Glow blobs, lens flares, colored radial gradients behind everything, pink flash frames, film grain as decoration.
- Gradient text, gradient buttons, glassmorphism cards stacked on colored backgrounds.
- Generic 3D shapes, abstract "AI" swooshes, stock-photo people, fake dashboards with invented charts.
- Bouncy overshoot on everything, blur-in type, spinning logos.
- Centered-everything layouts with no hierarchy.

## Type

- For the bundled kit, ad type defaults to **Geist** 600, tight tracking (−0.04 em), line height ≈ 1. Kickers in **Geist Mono** 500 caps with +0.14 em tracking. Code in Geist Mono.
- Inside a device, use the platform's system font and check the resolved font on the rendering machine. `system-ui` varies by platform; bundle a licensed font when exact metrics matter. Check stills for unintended fallback.
- Sizes: landscape headlines 120–210 px; vertical headlines 90–150 px; body in UI at the UI's real size scaled by the device factor.
- Left-align editorial headlines; center only single short lines.

## Icons

- **Lucide** (ISC) is the bundled default for UI and feature icons, stroke 1.5–2, sized consistently, in the text color. `fetch_assets.py --icons name,…` pulls them; names at https://lucide.dev/icons.
- Brand glyphs (GitHub, WhatsApp, Telegram) from **simple-icons** (CC0), only where the real UI shows them.
- The product's own logo from its source, drawn as SVG through `window.LOGO`.
- Icon tiles: a 1 px bordered rounded square on a raised surface, icon centered. No colored icon backgrounds unless the real UI has them.

## Motion

- **Masked line reveals** for headlines (each line rises out of a clip), **stamps** for words on the beat (appear at full size with a two-frame settle), **enter** (short rise and fade) for cards and rows.
- **Camera** on app windows: push toward the part that matters, hold while it is read, pull back. Ease in and out; never zoom past legibility.
- Choose deliberate cuts or a meaningful visual handoff between scenes. Align emphasis with the beat when it helps the story. Use [motion-direction.md](motion-direction.md) for continuity and camera review; a plain crossfade between busy layouts can create muddy double exposure.
- Typing at a believable speed with a caret; messages landing with a small rise; buttons pressed with a slight scale-down on click; a real cursor path.
- Keep readable content settled long enough to read. Background motion can continue if it does not compete with the text.

## Layout checks

On every contact sheet, check: text inside its box at every frame, no line wider than the frame, no collisions between caption and device, consistent margins (72 px on vertical, 160 px on landscape), one focal point per frame, and contrast of secondary text on the darkest surface.
