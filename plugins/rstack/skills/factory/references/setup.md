# Setup

Wire the factory once, before routing work at scale. The goal is a decided configuration: which harnesses and models the user can reach, which sources feed the factory, and any cost limits. The user owns authentication; you never log in, create tokens, or store credentials.

## Ask first

Ask the user for what the machine cannot tell you:

- Which harnesses they use or want: Claude Code, Codex, OpenCode, Amp, GitHub Copilot.
- Which models they can reach: Claude Opus or Sonnet, Fable 5.1, Haiku, GPT-6 Astra, the GPT-5.x family, or other providers through their subscriptions.
- Which sources feed the factory: GitHub issues, Sentry, Jira via `acli`, Linear, or MCP servers they already wired.
- Any budget or effort preferences: a per-task or per-session dollar cap, and when to escalate to a frontier model.

Only ask for decisions that change behavior. Do not ask a dozen setup questions when probing answers most of them.

## Probe

Check what is actually installed and configured rather than assuming. Plain `--version` probes are read-only and safe to run:

```sh
claude --version
codex --version
opencode --version
amp --version
copilot --version
gh --version
sentry-cli --version
acli --version
```

Or run the portable helper, which probes all of these and prints versions:

```sh
python3 scripts/factory-setup.py        # read-only report
python3 scripts/factory-setup.py --write  # save the report to user config
```

It writes `~/.config/rstack/factory.json` (or the platform equivalent), never touches auth state, and works on macOS, Linux, and Windows.

## Verify harness documentation

Flags and model names change fast. Before relying on a harness flag in this skill, confirm it against the harness's own docs or `--help`, and note the version you verified. See [harnesses.md](harnesses.md) for the per-harness invocation tables, each with a checked date.

## Decide and record

From the answers and probes, settle:

- The routing defaults: cheap tier model and effort, workhorse tier, and when to escalate to frontier. See [routing.md](routing.md).
- The source list the factory watches. See [sources.md](sources.md).
- Whether to provision worktrees per task and which cache-sharing strategy fits the package manager in play. See [worktrees.md](worktrees.md).

Record the decisions where the agent can read them next time: the user config written by the setup script, plus a short `FACTORY.md` in the repo when the user wants it versioned.

## No-auth rule

Never run login or auth commands on the user's behalf: no `gh auth login`, no `claude /login`, no writing tokens into env files, no creating API keys. If a harness is installed but not authenticated, report that it needs the user's login and move on. Users bring their own subscriptions; the factory only routes to what is already reachable.

## Hand off

Report what was detected, what was missing, and the decisions in place. Offer the install commands for missing harnesses, and ask before installing anything that costs money.