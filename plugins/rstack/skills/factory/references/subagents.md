# Delegation and session context

Choose a mechanism from the host's actual capabilities. A subprocess, subagent, worktree, and sandbox are separate things; one does not imply the others.

| Mechanism | Use when | Check before running |
| --- | --- | --- |
| Built-in subagent | A scoped task needs the current project's tools and returns to this conversation | Shared filesystem, inherited context, allowed models, tool permissions |
| Headless worker | Work needs a separate process, worktree, harness, or supported spend cap | Working directory, authenticated route, output file, permission mode |
| Session fork | A retry benefits from verified findings in an existing session | Fork support, explicit session ID, inherited permissions, shared files |
| Fresh session | Prior context is misleading or the repository or task changed | Complete brief, required references, base revision |

Prefer a built-in subagent for a small independent subtask when available. Separate writers still need separate file ownership or worktrees. A headless process does not automatically isolate writes. A fork usually copies conversation state, not a repository snapshot.

Use the installed help and [harnesses.md](harnesses.md) to resolve commands. Preserve explicit session IDs rather than selecting the latest session in a concurrent run. Resume continues the existing session; fork creates another where the host supports it.

Give workers the smallest complete brief, verified findings, and required resources. Avoid passing entire transcripts when a scoped handoff is enough. Keep nested delegation within the parent's concurrency and spend limits. Workers should return blockers to the parent rather than start additional unbudgeted harnesses.

Add a scheduler or persistent queue only for a requested queueing or recurring workflow. Document its requirements separately.
