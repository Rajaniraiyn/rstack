# R Stack

Rajaniraiyn's personal skills and workflows for coding agents.

One collection of portable `SKILL.md` files works across Claude Code, Codex, Cursor, GitHub Copilot, Amp, OpenCode, and Crush. R Stack keeps a single copy of each skill; the [skills CLI](https://github.com/vercel-labs/skills) handles per-client installation paths.

## Install

Start with the [installation guide](docs/installation.md) for native Claude Code, Codex, Cursor, Copilot, and Amp commands. OpenCode and Crush discover installed skill folders directly.

For a shared fallback, use Vercel's `skills` CLI from this checkout:

```sh
npx skills add ./plugins/rstack
```

It lets you choose skills and agents. From GitHub, use `npx skills add Rajaniraiyn/rstack`. Add `--global` to use the skills across projects.

## What's here

- `plugins/rstack/skills/` holds the skills and their bundled resources. The starter is `rstack-author-skill`.
- `plugins/rstack/plugin.json` is the canonical portable manifest: name, version, author, and repository.
- `scripts/rstack.py` syncs client manifests and catalogs, validates the package, and exports ZIPs.
- Generated metadata lives in `.claude-plugin/`, `.cursor-plugin/`, `.agents/`, and each plugin's client subdirectory.

MCP servers and hooks can be added when a workflow needs them.

## Develop

Requires [uv](https://docs.astral.sh/uv/):

```sh
uv sync
uv run scripts/rstack.py package
uv run python -m unittest discover -s tests
```

`package` validates before writing archives to `dist/`. After changing `plugin.json`, run `uv run scripts/rstack.py sync` to regenerate client metadata. See [authoring](docs/authoring.md) for adding skills and integrations.