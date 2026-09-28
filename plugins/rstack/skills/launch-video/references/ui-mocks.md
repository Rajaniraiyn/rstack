# UI mocks

When the video shows a phone, a chat app, an OS surface, or a third-party site, it must look and behave like the real thing. Viewers know these apps by heart; one wrong color or a notification that could never fire reads as fake. [../assets/templates/vertical-chat.html](../assets/templates/vertical-chat.html) implements everything below; start from it.

Before building any other app's UI, look up its current dark-mode tokens (published palettes, open-source clones, or a real screenshot) and write them down in `plan.md`.

## iPhone and iOS

- Design in points on a 393 × 852 pt screen and scale the whole screen by one factor (a 686 px wide screen is ×1.745; a full-bleed 1080 px lock screen is ×2.748).
- Device: ~108 px corner radius at 710 px wide, a dark titanium frame with a 2 px lighter edge, side buttons, soft drop shadow.
- Status bar 54 pt: time left (SF semibold 17), signal, Wi-Fi, and battery right, Dynamic Island 125 × 37 pt centered at 11 pt from the top, home indicator 134 × 5 pt at the bottom.
- Font `system-ui` (SF Pro). `-apple-system` alone falls back to a serif in headless Chrome.
- Lock screen: lock glyph, date (semibold ~20 pt), large time (bold ~104 pt), flashlight and camera buttons in the bottom corners, notifications as translucent cards (22 pt radius, app icon 38 pt, title bold, "now" at right, body two lines).

## WhatsApp, iOS dark

| Token | Value |
|---|---|
| chat background | `#0b141a` with a low-contrast doodle pattern |
| nav and composer bars | `#111b21`, hairline `rgba(255,255,255,.07)` |
| sent bubble | `#005c4b` |
| received bubble | `#202c33` |
| input field | `#2a3942` |
| text / secondary | `#e9edef` / `#8696a0` |
| read ticks | `#53bdeb` (double check) |
| accent (send button, caret) | `#00a884` |

- Bubbles: 16.5 pt text, 21 pt line, 8 pt radius, a tail on the first bubble of each group, time and ticks floated bottom right inside the bubble.
- Nav: back chevron, round avatar (grey default silhouette when there is no photo), name and subtitle ("You" / "Message yourself" for the self chat), video and call icons.
- Composer: plus, rounded field with a sticker icon, camera and mic; while text is present, a green round send button replaces them.
- Formatting WhatsApp renders: `*bold*`, `_italic_`, `~strike~`, and ``` monospace (a font change, not a boxed block). Links preview with the site's Open Graph image, title, and domain.
- An agent automating the user's linked account sends as the user: its replies are sent bubbles on the right, and the phone does not notify for them.

## Telegram, iOS night

| Token | Value |
|---|---|
| chat background | `#0e1621` with a pattern |
| nav and composer bars | `#17212b` |
| received bubble | `#182533` |
| sent bubble | `#2b5278` |
| input field | `#242f3d` |
| text / secondary | `#f5f5f5` / `#708499` |
| accent (links, send) | `#6ab3f3` |
| sent meta and ticks | `#7da8d3` / `#8fc2f0` |

- Bubbles: ~17 pt radius, time inside at bottom right.
- Nav: "‹ Chats" in the accent at left, centered name with "bot" underneath for bots, round avatar at right.
- Composer: paperclip, rounded field with a smile icon, mic; while typing, a round accent send button with an up arrow.
- Link previews: accent bar at left, site name in accent, bold title, then the image.
- A bot is a separate sender: incoming bubbles, a real notification on the lock screen.
- Check what formatting the product sends. If it strips markdown for Telegram, show plain text.

These are Telegram's classic night-blue values; verify against a current screenshot if the video depends on an exact match.

## Desktop app window

Rebuild the product's own window from its tokens: traffic lights, sidebar (brand, sections, the active item), top bar with the workspace or branch, the main pane. Keep it neutral with the tint on the active item only. Real strings from the locale files.

## Code, diffs, terminals

- Diffs: file header with path and `+N −M`, green and red row tints at ~13%, the gutter sign in its color, syntax colors muted (keywords rose, properties blue, types amber, comments grey).
- Terminal: `#0b0b0d`, mono, the prompt, then output streaming line by line; the pass summary in green. Use real output from a real run when you can.
- Chat bubbles that carry code keep lines short enough for the bubble (about 33 characters at 13 pt on a phone); summarize the change rather than overflow.

## GitHub

- Pull request card (dark): `#0d1117` background, `#30363d` borders, title `#e6edf3`, secondary `#8b949e`, open badge `#238636`, additions `#3fb950`, deletions `#f85149`.
- Social preview card (what chat apps unfurl): white, repo name small at top left, GitHub mark at top right, bold PR title with a grey `#N`, a footer with state, files, and +/−, and a language color bar along the bottom.
