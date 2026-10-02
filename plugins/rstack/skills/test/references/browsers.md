# Browser apps

## Choose a driver

| Need | Route |
| --- | --- |
| Repeatable assertions, fixtures, tracing, CI, multiple engines | The project's Playwright or equivalent test runner |
| Interactive Playwright exploration without creating a suite | Playwright CLI, or an available persistent JS session |
| Agent exploration with compact element references | Vercel's agent-browser CLI |
| Existing signed-in Chromium tab, extension state, visible user workflow | anomalyco/browser-control, once its extension and local relay are available |
| Existing supported DevTools automation | Reuse it when it can observe and assert the required behavior |

Playwright is the usual route for durable tests. agent-browser is useful for exploration; turn discovered failures into repository tests when appropriate. Load its version-matched `agent-browser skills get core` guide when available; request `--full` only when the needed references or examples are missing. Take a fresh snapshot after navigation or DOM changes before using element references. Keep a distinct named session for each independent run. Agent snapshots and click success are observations; assert the resulting app state or durable effect. [agent-browser upstream](https://github.com/vercel-labs/agent-browser).

browser-control operates through a browser extension and local relay. Check `doctor` and `status`, then retain the returned session ID for subsequent `execute` calls. Verify the selected tab and browser identity. Adopting an existing tab needs deliberate target selection; preserve user-owned tabs and authentication. Missing extension setup is an environment prerequisite, not a reason to silently automate a different profile. [browser-control upstream](https://github.com/anomalyco/browser-control).

Use the available CLI or tool connection. No MCP server is required just because a tool offers one. Pin dependencies for reproducible repository tests; avoid upgrading a shared running daemon during a test. Read tool-provided skills as versioned operating guidance, not permission to install integrations or change the task.

## Exercise behavior

- Start the correct frontend and backend, verify readiness and base URL, then wait for a specific visible or server-side state. Polling, streaming, and analytics can prevent network idleness. Prefer retrying assertions over fixed sleeps. [Playwright readiness guidance](https://playwright.dev/docs/api/class-page#page-wait-for-load-state).
- Use role, accessible name, label, or a stable test ID. Inspect frame identity and use frame locators for nested iframes. Open shadow roots and closed shadow roots have different automation access; canvas controls need a supported app interface or visual interaction with an independent assertion.
- Subscribe to console, page errors, and failed requests before acting. HTTP error responses need status checks as well as transport-failure listeners. Capture a trace for difficult failures and screenshots for visual evidence.
- Check navigation/back, validation, keyboard focus, loading/error/empty states, reload/persistence, offline recovery, downloads/uploads, and cancellation as relevant. Verify backend effects through an authorized API where needed. Test roles with separate accounts and browser contexts. Context isolation does not isolate shared backend records, mailboxes, queues, or rate limits; give each run distinct fixtures.
- Viewport emulation does not prove mobile Safari, OS permission UI, or installed PWA behavior. Run the required browser/device. Responsive screenshots supplement functional checks. Automated accessibility scans supplement keyboard and assistive-technology checks.
- Keep auth storage, cookies, HAR files, and traces out of public artifacts. Reuse a user profile only when the task calls for it; use isolated profiles otherwise.

Consult [Playwright locators](https://playwright.dev/docs/locators), [frames](https://playwright.dev/docs/frames), and [trace viewer](https://playwright.dev/docs/trace-viewer) for the installed version.
