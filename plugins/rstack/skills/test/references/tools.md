# Prefer supported modern tooling

Choose active maintenance, relevant host support, reproducible execution, diagnostics, and integration with the project over novelty alone. Verify current docs, release support, and installed version. Prefer supported stable releases for a new setup; don't silently upgrade a running shared service or replace a useful maintained runner just because it is older.

## Shortlist by job

| Job | Consider | Selection boundary |
| --- | --- | --- |
| JS/TS logic and features | [Vitest](https://vitest.dev/guide/) or the stack's maintained native runner | Match transforms/runtime; don't simulate browser-only behavior as Node evidence |
| Real browser components | [Vitest Browser Mode](https://vitest.dev/guide/browser/) with Playwright/WebdriverIO provider | A preview/simulated-event provider is different evidence from real automation |
| Browser end-to-end | [Playwright](https://playwright.dev/docs/intro) | Durable assertions, tracing, fixtures, engine coverage |
| Agent browser/terminal exploration | agent-browser, browser-control, tuistory | See [browsers.md](browsers.md) and [tui.md](tui.md); exploration still needs assertions |
| Native OS interaction | CUA CLI/SDK or supported native runner | See [os-automation.md](os-automation.md); background delivery and isolation matter |
| Network faults/fakes | [MSW](https://mswjs.io/docs/) or existing transport fixture | Mock a boundary, then verify relevant real integration separately |
| Real disposable dependencies | [Testcontainers](https://testcontainers.com/) | Actual engine/version and runtime availability; no public-service credentials needed for local containers |
| API generation/contracts | [Schemathesis](https://schemathesis.readthedocs.io/en/stable/), Pact | Generated schema cases need business/security assertions; provider verification still matters |
| Property/stateful cases | [fast-check](https://fast-check.dev/docs/introduction/), Hypothesis, language-native generators | Independent invariant, minimized failing input, reproducible seed |
| Mutation/sensitivity | [Stryker](https://stryker-mutator.io/docs/) or targeted local mutation | Limit scope/cost; investigate equivalent mutants rather than chasing a score |
| Load/reliability | k6 or the stack's existing maintained runner | Explicit workload, thresholds, budget, and suitable target |
| Formal modeling/proofs | Lean with the project’s pinned toolchain | [formal-models.md](formal-models.md): accepted spec, assumptions, trust, and implementation mapping |
| Fuzzing/schedule exploration | Native fuzz runner, AFL++, cargo-fuzz, Loom, or existing simulator | [simulation-fuzzing.md](simulation-fuzzing.md): distinct methods and controlled nondeterminism |
| Profiling/benchmarks | Stack-native profiler and existing benchmark harness; Perfetto where suitable | [performance.md](performance.md): representative workloads and uninstrumented comparison |
| Accessibility | [axe-core](https://www.deque.com/axe/core-documentation/) plus actual keyboard/assistive-technology checks | Automated findings cover only part of accessibility |
| AI quality/evals | Existing deterministic harness or [promptfoo](https://www.promptfoo.dev/docs/intro/) where useful | Pin cases/providers; don't silently invoke paid models or trust judges as facts |
| Firmware, HDL, kernel, games | Stack-native runners from the relevant target reference | A general browser tool doesn't replace a board, simulator, kernel, or engine runner |

Install only tooling needed for the task. Keep maintained stdlib, pytest, Go/Rust native runners, or framework-native tooling when they fit. Replace unsupported or unsuitable tools, not merely old ones. Prefer semantic locators, condition waits, structured results, and isolated fixtures over coordinate scripts or fixed sleeps. Retain host checks those abstractions cannot reach.

## Replace tooling deliberately

State the concrete problem the replacement solves and exercise the same representative passing/failing cases with both routes. Check feature parity, cancellation, setup cost, concurrency/isolation, artifacts, supported hosts, and CI behavior. Preserve bugs/regressions and fixture meaning during migration. Remove the superseded runner/config/dependency only after its unique coverage has moved. Don't run duplicate suites indefinitely or introduce wrappers solely to disguise a second runner.

Use the project package manager and lockfile. A temporary `bunx --bun`, `uvx`, or equivalent invocation can avoid global installation where the tool supports it; pin durable CI dependencies. Don't force Bun or Python onto a stack whose supported driver requires a different runtime. CLI/SDK calls are preferable to a new MCP connection when they accomplish the same workflow.
