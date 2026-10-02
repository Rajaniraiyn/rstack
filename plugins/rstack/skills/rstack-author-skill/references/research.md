# Compare and update skills

Use this reference for a competitive audit, a dependency or framework refresh, or deciding whether to add or merge a skill.

## Discover through several routes

Inspect `bunx --bun skills -h` before relying on its flags. Search by user task, capability, and owner, then list an upstream repository without installing:

```sh
bunx --bun skills find video
bunx --bun skills find writing --owner mattpocock
bunx --bun skills add mattpocock/skills --list
bunx --bun skills add anthropics/skills --list
bunx --bun skills add cursor/plugins --list --full-depth
```

Use a direct repository or a well-known skill endpoint when search misses it. The registry may still list removed names or omit new ones. Verify the current `SKILL.md`, bundled files, license, and commit. A listing or install count is discovery evidence, not a quality score. In skills CLI 1.7.0, `add --list --json` is rejected; use listing output or inspect the source rather than accidentally installing.

For OpenAI examples, check [openai/plugins](https://github.com/openai/plugins). [openai/skills](https://github.com/openai/skills) now carries a deprecation notice; old catalog entries and cached CLI results may still expose it.

## Read authoritative guidance

| Question | Source |
| --- | --- |
| Portable format and field constraints | [Agent Skills specification](https://agentskills.io/specification) |
| Codex authoring and invocation | [OpenAI build skills](https://learn.chatgpt.com/docs/build-skills) |
| Keep instructions short and task-specific | [OpenAI prompt and skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) |
| Behavioral evaluation | [OpenAI skill evals](https://developers.openai.com/blog/eval-skills) |
| Claude authoring and progressive disclosure | [Anthropic best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| Claude invocation and host fields | [Claude Code skills](https://code.claude.com/docs/en/skills) |
| Cursor discovery and host fields | [Cursor skills](https://cursor.com/docs/skills) |
| Pointer wording and instruction hierarchy | [Matt Pocock writing for agents](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents) |
| Composable engineering workflows | [Cursor pstack](https://github.com/cursor/plugins/tree/main/pstack) |
| Scheduler-specific skill integration | [Poteto Noodle authoring](https://github.com/poteto/noodle/blob/main/.agents/skills/noodle/references/skill-authoring.md) |

Official skill repositories are examples, not the shared specification. A Noodle `schedule` field, Remotion `version` field, or Claude `context` setting has no portable effect unless the target host implements it. Check current docs before adopting a field.

## Decide and record

For each local skill, compare trigger, outcome, instruction cost, resource completeness, dependencies, host assumptions, licensing, and validation. Record one of keep, rewrite, extend, merge, replace, or remove, with the evidence that supports it.

A merge earns its place when users get the same outcome with fewer overlapping routes. A replacement earns its place when a maintained upstream tool covers the current requirements and migration preserves outputs. Keep a working fallback until the replacement succeeds on a representative task.

For additions, show the recurring use case and why an existing skill or a small reference extension does not cover it. Prefer an optional upstream skill for a fast-moving vendor API. Active MCPs, hooks, scheduler services, and credentials require a concrete workflow and their own validation.

Report source dates, commits, decisions, and material uncertainty in the user's requested format. Use the conversation unless they requested a saved report. Keep source links in the references that need them, and date a version-sensitive shortlist when its freshness affects routing. Copy third-party files only with compatible licensing and preserved attribution. Summarize principles in original prose when vendoring would create avoidable maintenance.
