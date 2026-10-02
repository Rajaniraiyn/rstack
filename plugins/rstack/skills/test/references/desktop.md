# Desktop apps and embedded webviews

Identify native framework, packaged binary, OS/architecture, window model, and embedded engine. A Chromium renderer, WebView2, WKWebView, and WebKitGTK do not share one universal driver. Test native controls and host integration separately from document logic.

For native OS interaction, read [os-automation.md](os-automation.md). That reference owns background-delivery checks, focus constraints, and isolated-desktop setup.

## Pick the actual host route

| Stack | Starting point and limit |
| --- | --- |
| Electron | Playwright's experimental Electron support can launch the app and access main process and renderer windows. Check its compatibility with the installed Electron version. |
| Tauri | Current Tauri docs recommend WebdriverIO's Tauri service. Its embedded driver supports Windows, Linux, and macOS with test plugins. Direct upstream `tauri-driver` supports Windows/Linux. Choose the route intentionally. |
| WebView2 | Use a supported debugging connection to the test-owned host. DOM checks still need native host/bridge assertions. |
| AppKit, SwiftUI, Catalyst | Apple test tooling on macOS; see [apple.md](apple.md). |
| WinUI/WPF/Win32 | Windows UI Automation; current WinApp CLI offers agent inspection and UI automation. Check framework coverage and installed help. |
| GTK/Qt/other native Linux | Framework tests and accessibility automation through the available AT-SPI tree, where exposed. Check actual display/session support. |
| Flutter | See [flutter.md](flutter.md), plus native-host checks for plugins and dialogs. |

Sources: [Electron API](https://playwright.dev/docs/api/class-electron), [Tauri WebDriver](https://v2.tauri.app/develop/tests/webdriver/), [WebView2](https://playwright.dev/docs/webview2), [Windows testing](https://learn.microsoft.com/en-us/windows/apps/develop/testing/), [WinApp agent testing](https://learn.microsoft.com/en-us/windows/apps/develop/ai-assisted/testing), and [AT-SPI](https://gnome.pages.gitlab.gnome.org/at-spi2-core/).

Use test-only automation plugins/debug ports only for the selected workflow. Do not ship them accidentally in production or open ports beyond the required scope. A custom helper must expose just the needed operations; see [custom-tooling.md](custom-tooling.md).

## Host and webview checks

Enumerate windows and frame trees by identity, not creation order. Handle splash screens, secondary windows, popup views, nested frames, and window replacement. Verify the chosen automation path can reach out-of-process frames. Use an app-owned test interface when it cannot, and retain a real interaction check for wiring that the interface bypasses.

Exercise the bridge in both directions with actual serialization, permissions/capabilities, errors, timeouts, and disposal. Test filesystem/native plugin effects. A browser renderer with mocked IPC establishes only renderer behavior. Include host-origin URLs, CSP, local assets, drag/drop, clipboard, dialogs, menus, tray, deep links, single-instance handling, and close/reopen when relevant.

Test the packaged app for startup, writable paths, assets, signing/sandbox constraints, migrations, and restart persistence. Developer builds often bypass these failures. Compare OS-specific path, permission, keybinding, and WebKit/Chromium behavior.

For input and visual failures, record foreground window, DPI/scaling, monitor layout, display server, theme, and accessibility permissions. Coordinate clicks require a stable window and independent result assertion. Windows elevation and disconnected remote desktops, macOS privacy permissions, and Wayland input/capture restrictions can block automation. Xvfb provides an X11 test display; it does not prove Wayland behavior. Headless DOM tests cannot verify native menus or OS dialogs.
