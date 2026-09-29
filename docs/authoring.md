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

The `description` is the routing text agents see before loading `SKILL.md`. Keep it concise, describe the task and when to use it, and include words users are likely to say. The [Agent Skills specification](https://agentskills.io/specification) defines `name`, `description`, and optional `license`, `compatibility`, `metadata`, and experimental `allowed-tools`. `metadata` is a string-to-string map. Provider extensions may use namespaced metadata keys when that host documents them, but do not invent trigger or description fields that no host reads.

Use a frontmatter extension in the shared file when multiple target hosts implement the same behavior. Claude Code and Cursor both document `disable-model-invocation`; it prevents automatic selection while retaining explicit invocation in their standard skill flows. This field is a provider extension, not part of the Agent Skills core schema, so strict upload APIs may reject it. OpenCode v2's `metadata.opencode/autoinvoke` is a namespaced setting inside the standard `metadata` map. Keep its value as a string for compatibility with the core schema. Check each host's current documentation when relying on an extension.

Use an adapter for settings that only one host supports and that cannot be expressed through its standard `SKILL.md` format. Codex reads optional interface text and `policy.allow_implicit_invocation` from `agents/openai.yaml`; it does not define a subagent. Claude Code's `user-invocable` controls the user command menu separately from automatic invocation. For subagent behavior, use the target host's agent definition or invocation feature. Do not add adapter files to skills that do not need them. Extend the R Stack validator when adopting another frontmatter extension, and record its supported hosts and type there.

Use this as a field map, not a checklist. Add only fields that change the intended behavior or presentation:

| Host | Skill metadata location | Examples |
| --- | --- | --- |
| Agent Skills | `SKILL.md` | `name`, `description`, `license`, `compatibility`, string-valued `metadata`; `allowed-tools` is experimental. |
| Claude Code | `SKILL.md` frontmatter | `disable-model-invocation`, `user-invocable`, `argument-hint`, `context`, and `agent`. Its `when_to_use` adds routing context to `description`. |
| Cursor | `SKILL.md` frontmatter | `disable-model-invocation`, `paths`, `icon`, and `color`. |
| OpenCode | `SKILL.md` frontmatter | The v2 format uses namespaced values such as `metadata.opencode/autoinvoke` and `metadata.opencode/slash`. |
| Codex | `agents/openai.yaml` | UI text, `policy.allow_implicit_invocation`, and supported tool dependencies. |

The same concept may have different field names or effects. For instance, `description` routes a skill across hosts, while Codex `short_description` is UI text and Claude `when_to_use` extends routing text. Check the host docs before adding a field: [Claude Code](https://code.claude.com/docs/en/skills), [Cursor](https://cursor.com/docs/skills), [OpenCode v2](https://opencode.ai/v2/docs/skills), and [Codex](https://learn.chatgpt.com/docs/build-skills).

The `license` field is optional metadata. Keep the applicable license notice in every distributed archive, including standalone skill archives. For executable helpers, prefer stdlib-only Python or plain markdown over shell scripts: Windows may not have bash, and a portable skill should not force one OS's shell. Put references, helpers, and output templates inside the skill directory, use relative links, and add directories only when needed.

The specification defines one `description`, up to 1024 characters. It routes the skill; host UI fields serve a separate purpose. Codex `interface.short_description`, for example, is user-facing text and does not replace the skill description. There is no generic long-description field. Use `compatibility` only for real environment requirements, and keep it under 500 characters.

Availability, audience, invocation, and execution mode are separate choices. A skill can be public to install but aimed at a narrow audience. Automatic selection and user invocation are independent. A skill is not a subagent; isolation and agent definitions are host features.

The current skills have distinct audiences and invocation roles:

| Skill | Audience | Invocation intent |
| --- | --- | --- |
| `stop-slop` | Anyone using the package | The agent may select it for prose work; users can also invoke it directly. |
| `clean-slop` | Anyone using the package | The agent may select it for an AI-slop cleanup pass; users can also invoke it directly. It is not a general code reviewer. |
| `launch-video` | Anyone using the package | The agent may select it for video requests; users can also invoke it directly. Codex has a short UI description. |
| `factory` | Users who explicitly request delegated work | Claude Code and Cursor read `disable-model-invocation`; OpenCode v2 reads its namespaced metadata; Codex reads its policy file. |
| `rstack-author-skill` | R Stack maintainers and contributors | Explicitly invoked for R Stack authoring. It uses the same per-host controls as `factory`. |

These are product choices, not universal defaults. A host that ignores an extension will not enforce its policy. The package is public; "opinionated" describes Rajaniraiyn's perspective, not an access restriction. This draws on the separation between user-invoked and model-invoked workflows in [Matt Pocock's skill suite](https://github.com/mattpocock/skills), and the composable skills and dedicated agents in [Cursor's pstack plugin](https://github.com/cursor/plugins/tree/main/plugins/pstack). Skills may be discovered from a plugin-specific `skills/` directory, but registry listings and install counts depend on each registry's indexing and telemetry rules.

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
