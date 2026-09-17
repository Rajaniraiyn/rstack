# Sub-agents, forking, and fresh work

One harness can run many brains. Work reaches a second agent through four routes, and each route trades context, isolation, and control differently. Pick the route before you spawn, and say which one you picked.

## The four routes

### 1. Built-in sub-agent tool (in-session)

The host harness delegates to a sub-agent with its own tool: Claude Code subagents, Codex `spawn_agent`, OpenCode subagents, Amp's Task tool, Copilot's delegated or custom agents. The sub-agent runs inside the parent session, shares the parent's project, tools, and auth, gets one scoped task, and returns a summary.

Use for a sub-task that is part of the current session's work: it needs the same project context, you want the result back in the conversation, and the host already has the auth and tools it requires. Per-harness agent definitions pick the sub-agent's model, effort, and tools where supported; some harnesses let a sub-agent inherit the parent conversation (Claude Code fork-type subagents, newer Codex hydration), others always start cold. The knobs rotate; confirm against the harness docs.

Do not use the built-in tool when the work needs its own worktree, a different harness or model family than the host can reach, a hard budget cap the host does not offer, or a result delivered as a file for the review gate.

### 2. Manual headless spawn (factory worker)

Running a full harness binary as a child process: `claude -p`, `codex exec`, `opencode run`, `amp --execute`, `copilot -p`. The worker is a separate process with its own session ID, its own flags, and full control: model, effort, thinking, budget, sandbox, output format, worktree.

Use for work that deserves its own session: multi-file changes, a dedicated worktree, a different model or harness than the host, or a result the review gate will read from a file. This is the factory's truck: route, provision a worktree, spawn, collect the result.

### 3. Fork a session

Forking copies a previous session and its full context into a new session with its own ID, then runs it under new parameters: different model, effort, budget, or agent. The original session stays untouched. Fork to retry, escalate, or A/B a strategy against context that already exists, instead of rebuilding it by hand.

Use when a worker's result is wrong or stuck and you want to retry at a higher tier without losing what it already learned, when you want to A/B two approaches against the same investigation, or when you want a branch of a long session that stays out of the main context.

Which CLI can fork (checked 17 September 2026; confirm with `<cli> --help`):

- **Claude Code**: `claude --continue --fork-session` or `claude --resume <session-id> --fork-session`. In-session `/branch <name>` copies the conversation; `/fork` runs a background agent with your entire context and returns the result to you. `claude --list-sessions` prints session IDs.
- **Codex**: `codex fork` opens a picker and `codex fork --last` forks the latest interactive session into a new thread. Headlessly, `codex exec fork <session-id> [prompt]` forks into a new session with an optional follow-up prompt. `codex exec resume <session-id>` and `codex exec resume --last` continue an exec session (resume, not fork).
- **OpenCode**: `opencode run -c --fork` or `opencode run -s <session-id> --fork` forks the session into a new one. `-c` and `-s` without `--fork` continue in place.
- **Amp**: the Fork command was removed in January 2026. Threads are durable: reopen a thread by its threadID and continue it, or start a new thread when you want a branch.
- **Copilot CLI**: `copilot --resume` and `copilot --continue` reopen sessions, `/fork` branches a session with an optional name, and a session can rewind to a previous prompt. Branch by forking or by starting a new session and carrying over the context you need.

### 4. Fresh session

A new session with cold context and no session ID. Use when the prior context is noise (compaction summaries, tangents), the task changed domain or repository, or you intentionally want the agent to rediscover the project from the current state.

## Which route, when

1. Task inside the current session's project, small, result wanted in conversation: built-in sub-agent.
2. Task needs isolation, its own worktree, or full flag control: headless spawn.
3. Retry or escalate a prior worker with its context intact: fork its session, where supported.
4. New domain, noisy context, or changed repo: fresh session in a new worktree.

The trade per route:

| Route | Context | Isolation | Control | Cost |
| --- | --- | --- | --- | --- |
| Built-in sub-agent | fresh or inherited | same session | agent definition only | one session, low overhead |
| Headless spawn | fresh | own process and worktree | full flags | one full session |
| Fork | inherited from the parent | own session ID, same lineage | new flags | reuses context, spends new session |
| Fresh | none | owns its session | full flags | rebuilds context from scratch |

## The factory runs on the harness you are already in

The factory skill loads inside whichever harness the user already has open: Claude Code, OpenCode, Codex, Amp, or Copilot. That host is a running agent that can re-invoke its own binary headlessly, so the factory needs no separate runner or orchestrator process. If the user is in OpenCode, spawn workers with `opencode run`; in Claude Code, with `claude -p`. The factory is the router, not another agent to install.

## Workers can delegate

Every spawned worker is a full agent with its own built-in sub-agent tool. A Claude Code worker can spawn Claude Code subagents; a Codex worker can spawn Codex subagents. Keep delegation one or two levels deep; beyond that, context and cost explode. If a worker needs a different harness, harvest its result and route the next step yourself rather than nesting a second binary inside the worker.

## Verify before you script

Fork, resume, and sub-agent flags rotate faster than the base headless flags. Confirm each command with `<cli> --help` and record the version you verified, as with [harnesses.md](harnesses.md).