---
name: factory
description: "Orchestrate a software factory: intake work from GitHub, Sentry, Jira, or Linear, route each task to the best harness and model for its effort level, run agents headlessly in cheap shared-cache worktrees, review results, and hand back the final link. Use when the user wants to route work across Claude Code, Codex, OpenCode, Amp, or Copilot, spawn parallel agents, pick cheaper models or effort levels, or run factory setup to probe and configure CLIs."
license: MIT
compatibility: Requires git and at least one installed agent CLI (Claude Code, Codex, OpenCode, Amp, or GitHub Copilot) reachable with a --version flag.
metadata:
  trigger: factory, factory setup, route work, spawn agents, run agents, cheaper model, effort level, worktree, parallel agents, farm out issues
---

# Factory

Run a software factory: intake work, route each task to the best harness and model for its effort level, provision cheap isolated worktrees, run agents headlessly, review the results, and hand back a final link.

## Setup first

Before routing work at scale, run the setup workflow. Ask the user which CLIs and models they have access to. They bring their own subscriptions and auth; you only detect, configure, and route. Probe what is installed, check each harness's current documentation, and record the configuration. See [references/setup.md](references/setup.md) for the exact questions, probes, and the no-auth rule.

Invoke setup as `factory setup`, `factory-setup`, or `/factory setup`. You can also run [scripts/factory-setup.py](scripts/factory-setup.py) to probe the machine and write a config file. The script never logs in and never stores credentials.

## Intake

Collect work from the sources the user points at, or the ones configured: GitHub issues with `gh`, Sentry with `sentry-cli`, Jira, Linear, or any MCP server the user has wired. When the user pastes a link, fetch it with the matching CLI or MCP instead of guessing. Classify each item by type, priority, and rough size before routing. See [references/sources.md](references/sources.md).

## Route

For each task, pick a harness, a model, and an effort level. Rules of thumb:

- Mechanical work (renames, small refactors, boilerplate): cheapest workhorse model, low effort.
- Normal implementation: workhorse model, medium effort.
- Hard architecture, debugging, or long-horizon work: frontier model, high effort.
- Escalate to a frontier model (Fable 5.1, GPT-6 Astra, Opus 5) only when the workhorse tried and failed, or the task is known-hard.

Match the harness to the machine: Claude Code for Claude models and rich tooling, Codex for OpenAI models, OpenCode for provider freedom or shareable sessions, Amp or Copilot when the user prefers them. See [references/routing.md](references/routing.md) for tiers, prices, and effort tables.

## Provision

Give each agent its own git worktree so agents run in parallel without merge conflicts. Reuse install and build caches between worktrees: symlinks or junctions for `node_modules` when lockfiles match, pnpm's global store, uv's shared cache, the cargo registry cache. Keep worktrees disposable and recycle them. See [references/worktrees.md](references/worktrees.md).

## Run

Invoke each harness headlessly from inside your own session, and collect results back. Claude Code: `claude -p`, Codex: `codex exec`, OpenCode: `opencode run`, Amp: `amp --execute`, Copilot: `copilot -p`. Pass the model, effort, thinking, and budget flags that harness understands. See [references/harnesses.md](references/harnesses.md) for the per-harness tables.

The factory needs no separate runner: the harness you are already in is a running agent, so re-invoke its own binary headlessly instead of installing an orchestrator.

Choose how a task reaches its worker before spawning: the host's built-in sub-agent tool for small in-session sub-tasks, a headless spawn for isolated work that needs full flag control, a session fork to retry or escalate with inherited context, or a fresh session when the old context is noise. See [references/subagents.md](references/subagents.md) for the routes and which CLI can fork.

## Review

Before handing work back, run a review gate with a different harness or model than the one that wrote the work, read-only. Fix what the review finds, then re-run the gate. See [references/reviews.md](references/reviews.md).

## Hand back

Report the final URL: the pull request, a share link (`opencode run --share` or a session share), or the review report. Summarize in one short paragraph what shipped and on which branch or worktree.

## Guardrails

- Never authenticate for the user. Setup detects and configures only. The user manages subscriptions, tokens, and logins.
- Route only to harnesses that are installed and configured. Offer to install what is missing, but ask before installing anything that costs money.
- Default to the cheapest workable routing. Escalate deliberately, and say when you did and why.
- Prefer the built-in sub-agent tool for small in-session sub-tasks. Spawn or fork only when isolation, model freedom, budget control, or inherited context justifies a full session.
- Share caches, never active state. Two agents writing the same build directory corrupt each other's work.
- Helpers and examples in this skill are portable: stdlib-only Python and plain markdown, never shell that requires bash. Windows may not have bash.
- Before handing back generated code or prose, run the `clean-slop` skill on the artifacts. It owns the edit pass for produced work.

## Reference files

- [references/setup.md](references/setup.md)
- [references/harnesses.md](references/harnesses.md)
- [references/subagents.md](references/subagents.md)
- [references/routing.md](references/routing.md)
- [references/worktrees.md](references/worktrees.md)
- [references/sources.md](references/sources.md)
- [references/reviews.md](references/reviews.md)