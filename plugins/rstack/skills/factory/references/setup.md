# Setup

Configure available harnesses, models, issue sources, and cost limits before dispatching workers. Leave authentication to the user.

## Inspect before asking

Ask the user for what the machine cannot tell you:

- Which harnesses they use or want: Claude Code, Codex, OpenCode, Amp, GitHub Copilot.
- Which current routes they can reach: check the shortlist in [routing.md](routing.md) against the installed providers and subscriptions. Preserve an explicitly selected model; refresh old saved defaults only when the user requested migration.
- Which sources feed the factory: GitHub issues, Sentry, Jira via `acli`, Linear, or MCP servers they already wired.
- Any budget or effort preferences: a per-task or per-session dollar cap, and when to escalate to a frontier model.

Probe available capabilities and ask only for missing decisions.

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

Or run the portable helper, which probes all of these and prints versions. Resolve its path from the installed skill directory, not the project's working directory:

```sh
python3 scripts/factory-setup.py        # read-only report
python3 scripts/factory-setup.py --write  # save the report to user config
```

It updates the detected harness records in `~/.config/rstack/factory.json` (or the platform equivalent), never touches auth state, and works on macOS, Linux, and Windows.

## Verify harness documentation

Flags and model names change fast. Before relying on a harness flag in this skill, confirm it against the harness's own docs or `--help`, and note the version you verified. See [harnesses.md](harnesses.md) for the headless entry points and authoritative documentation.

## Decide and record

From the answers and probes, settle:

- The routing defaults: cheap tier model and effort, workhorse tier, and when to escalate to frontier. See [routing.md](routing.md).
- The source list the factory watches. See [sources.md](sources.md).
- Whether to provision worktrees per task and which cache-sharing strategy fits the package manager in play. See [worktrees.md](worktrees.md).

Record the decisions where the agent can read them next time: the user config written by the setup script, plus a short `FACTORY.md` in the repo when the user wants it versioned.

## No-auth rule

Never run login or auth commands on the user's behalf, write tokens into env files, or create API keys. If a harness is installed but not authenticated, report that it needs the user's login and move on.

## Hand off

Report what was detected, what was missing, and the decisions in place. Offer the install commands for missing harnesses, and ask before installing anything that costs money.
