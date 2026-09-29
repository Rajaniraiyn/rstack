# R Stack

<!-- skills.sh badge, shown once the repo is listed with install counts:
[![skills.sh](https://skills.sh/b/Rajaniraiyn/rstack)](https://skills.sh/Rajaniraiyn/rstack)
-->

Opinionated skills and workflows by Rajaniraiyn, published for anyone using coding agents.

Reusable skills for Claude Code, Codex, Cursor, GitHub Copilot, Amp, OpenCode, and Crush. The workflows share one canonical copy; host-specific settings are added only when a skill needs them.

## Skills

- [stop-slop](plugins/rstack/skills/stop-slop/SKILL.md): cut AI tells from anything you write or say.
- [clean-slop](plugins/rstack/skills/clean-slop/SKILL.md): remove AI slop from code, diffs, documents, copy, and design output.
- [factory](plugins/rstack/skills/factory/SKILL.md): route work across agent harnesses, models, and worktrees, and run them headlessly.
- [launch-video](plugins/rstack/skills/launch-video/SKILL.md): make polished launch and promo videos (landscape, vertical, square) with motion, music, and an optional voiceover.
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
