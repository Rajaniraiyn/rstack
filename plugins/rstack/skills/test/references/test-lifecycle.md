# Durable tests, temporary probes, and evidence

Execution layer, test purpose, and retention are separate decisions. A temporary integration probe can be valuable without joining every CI run. A benchmark can be durable but run only on a controlled host. Choose retention from future failure risk and maintenance cost, not filename or line count.

## Decide what should remain

| Artifact | Default treatment |
| --- | --- |
| Stable behavior/regression test | Keep in the appropriate existing suite when it protects a credible recurring failure |
| Exploratory reproducer or diagnostic probe | Run in an owned scratch directory; promote if the behavior needs lasting coverage |
| Expensive fuzz/DST campaign | Keep useful harness, invariant, minimized corpus, and replay case; separate bounded CI checks from longer campaigns |
| Formal model and proof | Keep when it documents an accepted contract; pin dependencies and maintain the implementation mapping |
| Performance harness/baseline | Keep when representative and reproducible enough for an agreed decision or supported gate |
| Profiles, captures, huge traces, random campaign outputs | Share relevant evidence paths; avoid committing sensitive or bulky artifacts by default |

Follow repository conventions and the user's requested deliverable. Temporary doesn't mean assertion-free or disposable before diagnosis. Don't add a second permanent runner just to preserve a one-off experiment.

## Make a temporary probe trustworthy

Record hypothesis, expected independent result, relevant revision/build, runtime, dependency mode, input/seed, and command before running. Use a task-owned scratch path outside automatic test discovery and release packaging. Where imports/builds require a project-local file, mark its ownership and remove only that file after the experiment. Never run a general cleanup glob over existing untracked user files.

Separate fixture/setup failure from the behavior being investigated. Capture failures before retries or cleanup. Bound execution time, output size, resources, and external effects; preserve existing credentials/session boundaries. Isolated copies are appropriate for deliberate bad mutations. A probe must not leave mutations in production code, alter a shared baseline, or suppress failures to appear successful.

Keep enough evidence to reproduce the result until handoff: exact script or meaningful command, minimal fixture/trace, relevant version and result. Don't expose secrets in shared output. Report which artifact is temporary, whether it was removed, and where retained evidence lives. Honor a request to keep the reproducer.

## Promote findings into the right owner

When a probe reveals a real bug, establish the intended behavior from an accepted spec or user decision. Repair only within the requested scope. Show the minimized reproducer fails for the original cause when feasible and passes after the fix. Preserve a durable regression if the bug is likely to recur and retained coverage doesn't already detect it. Fold the case into the existing owner rather than keeping both the exploration script and an equivalent permanent test.

For a resolved one-off environment question or low-impact change already covered, the temporary probe may be sufficient. Explain the evidence rather than generating a permanent test that mirrors the implementation. Remove owned scaffolding once evidence is captured and check no production flags, debug exports, fixtures, or background workers were left behind.

Use [suite-maintenance.md](suite-maintenance.md) before deleting existing tests. Use [formal-models.md](formal-models.md), [simulation-fuzzing.md](simulation-fuzzing.md), and [performance.md](performance.md) for specialized proof, replay, corpus, and measurement evidence. A bounded campaign, diagnostic profile, finite simulation, and kernel-checked theorem are distinct results; report each with its own assumptions and limits.
