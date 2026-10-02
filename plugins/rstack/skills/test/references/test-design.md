# Test layers, purposes, and responsibilities

Execution layer describes how much of the system runs. Purpose explains why a check exists; quality dimension explains what it measures. Keep these separate so a regression, security assertion, or contract can live at the appropriate layer.

## Select the execution layer

| Layer | Responsibility | Common misuse |
| --- | --- | --- |
| Unit | A meaningful computation or rule with controlled dependencies | One test per private helper, trivial assignment, or call count |
| Feature/component | Behavior through a subsystem's public interface, possibly spanning modules | Mocking away the behavior and asserting the mock |
| Integration | Interaction with an actual datastore, driver, host, transport, or plugin | Calling a fully stubbed path integration |
| End-to-end | Critical input-to-outcome journey through the intended system | Replaying every detailed rule already protected by focused tests |

Use the project's vocabulary. A feature test needn't use a browser, and a unit needn't be one function. Choose the least costly layer that faithfully protects the behavior. Add higher-layer checks for distinct risks such as transport, packaging, lifecycle, or native wiring. Assign a primary test owner to each contract; another layer should protect a risk that owner cannot reach. Hardware-in-the-loop and emulator checks must also state what actually runs.

## Separate purposes and quality dimensions

- A regression protects a previously failing behavior at any layer.
- A contract/compatibility check establishes independent agreement between consumers, protocols, schemas, formats, or supported versions. Provider verification belongs at the actual provider boundary.
- A smoke check selects a small readiness or packaging subset after build, install, or deployment. Launch or HTTP 200 alone is weak evidence for a feature.
- An eval measures variable task quality across representative cases with explicit scoring, acceptance criteria, and uncertainty. It complements deterministic orchestration checks; one judge score isn't ground truth. Use [data-ml.md](data-ml.md) for model and agent evaluations.

Functional correctness, security, accessibility, visual appearance, performance, recovery, compatibility, and resource use need different observations. A screenshot can't prove persistence; a role locator can't prove contrast; a functional pass can't prove deadlines. Compile/lint/static-analysis gates protect other contracts. Select dimensions from requirements instead of inventing one universal quality score.

## Keep method and lifetime separate

Property-based testing, fuzzing, deterministic simulation, differential checks, and formal proofs are methods, not extra execution layers. Select them for the failure mode. Lean proves an explicitly modeled proposition; validate the specification and implementation mapping through [formal-models.md](formal-models.md). Use [simulation-fuzzing.md](simulation-fuzzing.md) for controlled schedules and generated inputs.

Temporary probes, retained regressions, scheduled campaigns, benchmarks, and profiles have different lifetimes and execution budgets. Use [test-lifecycle.md](test-lifecycle.md) to decide what belongs in the maintained suite. Use [performance.md](performance.md) to distinguish a diagnostic profile from a reproducible measurement or regression gate.

## Write around observable results

Use a behavioral name, minimal credible input, explicit preconditions, the real action, and an independent expected outcome. Include rejected actions and absence of unwanted effects when they are part of the contract. Assert relevant state transitions rather than unrelated fields or incidental logs. Exact bytes/order are appropriate for documented wire formats and observable ordering requirements.

Separate fixture creation, host drivers, fault injection, and assertions. Reuse setup without building a framework for two cases. Parameterize equivalent inputs; keep cases with different setup or failure diagnosis distinct. Tests should run alone and release owned resources after failure as well as success.

Fake costly or uncontrollable dependencies at their documented boundary. Avoid mocks of internal collaborators that dictate implementation. Fixtures must not inject the outcome the action should produce. Verify important fake contracts against real dependencies where appropriate and label fake-backed results.

A new test needs a behavior, a credible failure it catches, and a gap in retained coverage. For a bug, show the assertion fails for the original cause when feasible; disclose unavailable baseline execution. Meaningful existing verification may suffice for a reversible low-impact change. Read [strategy.md](strategy.md) for generated cases and sensitivity checks, and [suite-maintenance.md](suite-maintenance.md) before removing coverage.
