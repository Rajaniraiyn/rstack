# Browser extensions

Identify manifest version, build output, supported browsers, requested permissions, and extension contexts. Test the built extension, not a standalone page that only resembles its UI.

For Playwright, use bundled Chromium with a persistent context and a temporary user-data directory. Current Chrome/Edge removed relevant command-line sideload flags; do not assume arbitrary branded-browser launches still support them. Discover the extension ID from the actual loaded context rather than hard-coding a development ID. [Playwright extension guide](https://playwright.dev/docs/chrome-extensions).

For Manifest V3, inspect service-worker readiness and collect worker errors. Assert registration before triggering the event, then trigger through the real event source; directly calling a worker handler bypasses browser dispatch. Exercise fresh startup and worker suspension/restart so global in-memory state is not mistaken for durable storage. A debugger can change worker lifetime; account for that during lifecycle verification. Check `chrome.storage`, alarm behavior, event registration, and message responses across restarts. [Chrome service-worker lifecycle](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle).

Separate coverage by context:

- Content scripts on allowed and disallowed real URLs, initial load and SPA navigation, isolated-world interactions, iframe injection, and host-permission changes.
- Popup, options, side panel, and offscreen documents where present. Opening a popup URL as a normal tab tests its document, but does not reproduce toolbar popup focus, closure, or sizing.
- Messages between page, content script, worker, and UI. Include absent receivers, delayed responses, duplicate events, reload, and rejected permissions.
- Install/update/uninstall and persisted configuration. Test packaged assets, CSP, network restrictions, browser API availability, and minimum declared versions.

Use [Chrome's end-to-end guidance](https://developer.chrome.com/docs/extensions/how-to/test/end-to-end-testing) for actual browser UI actions when those are the behavior under test. browser-control can inspect a configured existing extension workflow, but don't replace controlled installation tests with the user's personal profile. Firefox and Safari extensions need their own packaging/runtime checks; Chromium success is not portability evidence. Use [os-automation.md](os-automation.md) for toolbar or permission interactions requiring native input.
