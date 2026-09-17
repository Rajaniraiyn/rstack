# R Stack

My personal skills and workflows for coding agents.

Portable `SKILL.md` files that work with Claude Code, Codex, Cursor, GitHub Copilot, Amp, OpenCode, and Crush. One copy of each skill lives in `plugins/rstack/skills/`.

## Install

Use the [installation guide](docs/installation.md) for each agent's native commands, or the shared fallback:

```sh
npx skills add ./plugins/rstack
```

From GitHub: `npx skills add Rajaniraiyn/rstack`. Add `--global` to install across projects.

## Layout

- `plugins/rstack/skills/` - the skills and their bundled resources
- `plugins/rstack/plugin.json` - name, version, author, repository
- `scripts/rstack.py` - syncs client metadata, validates, exports ZIPs
- Generated metadata in `.claude-plugin/`, `.cursor-plugin/`, `.agents/`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) to add a skill or change the tooling.