# Authoring

## Add a skill

Create `plugins/rstack/skills/your-skill/SKILL.md`:

```markdown
---
name: your-skill
description: Describe the repeatable task and when the agent should use it.
---

# Your workflow

Describe the expected result and the decisions specific to this task.
```

Keep `name` and `description` portable. Put references, executable helpers, and output templates inside the skill directory, and use relative links. Add directories only when needed. Optional Codex display metadata belongs in `agents/openai.yaml`; essential instructions must work without it.

The included `rstack-author-skill` can guide this process. Check a matching request and a nearby request that should not trigger the skill. Test executable helpers with representative inputs.

## Maintain the package

Edit `plugins/rstack/plugin.json` for the version, author, and HTTPS repository URL. It is the canonical portable manifest. Run `uv run scripts/rstack.py sync` to regenerate the three client manifests and three marketplace catalogs. Extend `manifests()` when adding provider-specific fields; direct edits to generated files fail validation.

```sh
uv run scripts/rstack.py sync
uv run scripts/rstack.py package
uv run python -m unittest discover -s tests
```

`package` validates before exporting. Use `check` alone for validation without ZIPs. Archives preserve bundled resources and executable permissions, with stable ordering and timestamps. The packager rejects symlinks, environment files, and common caches. Distribute the filenames printed by the latest run; `dist/` can contain older versions.

The tooling handles one bundle, `rstack`. Extend it only when separate plugin installation becomes necessary. Choose a license before public distribution; none has been assigned yet. Development uses uv; run `uv sync` once for an environment.

## Add integrations

Shared skill syntax does not standardize all host configuration. Add integrations for a concrete workflow and verify them in each intended client.

| Component | Where it belongs |
| --- | --- |
| Workflows and bundled resources | Inside their skill directory |
| Portable MCP configuration | Plugin-root `mcp.json`, following the [Agent Plugins specification](https://agent-plugins.org) |
| Claude/Codex compatibility MCP | Plugin-root `.mcp.json` and the relevant manifest wiring |
| Cursor MCP and rules | Plugin-root `mcp.json` and `rules/*.mdc`, following [Cursor's reference](https://cursor.com/docs/reference/plugins) |
| Hooks | Client-specific configuration and scripts |
| Repository instructions | `AGENTS.md`; `CLAUDE.md` imports it for Claude Code |
| OpenAI app connections | `.app.json` only when an actual registered app mapping exists |

Keep credentials in client configuration. Document runtime and tool requirements, and test a real tool call before marking an integration supported. Amp also offers skill-level MCP wiring, but that is an [Amp extension](https://ampcode.com/docs/customize/skills), not a requirement other agents inherit.

## Design references

The structure follows the [Agent Skills specification](https://agentskills.io/specification) and [portable plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json). Native packaging follows [OpenAI](https://developers.openai.com/plugins/build/plugins), [Claude Code](https://code.claude.com/docs/en/plugins-reference), and [Cursor](https://cursor.com/docs/reference/plugins).

[Matt Pocock's skills](https://github.com/mattpocock/skills), [Anthropic skills](https://github.com/anthropics/skills), [OpenAI skills](https://github.com/openai/skills), and [Cursor's template](https://github.com/cursor/plugin-template) informed the original structure. No third-party skill content is copied. The [skills CLI](https://github.com/vercel-labs/skills) owns agent discovery and installation paths.
