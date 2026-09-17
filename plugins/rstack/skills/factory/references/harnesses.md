# Harnesses

Verified September 2026. These CLIs ship updates constantly; confirm flags with `<cli> --help` before scripting them, and record the version you checked.

## Claude Code

For unattended work, prefer `--permission-mode auto` where available: Claude Code uses a classifier to review actions. This differs from `bypassPermissions`, which skips permission checks, and from sandboxing, which limits filesystem and network access. Auto mode is not a sandbox or a guarantee of safety; keep the user's approved scope and managed restrictions in force.

Headless (print mode):

```sh
claude -p "task" --output-format json --max-budget-usd 5
claude -p "task" --model sonnet --effort medium --allowedTools "Bash(git status),Read,Edit"
```

Knobs:

- `--model`: model id (for example `opus`, `sonnet`, `haiku`).
- `--effort`: `low`, `medium`, `high`, `xhigh`, `max` (or `ultracode` on newer versions with supported models).
- `--max-budget-usd` and `--max-turns`: cap spend and turns in print mode.
- `--append-system-prompt`: add context without touching the session's prompt.
- `--allowedTools` and `--permission-mode`: control what headless runs can touch.
- `--output-format text|json|stream-json`: structured results for downstream parsing.
- `--add-dir`: load a directory of skills explicitly.
- `--worktree`: start in an isolated git worktree.
- `--bg --exec`: run as a background agent.
- `MAX_THINKING_TOKENS`: set the thinking budget. Some models can disable thinking; frontier models (Fable) cannot.

Skills: `.claude/skills/`, `~/.claude/skills/`, or plugin marketplaces; `--add-dir` loads a skills directory even in bare mode.

## Codex

Headless:

```sh
codex exec "task" --sandbox workspace-write --ask-for-approval on-request --json
codex exec "task" --model gpt-5.5 -o result.txt
```

Knobs:

- `--sandbox`: `read-only`, `workspace-write`, `danger-full-access`.
- `--ask-for-approval`: `untrusted`, `on-request`, `never`.
- `--model` or `-m`: override the configured model.
- `--json`: JSON Lines event stream on stdout, for pipelines.
- `-o FILE`: write the final response to a file.
- `--output-schema`: enforce a JSON schema on the result (check model support).
- `--profile` / `-p`: load a named config profile; `config.toml` supports profiles that bundle model, sandbox, and approval.
- `codex exec resume --last`: continue the previous session.
- `--ephemeral`: skip persisting session files, for stateless parallel jobs.

Note: `--full-auto` was removed. Use an explicit sandbox plus approval mode instead of the old alias.

Skills: `~/.codex/skills/` with `SKILL.md`, invoked by name with `$skill-name` or auto-activated from the description. `AGENTS.md` holds always-on repo instructions; skills load on demand.

## OpenCode

Headless:

```sh
opencode run "task" -m anthropic/claude-sonnet-4-6 --format json
opencode run "task" -m openai/gpt-5.5 --variant high --share
```

Knobs:

- `-m provider/model`: pick the model per invocation.
- `--variant`: provider-specific reasoning effort (`minimal`, `high`, `max`).
- `--format json`: raw event objects for parsing.
- `--share`: publish the session and get a share link.
- `--continue` / `-c` and `--session` / `-s`: continue prior sessions; `--fork` keeps the original.
- `--prompt`: seed the agent with a prompt at launch.
- `opencode serve` / `opencode web`: headless HTTP server or web UI.
- `opencode agent create`: define custom agents with model and permissions; subagents are configured in the agent's frontmatter.

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

Amp is multi-model (for example GPT and Claude families) and routes internally; pick the model through its settings or thread configuration.

## GitHub Copilot CLI

Headless:

```sh
copilot -p "task" -s --no-ask-user --model gpt-5.5
copilot -p "review this diff" --agent code-review
```

Knobs:

- `-p` / `--prompt`: one-shot execution.
- `-s`: clean, script-friendly output.
- `--no-ask-user`: never block waiting for input.
- `--model`: pin the model.
- `--agent`: run a specialized agent profile (for example a code-review agent).
- `--mode`: `interactive`, `plan`, `autopilot`; `--plan --mode autopilot` plans then auto-executes.
- `/mcp` and `/plugin`: manage MCP servers and plugins inside a session.
- Instructions come from `AGENTS.md`, `.github/copilot-instructions.md`, or `.instructions/`.

## Skills access across harnesses

A skill bundle installed once (for example `npx skills add Rajaniraiyn/rstack`) lands in each agent's skill directory where supported:

- Claude Code: `.claude/skills` or `--add-dir <dir>`.
- Codex: `~/.codex/skills`.
- OpenCode: its configured skills directory.
- Copilot and Amp: follow their skill or toolbox conventions.

When a harness cannot see a skill the user wants, pass the SKILL.md content into the prompt directly (`--append-system-prompt "$(cat SKILL.md)"` in Claude Code, or read the file into the task text) as an ephemeral fallback. Prefer that over giving the harness filesystem paths it cannot reach.

## Sessions, forks, and sub-agents

Every harness here also has session and delegation mechanics: built-in sub-agent tools, session resume, and in some cases session forking (`claude --fork-session`, `codex fork --last`, `opencode run --fork`, Copilot `--resume` with rewind). Amp removed its Fork command and uses durable, resumable threads instead. The strategic choice between the built-in sub-agent tool, a headless spawn, a fork, and a fresh session is in [subagents.md](subagents.md).