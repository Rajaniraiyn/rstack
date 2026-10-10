# Keep the suite useful

Use this workflow for requested test cleanup, slow/flaky suites, or duplicated coverage found during authorized changes. Optimize failure detection, diagnosis, and maintenance cost, not deletion count or coverage percentage alone.

## Inventory before changing

Read applicable repository instructions and the relevant tests, production paths, fixtures, CI selection, and useful history. Establish a baseline and record existing failures. Group by the behavior protected and the boundary exercised, not only by filenames. Identify its primary test owner and any separate transport, lifecycle, platform, or security risk. Measure slow cases, retries, expensive setup, and test-support code where they affect the task.

For each proposed removal or consolidation, identify what failure it can catch and what retained test still catches that failure. Similar-looking tests may protect different OSs, transport paths, security guards, or migration versions. A failed test may expose a product defect. Don't delete it simply because the suite turns green afterward.

Temporary probes and durable regressions need different retention decisions; use [test-lifecycle.md](test-lifecycle.md). Preserve useful minimized fuzz corpora, replay traces, accepted models, and stable performance requirements when consolidating their harnesses.

## Candidates to inspect

- Assertions with expected values computed by the code under test, tautologies, and fixtures that inject the expected outcome before the action.
- Source/import/string checks that enforce incidental organization rather than a stable contract.
- Tests of private call order, helper names, mock interactions, or snapshots that change under a behavior-preserving refactor.
- Repeated examples of the same behavior at the same boundary; expensive end-to-end copies of detailed cases already protected elsewhere.
- Assertions that can pass without exercising the named behavior, including rejection by an unrelated earlier guard.
- Unused fixtures, obsolete adapters, dead quarantines, and production exports/flags added solely for brittle tests.
- Excessive fixture setup, shared mutable state, arbitrary sleeps, broad retry policies, and unbounded snapshots.

These are suspects, not automatic deletion rules. Packaging, release metadata, stable CLI/protocol bytes, defaults, architecture restrictions, and declared public exports may justify exact/static checks. Slow real integration tests can be the only meaningful evidence for a driver or persistence bug.

## Edit one coherent area

Keep valuable tests. Rewrite coupled tests at a useful interface when they protect a real behavior. Merge equivalent cases into a table and consolidate repeated setup. Remove duplicates only after identifying remaining coverage; remove obsolete support code only after checking non-test callers. Preserve useful failure labels and cases. Avoid a parameterized mega-test that reports only that one of fifty workflows failed.

Retain narrow adapters that make real hardware or a closed host observable, as described in [custom-tooling.md](custom-tooling.md). Remove seams that only preserve internal implementation tests. Don't perform unrelated production refactors merely to reduce test-support code.

Improve speed from measured bottlenecks. Reuse immutable expensive setup, isolate mutable state, select targeted tests, and apply bounded parallelism. Don't skip critical host tests because unit tests are faster. Avoid broad runner migration in a cleanup unless the requested scope and evidence justify it. Make edits between runner executions, not during a run whose inputs can change beneath it.

## Verify remaining confidence

Run focused tests and the repository's required checks. For removed static assertions, execute the artifact or supported boundary they claimed to protect when possible. Use a targeted bad fixture/mutation when it helps show retained tests still fail correctly. Report what retained checks protect after removals, deleted support code, useful exceptions, measured runtime changes, and unresolved failures. Do not claim the suite became faster without comparable timing evidence. Keep the result in the conversation unless a document is requested.

The [OpenClaw test-audit skill](https://github.com/openclaw/openclaw/tree/main/.agents/skills/test-audit) informed evidence checks before test removal and retention of independently useful contracts.
