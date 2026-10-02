# Render

## Set up

```sh
python scripts/fetch_assets.py work/ --template vertical-chat --icons rocket,bell --brands github
```

This copies the kit ([../assets/kit/kit.css](../assets/kit/kit.css), [../assets/kit/kit.js](../assets/kit/kit.js)), writes `icons.js`, downloads Geist fonts, and copies starter pages. Everything a page needs lives in `work/`, loaded by relative path.

## Page contract

A page is one HTML file at the video's exact pixel size.

- It loads `kit.css`, then `icons.js`, then `kit.js`.
- `window.render(t)` sets every element's state from `t` alone: no timers, no CSS transitions or animations, no randomness without a fixed seed. Rendering the same `t` twice gives the same frame, in any order.
- `window.ready` resolves when fonts and images are loaded: `window.ready = kitReady().then(() => { /* measure */ render(0); })`. Measure layout (text widths, bubble heights) inside that callback, after fonts load.
- Scenes are absolutely positioned layers switched with `visibility`. A child with `visibility: visible` shows even inside a hidden parent, so gate each child by its scene's time range too.
- Put all product content in one clearly marked block at the top of the script so the next iteration edits one place.

Kit helpers (all take `t`): `enter(el, t, t0, d, dy)`, `lines(el, t, t0, stagger, d)` for `.ln > span` masked lines, `stamp(el, t, t0)`, `camAt(t, keys)` for eased keyframes, `ic(name, size, color, stroke)` for Lucide, `brand(slug, size, color)`, `logo(size)`.

## Camera

Wrap an app window in a full-frame `#cam` with `transform-origin: 0 0`, key it with `[t, scale, focusX, focusY]`, and apply `translate(W/2 − fx·s, H/2 − fy·s) scale(s)`. A cursor over a camera-moved window must map its target through the same transform.

## Check before the full render

```sh
python scripts/render.py sheet work/vertical-chat.html 0.5 2 4 6 8 10 12 14 16 18 20 --size 1080x1920 --query "?p=wa" --cols 6 --thumb 300 --out work/sheet.jpg
python scripts/render.py stills work/landscape.html 1.9 9.8 --out work/stills
```

Look at every scene and every transition midpoint. Common failures:

| Symptom | Cause and fix |
|---|---|
| serif text in a phone or lock screen | the requested font is unavailable; bundle an authorized font or choose and verify an intentional fallback |
| headline runs off the frame | measure with `offsetWidth` (unaffected by transforms) and split to two lines |
| caption words laid out side by side oddly | a flex container turned inline spans into flex items; wrap the content in one block element |
| text from one scene shows in another | a child `visibility` overriding its hidden scene; gate by time |
| code overflows a chat bubble | shorten lines, or summarize the change |
| muddy frame during a transition | stagger out then in, or dip through the background |
| layout changes after fonts load | measure inside `window.ready`, not at script start |
| emoji render as boxes | the machine lacks the required glyphs; use a suitable font when the real UI or brief requires emoji |

## Render

```sh
python scripts/render.py video work/landscape.html --duration 22.5 --out work/video-landscape.mp4
python scripts/render.py video work/vertical-chat.html --size 1080x1920 --query "?p=tg" --duration 22.5 --out work/video-tg.mp4
```

The renderer is stdlib Python: it starts headless Chrome (`CHROME` overrides the path), drives it over the DevTools protocol, and pipes JPEG frames to ffmpeg (`FFMPEG` overrides the path). Measure rendering speed on this host before estimating completion. Render independent cuts in parallel only within available CPU and memory, with separate output paths. The intermediate is high quality (`--crf 15`); `deliver.py` makes the final encode.
