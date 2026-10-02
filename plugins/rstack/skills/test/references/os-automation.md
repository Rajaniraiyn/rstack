# OS automation without interrupting the user

Prefer semantic actions on a named app/window or a dedicated test desktop. Headless browser contexts and PTYs usually avoid host focus; OS input needs an explicit delivery contract. Restoring focus after an action still interrupts the user. A separate cursor alone does not establish separate keyboard focus, clipboard, dialogs, or desktop state.

## CUA through commands or SDKs

[trycua/cua](https://github.com/trycua/cua) provides Cua Driver for desktop actions and Cua sandboxes/Spaces for isolation. Use the CLI or a small SDK client on demand. Don't register an MCP server or autostart service to run this skill. The driver CLI still needs its local runtime, platform permissions, and a supported desktop session. Upstream installers can offer agent configuration, MCP registration, sign-in, or autostart; inspect their options and select only the runtime needed for this task.

Inspect an installed driver's schema before sending input:

```sh
cua-driver --help
cua-driver status
cua-driver doctor
cua-driver list-tools
cua-driver describe get_window_state
cua-driver describe click
cua-driver describe type_text
cua-driver call list_apps
```

`cua-driver call <tool> '<json>'` accepts schema-validated arguments; JSON can also come through stdin to avoid shell quoting. Query the chosen window by actual PID/window ID, then use a current element token when possible. Save captures with `--screenshot-out-file` on supported calls. Do not paste example PIDs or coordinates into a real session. [CLI reference](https://cua.ai/docs/cua-driver/reference/cli), [tool schemas](https://cua.ai/docs/cua-driver/reference/mcp-tools).

When an operation exposes `delivery_mode`, request `background` explicitly. Verify the effect in app state and check for structured refusal or a no-op. Do not assume successful input delivery means the target acted. Reinspect after each change; stale element tokens can address the wrong state. Don't call activation/bring-to-front or desktop-scoped hotkeys as a workaround for a background refusal.

## Platform limits

| Platform | Select and verify |
| --- | --- |
| Windows | UI Automation and supported targeted input; elevation and some app input paths can refuse background delivery. |
| macOS | Accessibility actions and supported window-targeted input; permissions and some minimized/off-Space controls limit coverage. |
| Linux X11 | AT-SPI or supported target-addressed actions; toolkit acceptance differs. |
| Linux Wayland | Semantic accessibility where available; ordinary raw input to unfocused windows generally cannot be targeted. Compositor support differs. |
| Hyprland/Omarchy | Experimental CUA coverage, with narrowly qualified optional isolated seats. Don't inherit Sway support or assume Chromium/Electron raw input works. |

Check the current [CUA support matrix](https://cua.ai/docs/cua-driver/concepts/platform-support) and tool-specific schemas. Avoid changing the user's compositor, desktop permissions, or global shortcuts merely to make a test pass.

## Isolate interactions that need foreground input

Run the app in an available CUA sandbox/Space, VM, dedicated desktop session, or remote test machine. Foreground actions inside an isolated guest can exercise menus, dialogs, drag/drop, and keys without moving the host user's focus. Confirm the input and capture endpoint belongs to that guest. Do not auto-open a viewer, teleport personal authenticated apps, or synchronize the host clipboard.

Select an OS/build appropriate to the app and available host virtualization. Do not assume each CUA runtime provisions every OS. Use existing local capacity before paid cloud resources. Reuse approved setup; missing permissions or unsupported delivery are reported prerequisites. If host noninterference cannot be guaranteed, continue other checks and mark this interaction blocked rather than quietly escalating to foreground input.

Use one input sequence at a time per input/focus domain unless the driver proves independent routing. Two windows or cursors on one seat are not automatically independent workers. Separate guests can run concurrently within resource limits. Track owned processes/guests, collect results, and release only those resources. Record app/OS/build, display backend, driver version, delivery mode, and whether host focus/pointer stayed unchanged. An isolated guest pass doesn't establish the user's host-specific compositor behavior.
