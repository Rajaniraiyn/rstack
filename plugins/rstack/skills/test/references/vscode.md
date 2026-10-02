# VS Code extensions

Identify desktop, web, remote, or multiple extension targets. Native Node access in the desktop Extension Host differs from a browser worker, and remote placement can move filesystem and process execution away from the UI machine. Test the declared target and repository-supported VS Code versions.

Use [VS Code's extension test tooling](https://code.visualstudio.com/api/working-with-extensions/testing-extension), including `@vscode/test-cli` and `@vscode/test-electron`, for integration with the real Extension Development Host. Use the [web extension test route](https://code.visualstudio.com/api/extension-guides/web-extensions#test-your-web-extension) for web targets. Prefer the existing config, pinned runtime, isolated profile, and fixture workspace. Running extension functions in a normal unit runner does not prove activation or host registration.

Check activation events, contributed commands, settings, keybindings, menus, editor/document changes, and deactivation. Include workspace trust, empty/multi-root workspaces, virtual/remote filesystem behavior, cancellation, and reload when relevant. Exercise APIs through `vscode.workspace.fs` and actual URI schemes when the extension promises virtual or remote support; local-path fixtures cannot establish it. Collect Extension Host errors as well as workbench errors. Run packaged VSIX smoke checks for asset and manifest failures that a source launch can hide.

## Webviews and nested frames

A webview has its own document and may contain nested frames. Inspect the frame tree and target the actual content frame. Reacquire after reload, disposal, or recreation; do not assume an old frame handle still represents the panel. Plain browser testing can cover renderer logic, but needs a real-host check for the VS Code bridge.

Exercise message delivery in both directions, readiness, request correlation, cancellation, malformed/stale messages, panel disposal, and restored state. Test resources through `asWebviewUri`, declared local resource roots, and the real CSP. Do not disable CSP or replace `acquireVsCodeApi()` with a permissive stub to claim integration success. Check focus and keybinding conflicts between editor, panel, and inner input in an isolated workbench. Use [os-automation.md](os-automation.md) when the driver needs foreground input. [VS Code webview guide](https://code.visualstudio.com/api/extension-guides/webview).

For workbench UI automation, use a repository-owned driver compatible with the chosen VS Code build. Accessible locators are preferable to internal CSS; workbench DOM is not a stable extension API. If only API integration is available, report command coverage separately from user-visible panel coverage.
