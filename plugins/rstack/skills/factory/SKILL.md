---
name: factory
description: Delegates software tasks to installed agent CLIs and reviews their results. Use when explicitly asked to set up a factory, farm out issues, or run agent workers.
license: MIT
compatibility: Requires git and at least one installed, authenticated agent CLI. The optional setup helper needs Python 3.10+.
disable-model-invocation: true
---

# Factory

Use the user's available harnesses to complete delegated work. Invocation authorizes delegation for the requested task, not unrelated backlog work, publishing, or broader permissions.

## Prepare a worker brief

Inspect existing factory configuration and probe missing capabilities before asking setup questions. Use [references/setup.md](references/setup.md) for setup or [scripts/factory-setup.py](scripts/factory-setup.py) for a read-only installed-CLI report. Authentication remains the user's responsibility.

Fetch only the work the user selected, using existing connections. Read [references/sources.md](references/sources.md) for issue intake. Give each worker:

- The requested outcome, source issue or local evidence, and an observable completion condition.
- Its base commit, worktree, owned files, and dependencies on other workers.
- Required checks, output location, budget, and actions it may perform.
- A stopping condition for failures, blocked input, or exhausted budget.

## Route and run

Use the current model shortlist, task defaults, and reasoning settings in [references/routing.md](references/routing.md). Preserve the user's selected route and confirm actual harness support. Refresh the shortlist from official catalogs when requested; replace superseded entries rather than appending model history.

Choose the delegation mechanism using [references/subagents.md](references/subagents.md). Parallelize independent tasks; sequence tasks that share a dependency or need another worker's result. Shared-checkout subagents can edit disjoint owned files when their commands do not mutate shared outputs. Use separate worktrees for independent builds, overlapping writes, or headless workers. Worktrees prevent file overwrites during execution but do not prevent integration conflicts or provide a security sandbox. Read [references/worktrees.md](references/worktrees.md) when provisioning them.

Confirm the installed CLI's help before constructing a headless command. Use [references/harnesses.md](references/harnesses.md) for entry points and vendor documentation. Retain the user's execution restrictions. Save logs, exit status, commits, and the worker's final result. Treat successful process exit as execution evidence, then check the artifact against the brief.

## Integrate and review

Inspect each worker's diff, resolve integration conflicts, and run the combined repository checks. Review with an independent harness or model within budget, or perform a separate read-only pass and report the route used. Use [references/reviews.md](references/reviews.md) for the review contract and bounded repair loop.

Preserve worker artifacts and user changes until they are reviewed. Report the branch or worktree, completed outcomes, validation, unresolved work, and route costs when known. Link a local result or an authorized PR. Share or publish a session only when the user requested it.
