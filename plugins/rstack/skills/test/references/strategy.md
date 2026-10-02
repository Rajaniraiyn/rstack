# Choose tests that can find the bug

## Map behavior and risk

Inspect the change and its callers, schemas, saved formats, build/configuration, and runtime boundaries. For a new product, map its main behaviors first. Identify which failures lose data, cross an authorization boundary, block the main task, or leave a system unable to recover. Test those before incidental display details.

Keep a small working matrix in the conversation, scaled to the task:

| Behavior/change | Expected result or invariant | Relevant target/boundary | Dependency mode | Check and status |
| --- | --- | --- | --- | --- |
| Retry a timed-out write | One durable operation despite duplicate requests | Client, API, actual datastore | Controlled timeout plus real datastore | Overlap/retry and inspect outcome |
| Power fails during a settings update | Prior or new valid settings after reboot | Firmware, persistent storage | Emulation and bench device | Interrupt selected write phases |

These are examples, not mandatory cases. Add a target only when it changes behavior or is part of the support promise. Use representative combinations for independent factors; explicitly test interacting factors such as OS plus plugin ABI or firmware plus board revision. An indiscriminate Cartesian product wastes execution without identifying risk.

## Pick the strongest economical check

| Change or uncertainty | Useful technique |
| --- | --- |
| Public behavior regressed | Reproduce through that interface and retain a sensitive regression |
| Parser, serializer, state machine | Boundaries, malformed inputs, property/stateful testing, bounded fuzzing |
| Backend, driver, plugin, native bridge | Contract tests plus an actual integration check |
| Ordering, shared state, retries | Controlled overlap, fault injection, explicit invariants |
| Refactor, optimization, replacement | Differential checks against an independent reference or supported baseline |
| Data migration or format evolution | Prior-version fixtures, upgrade, repeat run, recovery |
| Numerical/model behavior | Known examples, justified tolerances, representative held-out cases |
| Packaging, architecture, configuration | Build and run the produced artifact on the relevant host |
| Performance claim | Comparable workload/environment, steady-state metrics and predefined limits |

Choose a known expected value, a public contract, or an independently implemented model. Two implementations that share the same faulty helper can agree and still be wrong. Round trips alone may miss mutually compatible encoder/decoder defects. For invariants without a single expected output, use relationships such as equivalent input partitions, conservation, monotonicity, or state-transition rules only when the product contract supports them.

## Strengthen coverage without padding the suite

Use [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) or the stack's property runner to generate and shrink cases; [stateful tests](https://hypothesis.readthedocs.io/en/latest/stateful.html) can check sequences. Preserve seeds and minimized failures. For native parsers, [libFuzzer](https://llvm.org/docs/LibFuzzer.html) is one supported route. Bound time, memory, input size, and corpus growth; run on owned targets. Fuzzing without a correctness check may find crashes but miss invalid successful results.

Probe assertion sensitivity when it matters. Run a bug fixture, a deliberate wrong response, or a narrow mutation in an isolated copy and confirm the intended assertion fails. Distinguish an assertion failure from a broken setup. Never leave the mutation in user code or reinterpret a setup crash as proof of a useful test.

Use line/branch coverage to find unexercised changed behavior, then ask whether assertions protect it. High percentages don't prove correctness, and unchanged trivial getters don't justify a flood of tests. Include relevant negative, recovery, lifecycle, compatibility, and resource-limit paths. Avoid snapshots that merely preserve the current bug.

Use changed paths and dependency maps to select fast local checks, then the affected integration/host checks. Selection is an optimization, not proof that omitted paths are unaffected: include callers, shared fixtures, configuration, and generated artifacts. Keep the repository's required CI/release checks. Expand when new failures or a cross-cutting change justify it. If repeated attempts only reproduce a missing capability, stop that branch, report the prerequisite, and continue independent checks. Don't replace missing evidence with a longer suite on the wrong runtime.
