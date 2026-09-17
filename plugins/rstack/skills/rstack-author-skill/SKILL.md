---
name: rstack-author-skill
description: Create or revise a portable skill for a personal skills repository, including its supporting resources and installation checks. Use when adding a reusable agent workflow to R Stack.
---

# Author a skill

Identify the repeatable task, the requests that should trigger it, and the expected result. Use the user's examples when available. Ask only for missing decisions that would change the skill's behavior.

Inspect the target repository's authoring instructions and an existing skill before choosing a location. In R Stack, use `plugins/rstack/skills/<skill-name>/`.

Write a `SKILL.md` with a matching lowercase, hyphenated name and a description that identifies the task and trigger. Keep the body focused on decisions an agent would otherwise get wrong. Preserve the user's scope and avoid introducing extra approval steps.

Use [the portability checklist](references/portability.md) when the skill must work across clients. Put supporting references, executable helpers, and output templates inside the skill directory. Link references where the agent needs them. Do not require another installed skill unless that dependency is intentional and documented.

In an R Stack checkout, run `uv run scripts/rstack.py check` and package the skill with `uv run scripts/rstack.py package`. In another repository, use its own checks. Exercise any new script with a representative input. Check a realistic matching request and a nearby request that should not trigger the skill.

Report the skill's location, intended trigger, validation results, and any host-specific limitation.
