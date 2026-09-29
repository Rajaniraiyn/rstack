# Authoring

## Add a skill

Create `plugins/rstack/skills/your-skill/SKILL.md`:

```markdown
---
name: your-skill
description: What the skill does, then when to use it. Name the exact requests that should load it: user actions and phrases, in quotes.
---

# Your workflow

Describe the expected result and the decisions specific to this task.
```

The `description` is the routing text that agents see before loading `SKILL.md`. Keep it concise, describe the task and when to use it, and include words users are likely to say. The [Agent Skills specification](https://agentskills.io/specification) defines `name`, `description`, and optional `license`, `compatibility`, `metadata`, and experimental `allowed-tools`. `metadata` is an arbitrary string-to-string map, not a standard routing mechanism. Do not duplicate trigger phrases there.

Keep canonical frontmatter to the specification's fields. Add host-specific metadata only when that skill needs the behavior. Codex's optional `agents/openai.yaml` can set UI text and `policy.allow_implicit_invocation`; it does not define a subagent. Claude Code has separate invocation fields, which are not portable and may be rejected by other Agent Skills upload paths. Its `disable-model-invocation` controls automatic invocation, while `user-invocable` controls the user command menu. Those settings are distinct. If a workflow needs subagent behavior, use the target host's agent definition or invocation feature. Do not add an adapter file to every skill by default.

The `license` field is optional metadata. Keep the applicable license notice in every distributed archive, including standalone skill archives. For executable helpers, prefer stdlib-only Python or plain markdown over shell scripts: Windows may not have bash, and a portable skill should not force one OS's shell. Put references, helpers, and output templates inside the skill directory, use relative links, and add directories only when needed.

The specification defines one `description`, up to 1024 characters. Some hosts provide optional UI metadata with a shorter user-facing description; those fields do not replace the portable description and should be maintained in that host's adapter. Use `compatibility` only for real environment requirements, and keep it under 500 characters. Avoid invented metadata fields such as `long-description` unless a named consumer reads them.

The included `rstack-author-skill` can guide this process. Check a matching request and a nearby request that should not trigger the skill. Test executable helpers with representative inputs. In this package, `rstack-author-skill` and `factory` are explicit-only in Codex. `launch-video` has Codex display text and can be invoked explicitly or selected by its description. `clean-slop` and `stop-slop` use their portable descriptions for automatic selection and remain available for direct requests. Other hosts may need separate adapters to enforce the same choices. Skills may be discovered from a plugin-specific `skills/` directory, but registry listings and install counts depend on each registry's indexing and telemetry rules.

## Maintain the package

Edit `plugins/rstack/plugin.json` for the version, author, and HTTPS repository URL. It is the canonical portable manifest. Run `uv run scripts/rstack.py sync` to regenerate the three client manifests and three marketplace catalogs. Extend `manifests()` when adding provider-specific fields; direct edits to generated files fail validation.

```sh
uv run scripts/rstack.py sync
uv run scripts/rstack.py package
uv run python -m unittest discover -s tests
```

`package` validates before exporting. Use `check` alone for validation without ZIPs. Archives preserve bundled resources and executable permissions, with stable ordering and timestamps. The packager rejects symlinks, environment files, and common caches. Distribute the filenames printed by the latest run; `dist/` can contain older versions.

The tooling handles one bundle, `rstack`. Extend it only when separate plugin installation becomes necessary. Development uses uv; run `uv sync` once for an environment.

The [skills.sh](https://skills.sh) repo page groups skills into sections from a root-level `skills.sh.json` (`groupings`, `notGrouped`). This file changes page display, not indexing or installs. skills.sh says it learns the grouping file after a CLI install with telemetry enabled, and repo pages are cached. A skill missing from the page may not yet have been observed or indexed; changing its grouping does not create an install record. See the [customize docs](https://skills.sh/docs/customize).

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

[Matt Pocock's skills](https://github.com/mattpocock/skills), [Anthropic skills](https://github.com/anthropics/skills), [OpenAI skills](https://github.com/openai/skills), and [Cursor's template](https://github.com/cursor/plugin-template) informed the original structure. No third-party skill content is copied, except `launch-video/references/brag/`, which vendors the MIT-licensed [/brag skills](https://github.com/latent-spaces/brag) with their license and source commit. The [skills CLI](https://github.com/vercel-labs/skills) owns agent discovery and installation paths.
