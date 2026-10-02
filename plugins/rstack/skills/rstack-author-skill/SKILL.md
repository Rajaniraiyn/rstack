---
name: rstack-author-skill
description: Create, compare, or revise self-contained portable skills in R Stack. Maintainer workflow for skill authoring, frontmatter, resource structure, and validation.
license: MIT
disable-model-invocation: true
---

# Author a skill

Start from the repeatable task and the decisions an agent needs help making. In R Stack, canonical skills live in `plugins/rstack/skills/<skill-name>/`. Read the repository instructions and an existing skill before editing.

## Establish the need

Identify the user's matching requests, a nearby request outside scope, and the expected artifact. Inspect existing skills before adding another. Merge overlapping branches when they share an outcome and invocation policy; keep independently useful workflows separate. Preserve installed names unless a migration is intentional.

For a comparison or update, read [references/research.md](references/research.md). Discover comparable skills in several ways, inspect their actual source, and check current official docs. Borrow a useful design principle without inheriting another package's services, approvals, scheduler, or tool names.

## Write the smallest complete workflow

Keep `name` and `description` in valid YAML. The description tells the host what the skill does and when it applies. The body states the outcome, essential decisions, constraints, and completion conditions. Remove instructions that repeat host behavior or can be obtained from one local lookup.

Inline what every branch needs. Put substantial branch-specific details in a bundled reference and link it with a condition for reading it. Put deterministic repeated operations in scripts and output material in assets. Add a file only when the workflow uses it. Keep independently installed skills self-contained.

Read [references/portability.md](references/portability.md) for frontmatter and host boundaries. New skills use automatic discovery unless the user requests explicit-only invocation; preserve existing policy unless the user requests a change. Provider-specific settings belong in the documented adapter, not a portable workflow's prose.

## Validate and hand off

Use [references/evaluation.md](references/evaluation.md) to check routing and task behavior. Static validation proves structure, not task quality. Exercise changed helpers with representative inputs and include an error or boundary case where it matters.

In this checkout, run:

```sh
uv run scripts/rstack.py sync
uv run scripts/rstack.py check
uv run python -m unittest discover -s tests
uv run scripts/rstack.py package
```

Edit shared identity in `plugins/rstack/plugin.json` before syncing. In another repository, use its own checks. Report the skill location, intended scope, changes, checks actually run, and host or runtime limitations. Separate a proposed evaluation from a completed run.
