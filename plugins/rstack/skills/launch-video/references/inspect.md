# Inspect

Decide what the input is, then gather material. Use the supplied brief and existing conversation before gathering missing material.

| Input | Recognize it by | Material comes from |
|---|---|---|
| Project | no input, and the current directory is a project | the code |
| Website | an `http(s)://` URL or a bare domain | the live site |
| Brief or assets | supplied description, screenshots, brand kit, or recordings | supplied material, with claims verified against available product evidence |

If neither fits, ask what the video is about.

## Project

Read the README, entry screen, styles, routes, key components, locale files, and recent history. Identify the entry, key action, and result of the product flow to show.

- Take UI strings verbatim from locale or component files, including onboarding titles, empty states, button labels, and toasts.
- Use the logo component or SVG, CSS tokens, and fonts. Prefer a vector mark over an app-store PNG when available.
- Use actual diffs, test results, PR titles and counts, and release notes rather than invented data.
- Render the app's components when they work without the backend. Otherwise rebuild the screens from its tokens, strings, and assets and record the substitution in the plan.

## Website

Get the site as a visitor sees it. A plain download of a JavaScript-built page can be an empty shell; if so, load it in the headless browser. Dismiss cookie banners and overlays, and scroll section by section, since scroll-animated content stays blank in a single capture.

- **Copy:** headline, tagline, section headings, feature names, calls to action, testimonials, and the title, meta description, and social-preview tags.
- **Identity:** exact colors from the CSS and the fonts it loads.
- **Visuals:** logo, product screenshots, hero images, demo videos; download what you will use into `work/`.
- **Screenshots** at the video's aspect ratio, to understand layout. In the video, reuse real markup, CSS, and assets and animate them, rather than panning over flat screenshots.
- **The product in use:** demo videos, how-it-works sections, and docs for the entry → key action → result flow.

## Verify behavior before you depict it

Every screen in the video must behave the way the real product and platform behave. Find out from the code or docs, not from assumptions:

- **Who sends what.** An agent acting through a linked account sends as the user (for example WhatsApp linked-device automation: replies are the user's own outgoing bubbles). A bot account is a separate sender (for example a shared Telegram bot: incoming bubbles with a "bot" label).
- **What notifies.** A phone does not notify you about messages your own account sent. Do not build a hook on a notification that could never appear.
- **What formatting survives.** Check how the product formats outgoing text per platform. Some strip markdown for one app and keep bold and code blocks for another.
- **What is local and what is not.** Privacy claims must match the docs exactly: "memory and settings stay local" is not "nothing leaves your machine" if model requests go to a provider.
- **Names.** Use the product's real names for things (the shared bot's display name, the mode names, the model names). If a name comes from a server and you cannot see it, use the generic label the UI shows instead of inventing a handle.

Write these decisions into `plan.md` under an "Accuracy" heading so the next iteration keeps them.

## Brief questions

Resolve these from supplied material and context before planning; ask only for consequential missing information: What is it, in one sentence? Who is it for, and what does it do for them? What sets it apart? What is the most impressive or funniest true thing? What is the visual hook? Which real UI or flow will be shown? What tone fits? What is the one-line share caption?
