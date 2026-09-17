# Harnesses

Checked 17 September 2026 against installed CLIs (claude 2.1.270, codex-cli 0.154.0, opencode v2.0.5) plus current vendor docs for Copilot CLI and Atlassian acli. These CLIs ship updates constantly; confirm flags with `<cli> --help` before scripting them, and record the version you checked.

## Claude Code

For unattended work, prefer `--permission-mode auto` where available: Claude Code reviews actions with a classifier instead of prompting. This differs from `bypassPermissions`, which skips permission checks, and from sandboxing, which limits filesystem and network access. Auto mode is not a sandbox and not a guarantee of safety; keep the user's approved scope and managed restrictions in force. Use bypass modes only where the user approved them, and only in a disposable worktree, container, or VM with no sensitive access.

Headless (print mode):

```sh
claude -p "task" --output-format json --max-budget-usd 5
claude -p "task" --model sonnet --effort medium --allowedTools "Bash(git status),Read,Edit"
```

Knobs:

- `--model`: model alias or id (for example `fable`, `opus`, `sonnet`, `haiku`).
- `--effort`: `low`, `medium`, `high`, `xhigh`, `max` (or `ultracode` on newer versions with supported models).
- `--max-budget-usd`: cap spend in print mode.
- `--append-system-prompt`: add context without touching the session's prompt.
- `--allowedTools`, `--disallowedTools`, and `--permission-mode`: control what headless runs can touch. Modes include `manual`, `acceptEdits`, `plan`, `auto`, `dontAsk`, and `bypassPermissions`.
- `--dangerously-skip-permissions`: bypass all permission checks. Only where the user approved it and the environment is disposable.
- `--output-format text|json|stream-json`: structured results for downstream parsing.
- `--add-dir`: load a directory of skills explicitly.
- `--worktree`: start in a managed git worktree.
- `--bg`: run as a background agent; `claude agents` lists sessions, `attach`, `logs`, `stop`, and `rm` manage them.
- `MAX_THINKING_TOKENS`: set the thinking budget. Some models can disable thinking; always-on thinking models (Fable) cannot.

Skills: `.claude/skills/`, `~/.claude/skills/`, or plugin marketplaces; `--add-dir` loads a skills directory even in bare mode.

## Codex

Headless:

```sh
codex exec "task" --sandbox workspace-write --ask-for-approval on-request --json
codex exec "task" --model gpt-5.5 -o result.txt
```

Knobs:

- `--sandbox`: `read-only`, `workspace-write`, `danger-full-access`.
- `--ask-for-approval`: `on-request`, `never`.
- `--approve-for-me`: route approval requests through automatic review under the workspace-write sandbox.
- `--dangerously-bypass-approvals-and-sandbox`: skip all confirmation prompts and sandboxing. Only where the user approved it and the environment is externally sandboxed.
- `--model` or `-m`: override the configured model.
- `--json`: JSON Lines event stream on stdout, for pipelines.
- `-o FILE` / `--output-last-message FILE`: write the final response to a file.
- `--output-schema`: enforce a JSON schema on the result (check model support).
- `--profile` / `-p`: layer a named config file on top of the base user config; profiles bundle model, sandbox, and approval.
- `codex exec resume --last` or `codex exec resume <session-id>`: continue a previous exec session.
- `codex exec fork <session-id> [prompt]`: fork a previous session into a new one, headlessly, with an optional follow-up prompt.
- `--worktree`: run the session in a new managed git worktree.
- `--ephemeral`: skip persisting session files, for stateless parallel jobs.

Note: `--full-auto` was removed. Use an explicit sandbox plus approval mode instead of the old alias.

Skills: `~/.codex/skills/` with `SKILL.md`, invoked by name with `$skill-name` or auto-activated from the description. `AGENTS.md` holds always-on repo instructions; skills load on demand.

## OpenCode

Headless:

```sh
opencode run "task" -m anthropic/claude-opus-4-6 --format json
opencode run "task" -m openai/gpt-5.5#high --format json
```

Knobs (from `opencode run --help`):

- `-m provider/model#variant`: pick the model and reasoning variant per invocation.
- `--format json`: raw event objects for parsing.
- `--auto`: auto-approve permissions that are not explicitly denied.
- `--continue` / `-c` and `--session` / `-s`: continue prior sessions; add `--fork` to keep the original.
- `--agent`: run a configured agent.
- `--file` / `-f`: attach files to the message.
- `--title`: name the session.
- `--thinking`: show thinking blocks.

Check `opencode --help` for server, share, and agent-management commands; they move between releases, so confirm before scripting them.

Skills: hosted in the agent's skill directories; install with `npx skills add` or by adding a skills directory to the agent config.

## Amp

Headless:

```sh
amp --execute "task" --stream-json
amp --execute "task" --stream-json-thinking
```

Knobs:

- `--execute`: non-interactive mode (the headless entry point).
- `--stream-json` and `--stream-json-thinking`: structured output, with or without thinking blocks.
- `--no-tui`: headless runner that waits for remotely created threads.
- Settings file (`~/.config/amp/settings.json`): MCP servers, command allowlist, multi-model routing.

Amp is multi-model (for example GPT and Claude families) and routes internally; pick the model through its settings or thread configuration. Amp was not installed on the check machine, so confirm its flags against its own docs and `--help` before scripting.

## GitHub Copilot CLI

Headless:

```sh
copilot -p "task" --model gpt-5.5
copilot -p "review this diff" --agent code-review
```

Knobs (from vendor docs; Copilot CLI was not installed on the check machine, so confirm with `--help`):

- `-p` / `--prompt`: one-shot execution.
- `--mode`: `interactive`, `plan`, `autopilot`; autopilot works a trusted task end to end without stopping for approval.
- `--allow-all` (with `--allow-all-tools`, `--allow-all-paths`, `--allow-all-urls`) and `--yolo`: skip approval gates. These widen what the agent may touch, so use them only where the user approved them and the scope is safe.
- `--model`: pin the model.
- `--agent`: run a specialized agent profile (for example a code-review agent).
- `--resume` / `--continue`: reopen a saved session with its context; `/fork` branches a session with an optional name.
- `--sandbox` / `--no-sandbox`: sandbox control, separate from approval flags.
- `--share`: write or publish the session transcript; `--session-id` pins the session.
- `--worktree`: run in a managed worktree.
- `/mcp` and `/plugin`: manage MCP servers and plugins inside a session.
- Instructions come from `AGENTS.md`, `.github/copilot-instructions.md`, or `.instructions/`.

## Approval, bypass, and sandbox

These are three separate controls. Do not treat them as one switch.

- Auto-approve keeps checks in place and approves the safe ones: Claude Code `--permission-mode auto` (classifier), Codex `--approve-for-me` (automatic review under workspace-write sandbox), OpenCode `run --auto` (approves what is not denied), Copilot `--mode autopilot` (works without stopping for approval). Prefer these for unattended runs.
- Bypass skips the prompts: Claude Code `--dangerously-skip-permissions`, Codex `--dangerously-bypass-approvals-and-sandbox`, Copilot `--allow-all` / `--yolo`. Use only where the user approved it, only in a disposable worktree, container, or VM, and never as the default.
- Sandbox limits what processes can touch even when approved: Codex `--sandbox`, Copilot `--sandbox`, Claude Code sandboxing. Keep a sandbox on for any run that edits files or runs commands in a shared checkout.

A bypass flag is not evidence the agent is trustworthy. It is evidence the blast radius must be small. Scope the run, keep the sandbox, and say which mode you used when you report cost and results.

## Skills access across harnesses

A skill bundle installed once (for example `npx skills add Rajaniraiyn/rstack`) lands in each agent's skill directory where supported:

- Claude Code: `.claude/skills` or `--add-dir <dir>`.
- Codex: `~/.codex/skills`.
- OpenCode: its configured skills directory.
- Copilot and Amp: follow their skill or toolbox conventions.

When a harness cannot see a skill the user wants, pass the SKILL.md content into the prompt directly (`--append-system-prompt "$(cat SKILL.md)"` in Claude Code, or read the file into the task text) as an ephemeral fallback. Prefer that over giving the harness filesystem paths it cannot reach.

## Sessions, forks, and sub-agents

Every harness here also has session and delegation mechanics: built-in sub-agent tools, session resume, and in some cases session forking (`claude --fork-session`, `codex fork --last` or `codex exec fork`, `opencode run --fork`, Copilot `/fork` or `--resume` with rewind). Amp removed its Fork command and uses durable, resumable threads instead. The strategic choice between the built-in sub-agent tool, a headless spawn, a fork, and a fresh session is in [subagents.md](subagents.md).