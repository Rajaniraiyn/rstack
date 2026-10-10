# Harnesses

Capture `<cli> --version`, the relevant subcommand's `--help`, and the selected model before composing a worker command. Verify the entry points below against the installed version.

| Harness | Headless entry point | Official reference |
| --- | --- | --- |
| Claude Code | `claude -p` | [CLI reference](https://code.claude.com/docs/en/cli-reference), [permissions](https://code.claude.com/docs/en/permissions) |
| Codex | `codex exec` | [CLI reference](https://developers.openai.com/codex/cli/reference), [security](https://developers.openai.com/codex/security) |
| OpenCode | `opencode run` | [CLI](https://opencode.ai/docs/cli/), [v2 docs](https://opencode.ai/v2/docs) |
| Amp | `amp --execute` | [Amp manual](https://ampcode.com/manual) |
| GitHub Copilot | `copilot -p` | [Copilot CLI documentation](https://docs.github.com/en/copilot/how-tos/copilot-cli) |

Check support for the selected model, reasoning setting, noninteractive permissions, sandbox, working directory, structured output, final-result file, resume/fork, and cost limits. Omit unsupported options. A capability supported by one client is not a flag another client inherits.

Construct arguments as a list when using a process API. Prefer a prompt file or stdin when supported. If a shell is necessary, quote for that shell; neither JSON escaping nor interpolating arbitrary issue text makes a safe command.

## Permissions and isolation

Approval mode, tool allowlists, and sandbox restrictions are separate controls. Retain the user's configured restrictions. Noninteractive execution should stop and report an approval requirement when it cannot proceed within them. A disposable worktree shares host access and credentials; it does not justify a bypass flag.

For review, enforce read-only access with the harness's supported sandbox or tool restrictions. A prompt saying "read-only" alone is not an execution boundary. If no enforceable mode exists, disclose that limitation before relying on the run as an isolated reviewer.

## Skill access and sessions

Use the target host's documented skill discovery paths or an installed plugin. Verify the worker can read the requested skill and its bundled references. If passing skill content directly, preserve resource paths and give access to only the necessary files.

Capture the worker's session ID explicitly. Resume continues that session; fork creates another session where supported. Avoid `--last` when several workers run concurrently, because it may select another task's session. Confirm fork and resume syntax with installed help before using it.
