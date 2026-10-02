# CLIs and process contracts

A CLI exposes arguments, input, streams, exit status, and side effects. A TUI also exposes a changing screen and interactive state. A command can have both modes; test pipes without a PTY and interactive behavior with one. Use [tui.md](tui.md) for the latter.

Launch through the project's normal entrypoint with explicit arguments, cwd, fixtures, and environment. Prefer an argument array to a shell string unless shell behavior itself is under test. Capture stdout and stderr separately, bound execution time, and close stdin when input is complete. Drain both streams while waiting so a full pipe cannot deadlock the test. [Python subprocess documentation](https://docs.python.org/3/library/subprocess.html).

Choose meaningful cases:

- Help/version and invalid arguments; exit status, diagnostics, and machine-readable output. Parse JSON as JSON. Successful exit alone does not prove correct output. Prefer assertions on contract fields to snapshots of all help text or incidental whitespace.
- Empty input, EOF, malformed input, large input, piped input, redirected output, and early downstream close. Check whether prompts or color escape into noninteractive output. Respect the project's color and no-prompt contract.
- Filenames with spaces, Unicode, leading dashes, and paths outside cwd. Use temporary config/cache/data roots through app-supported settings. Avoid replacing system `HOME` just to simplify a command.
- Dry-run behavior, overwrite/conflict handling, partial writes, atomicity, and rerun behavior. Assert files or API effects, not only progress messages.
- Timeout, cancellation, signal handling, child cleanup, and useful failure diagnostics. Distinguish a timeout imposed by the test from an app-generated timeout or exit status. Kill only processes this test owns. Test whether interruption leaves terminal state or data damaged.

## Platform and shell differences

Windows process quoting, PowerShell parsing, POSIX shells, and direct process execution are different interfaces. Shell examples must name their shell. Test scripts under the shells the project promises to support. File case sensitivity, executable bits, separators, CRLF, locale, and encoding can change behavior.

POSIX signals are not Windows console events. PTYs can combine streams, alter buffering, and enable prompts or color, so PTY output cannot prove the noninteractive stream contract. A Windows ConPTY path needs its own check; WSL tests establish Linux behavior. For command dispatch and job control, verify the actual process tree rather than assuming a shell wrapper forwards signals.

Test the installed artifact outside the source tree when packaging, completions, entrypoints, or bundled assets change. For Go, Rust, Python, or Node CLIs, reuse their existing process-test libraries. Add an external driver only when the standard runner cannot exercise the required boundary.
