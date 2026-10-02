# TUIs and terminals

Use a real PTY for interactive prompts, full-screen apps, REPLs, and key handling. A text stream with ANSI removed loses cursor movement, redraws, and the alternate screen. Assert the rendered state after input, and inspect raw output when diagnosing escape sequences.

## Tool choices

- [tuistory](https://github.com/remorses/tuistory) provides named sessions, screen snapshots, reactive waits, input, resize, and a JS/TS `launchTerminal` API. Read installed help first. Use an explicit unique session and geometry; options precede `--`. Its daemon may restart on upgrade, so keep one version while sessions are active.
- [terminal-control](https://github.com/anomalyco/terminal-control) provides Ghostty-based capture, persistent sessions, and a typed TS client. One-off `show`/`save` terminate the launched process tree afterward; use `start` for a lasting app. Semantic snapshots need a cooperating provider and can be empty. Check the current macOS/Linux runtime support.
- [Pexpect](https://pexpect.readthedocs.io/en/stable/) fits prompt/response testing on supported PTYs. `tmux` can drive an existing project workflow; target a specific owned pane and wait on observable state. For a programmable multipane session route, inspect [shux](https://github.com/indrasvat/shux) if the existing drivers lack that capability. Tool names do not establish platform support.
- Framework render-test utilities can test widgets deterministically. Keep a PTY check for actual input, startup, terminal restoration, and process behavior.

Example with an installed tuistory, replacing `my-tui` and `Ready` with the app's actual contract:

```sh
tuistory --help
tuistory -s test-owned-example --cols 100 --rows 30 -- my-tui
tuistory -s test-owned-example wait "Ready" --timeout 10000
tuistory -s test-owned-example snapshot --trim
tuistory -s test-owned-example press tab
tuistory -s test-owned-example snapshot --trim
tuistory -s test-owned-example resize 60 20
tuistory -s test-owned-example snapshot --trim
tuistory -s test-owned-example close
```

For durable tests, assert expected state and side effects with the API or project runner. Idle output alone is not successful completion. Do not attach an interactive human session in an agent tool call, close other sessions, or stop a shared daemon for cleanup.

## Terminal-specific checks

Test narrow and normal geometry, resize while a dialog is open, scrolling, selection, focus, keyboard-only navigation, escape/back, and clean exit. Verify state after each action. Avoid whole-screen snapshots dominated by timestamps or spinners; normalize only fields irrelevant to the assertion.

Distinguish typed text, pasted text, and key chords. Bracketed paste, escape/Alt ambiguity, Ctrl keys, modified arrows, kitty keyboard protocol, mouse reporting, and terminal-owned shortcuts depend on emulator support. Test advertised protocols in a compatible terminal. Exercise IME, combining characters, emoji/CJK cell width, and multiline paste when the app accepts them.

Record terminal emulator, `TERM`, locale, color depth, font, and geometry for rendering bugs. Check dark/light contrast, no-color mode, and plain/limited terminals if supported. PTY emulation does not prove pixel appearance, screen-reader behavior, clipboard integration, or every emulator's protocol. Add the relevant real-terminal check.

Validate Ctrl+C and graceful quit, subprocess interruption, raw/cooked-mode restoration, cursor visibility, alternate-screen exit, and cleanup after a crash. On Windows, test the actual console/ConPTY path; a Unix PTY or WSL pass is insufficient.
