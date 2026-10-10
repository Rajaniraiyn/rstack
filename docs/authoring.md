# Authoring

## Add a skill

Create `plugins/rstack/skills/your-skill/SKILL.md`:

```markdown
---
name: your-skill
description: What the skill does, then when to use it. Describe the task and its matching user requests without a long synonym list.
---

# Your workflow

Describe the expected result and the decisions specific to this task.
```

The `description` is the routing text agents see before loading `SKILL.md`. Keep it concise, describe the task and when to use it, and include words users are likely to say. The [Agent Skills specification](https://agentskills.io/specification) defines `name`, `description`, and optional `license`, `compatibility`, `metadata`, and experimental `allowed-tools`. `metadata` is a string-to-string map. Provider extensions may use namespaced metadata keys when that host documents them, but do not invent trigger or description fields that no host reads.

Use a shared frontmatter extension when multiple target hosts implement the same behavior. Claude Code, Cursor, and OpenCode v2 recognize `disable-model-invocation`, which prevents automatic selection while retaining explicit invocation. Strict Agent Skills upload APIs may reject this extension. Check each host's current documentation.

Use an adapter for settings that only one host supports and that cannot be expressed through its standard `SKILL.md` format. Codex reads optional interface text and `policy.allow_implicit_invocation` from `agents/openai.yaml`; it does not define a subagent. Claude Code's `user-invocable` controls the user command menu separately from automatic invocation. For subagent behavior, use the target host's agent definition or invocation feature. Do not add adapter files to skills that do not need them. Extend the R Stack validator when adopting another frontmatter extension, and record its supported hosts and type there.

Add only fields needed for behavior or presentation:

| Host | Skill metadata location | Examples |
| --- | --- | --- |
| Agent Skills | `SKILL.md` | `name`, `description`, `license`, `compatibility`, string-valued `metadata`; `allowed-tools` is experimental. |
| Claude Code | `SKILL.md` frontmatter | `disable-model-invocation`, `user-invocable`, `argument-hint`, `context`, and `agent`. Its `when_to_use` adds routing context to `description`. |
| Cursor | `SKILL.md` frontmatter | `disable-model-invocation`, `paths`, `icon`, and `color`. |
| OpenCode | `SKILL.md` frontmatter | `disable-model-invocation`; optional `metadata.opencode/autoinvoke` overrides it when both are set. |
| Codex | `agents/openai.yaml` | UI text, `policy.allow_implicit_invocation`, and supported tool dependencies. |

R Stack validates matching names, descriptions, non-empty optional fields, string-valued metadata, and consistent invocation settings. Explicit-only skills must include the Codex policy adapter. UI prompts name their own skill, and picker descriptions follow the local 25–64 character convention.

Check host fields against [Claude Code](https://code.claude.com/docs/en/skills), [Cursor](https://cursor.com/docs/skills), [OpenCode v2](https://opencode.ai/v2/docs/skills), and [Codex](https://learn.chatgpt.com/docs/build-skills).

Keep the applicable license notice in every distributed archive, including standalone skill archives. Prefer stdlib-only Python or plain markdown over shell scripts for Windows compatibility. Put references, helpers, and output templates inside the skill directory and use relative links.

Limit `description` to 1024 characters and `compatibility` to 500. Use `compatibility` for runtime requirements. Codex `interface.short_description` is picker text, separate from the routing description.

Skills allow automatic selection unless marked explicit-only. Set `disable-model-invocation` for Claude Code, Cursor, and OpenCode v2, and the Codex policy adapter for Codex. Hosts that ignore an extension will not enforce it.

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

[Matt Pocock's skills](https://github.com/mattpocock/skills), [Anthropic skills](https://github.com/anthropics/skills), [OpenAI plugins and skills](https://github.com/openai/plugins), [Cursor's template](https://github.com/cursor/plugin-template), and [pstack](https://github.com/cursor/plugins/tree/main/pstack) informed the structure and invocation policies. Record upstream revisions and licenses when adapting material. Use the [skills CLI](https://github.com/vercel-labs/skills) for agent discovery and installation paths.

## Compare and evaluate

Use the maintainer skill's [research guide](../plugins/rstack/skills/rstack-author-skill/references/research.md) for source selection and [evaluation guide](../plugins/rstack/skills/rstack-author-skill/references/evaluation.md) for routing and behavior checks.

Give each conditional reference a reading condition. Preserve task scope, authorization, and invocation policy. Test routing and task behavior separately from static validation and report which checks ran.

Update model shortlists in place and verify harness support. Resolve CLI flags, APIs, and prices from installed versions and current vendor sources.

Exercise integrations on their actual runtime. For a renderer, inspect its output; for a driver or service, execute a scoped call. Configure external tools separately and preserve authorization for execution, attachment, extraction, interception, and device changes. Use supported background input or an isolated desktop for foreground-dependent controls. Distinguish host, simulated, emulated, bench, and deployed results. Check external licenses and capabilities before use.
