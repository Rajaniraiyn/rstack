# R Stack

<!-- skills.sh badge, shown once the repo is listed with install counts:
[![skills.sh](https://skills.sh/b/Rajaniraiyn/rstack)](https://skills.sh/Rajaniraiyn/rstack)
-->

My personal skills and workflows for coding agents.

Portable `SKILL.md` files that work with Claude Code, Codex, Cursor, GitHub Copilot, Amp, OpenCode, and Crush. One copy of each skill lives in `plugins/rstack/skills/`.

## Skills

- [stop-slop](plugins/rstack/skills/stop-slop/SKILL.md): cut AI tells from anything you write or say.
- [clean-slop](plugins/rstack/skills/clean-slop/SKILL.md): remove AI slop from code, diffs, documents, copy, and design output.
- [rstack-author-skill](plugins/rstack/skills/rstack-author-skill/SKILL.md): create or revise a portable skill for this repository.

## Install

Use the [installation guide](docs/installation.md) for each agent's native commands, or the shared fallback:

```sh
npx skills add Rajaniraiyn/rstack
```

Add `--global` to install across projects.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) to add a skill or change the tooling.

## License

MIT. See [LICENSE](LICENSE).