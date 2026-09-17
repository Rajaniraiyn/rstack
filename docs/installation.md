# Installation

Use your agent's native method below when available. [Vercel's skills CLI](#shared-fallback-with-skillssh) is the fallback for installing the same skills across agents or from GitHub.

Commands use a local R Stack checkout. Run them from its root unless noted. Choose one method per agent to avoid duplicate skills. Native commands vary by installed version; check `<command> --help` if your CLI does not recognize one.

## Claude Code

Install the native plugin through this repository's marketplace:

```sh
claude plugin marketplace add .
claude plugin install rstack@rstack
```

For a single development session, use `claude --plugin-dir ./plugins/rstack`. The starter skill is `/rstack:rstack-author-skill`. From GitHub, add the marketplace with the repository name and install as above. See [Claude's marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces).

## Codex

Recent Codex CLIs can register and install the plugin:

```sh
codex plugin marketplace add .
codex plugin add rstack@rstack
codex plugin list
```

If `codex plugin add` is unavailable, register the marketplace and install R Stack through the app's plugin directory, or use the shared skills installer below. Start a new conversation after installation. See [OpenAI's plugin guide](https://developers.openai.com/plugins/build/plugins). The `add` syntax was also checked against the local Codex CLI help.

## Cursor

Cursor's CLI can load the local plugin for a session:

```sh
agent --plugin-dir ./plugins/rstack
```

`agent` is Cursor's CLI executable. This loads the directory; it does not permanently install a marketplace plugin. For persistent local skills, use the shared installer below. For plugin distribution, use Cursor's public or team marketplace flow with the committed `.cursor-plugin` catalog. See [CLI parameters](https://cursor.com/docs/cli/reference/parameters) and [plugin packaging](https://cursor.com/docs/reference/plugins).

## GitHub Copilot

Copilot CLI can register the skill collection as a custom source:

```sh
copilot skill add ./plugins/rstack/skills
copilot skill list
```

Directory registration keeps the collection in place, so retain the checkout. Avoid installing only `SKILL.md` because this skill also needs its bundled reference. See [Copilot's skill commands](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#managing-skills-non-interactively).

For a copied project install, GitHub CLI also provides skill installation:

```sh
gh skill install ./plugins/rstack rstack-author-skill --from-local --agent github-copilot --scope project
```

Use `--scope user` across projects. From GitHub, use `gh skill install Rajaniraiyn/rstack rstack-author-skill --agent github-copilot` without `--from-local`. This requires a GitHub CLI version with `gh skill`; see [its command reference](https://cli.github.com/manual/gh_skill_install).

For Copilot's cloud agent, commit project skills to the repository it uses. A global install on your laptop is not a cloud deployment.

## Amp

Amp has a native skill installer:

```sh
amp skill add ./plugins/rstack
amp skills list
```

Use `amp skill add ./plugins/rstack --global` for a machine-wide install. The source can also be a GitHub repository or Git URL. Existing sessions may need a skill reload. Hosted personal and workspace skill repositories have separate import and layout rules. See [Amp's skill documentation](https://ampcode.com/docs/customize/skills).

## OpenCode and Crush

Both discover standard skill directories. Their documented routes do not require a dedicated skill-install subcommand. Use the shared CLI below, or copy a complete skill into a documented project directory:

| Agent | Project directory for manual installation | Documentation |
| --- | --- | --- |
| OpenCode | `.opencode/skills/` or `.agents/skills/` | [Skill discovery](https://opencode.ai/docs/skills/) |
| Crush | `.crush/skills/` or `.agents/skills/` | [Agent skills](https://github.com/charmbracelet/crush#agent-skills) |

For example, from the target project on macOS or Linux, replacing the source path with your checkout:

```sh
mkdir -p .agents/skills
cp -R /path/to/rstack/plugins/rstack/skills/rstack-author-skill .agents/skills/
```

Keep the entire directory, including references. Global discovery paths differ; use each client's docs or the installer's `--global` option.

## Claude web and desktop

Run `uv run scripts/rstack.py package`, then upload an individual skill ZIP such as `dist/rstack-author-skill-0.1.0.zip` through [Claude's custom-skill interface](https://support.claude.com/en/articles/12512180-use-skills-in-claude). The full `rstack-0.1.0.zip` is a plugin bundle, not an individual skill upload.

An upload does not provide a local checkout, Python environment, or MCP connection. Configure those separately when the workflow needs them.

## Shared fallback with skills.sh

[Vercel's skills.sh](https://skills.sh/docs) provides the `skills` CLI. It discovers the same skill folders and installs them into each selected agent's supported location. Node.js with `npx` is required; [uv](https://docs.astral.sh/uv/) is only needed to develop or package R Stack.

From the checkout, list or choose skills and agents interactively:

```sh
npx skills add ./plugins/rstack --list
npx skills add ./plugins/rstack
```

Or select agents explicitly:

```sh
npx skills add ./plugins/rstack --agent claude-code codex cursor github-copilot amp opencode crush
```

| Client | `--agent` value |
| --- | --- |
| Claude Code | `claude-code` |
| Codex | `codex` |
| Cursor | `cursor` |
| GitHub Copilot | `github-copilot` |
| Amp | `amp` |
| OpenCode | `opencode` |
| Crush | `crush` |

Add `--global` to install across projects, `--skill rstack-author-skill` for one skill, or `--copy` to copy instead of symlink. Project installs target the current directory. To install into another project, run there and pass the absolute path to this checkout's `plugins/rstack` directory.

From GitHub, the CLI installs straight from the repository:

```sh
npx skills add Rajaniraiyn/rstack
```

You can also use the full GitHub URL or a direct URL to `plugins/rstack`.

Other installer targets include Cline, Continue, Gemini CLI, Goose, and Windsurf. Use interactive selection or the [maintained agent list](https://github.com/vercel-labs/skills#supported-agents); R Stack does not duplicate that registry.

## Compatibility and verification

All seven named clients accept the shared [Agent Skills format](https://agentskills.io/specification). The R Stack skill content needs no client-specific copy. Skill installation does not install plugin hooks or configure MCP connections; those remain host-specific. R Stack ships native plugin metadata for Claude Code, Codex, and Cursor.

Checked on 2026-09-17 with `skills@1.6.0`: each of the seven agent targets installed the starter skill and its reference into an isolated temporary project. Native commands above were checked against official documentation or installed CLI help. Claude's plugin/catalog validators pass. These checks do not run the models or certify activation in every app.

For shared CLI installs, use `npx skills check` and `npx skills update`. Native plugins update through their client marketplace. Rebuild and re-upload web skill ZIPs after changes.
