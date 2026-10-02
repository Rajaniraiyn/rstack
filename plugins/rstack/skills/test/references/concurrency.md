# Concurrency, realism, and load

## Parallel test execution

Parallelize tests only when their mutable resources are isolated. Assign each worker its own account/profile, schema or namespace, files, ports, device/session, and artifact directory as needed. Serialize operations that truly share an exclusive device, foreground window, terminal, or migration lock. Avoid solving collisions by retrying the whole suite.

Bound workers to available CPU/memory, container/device capacity, connection pools, and provider limits. More workers can create harness failures rather than app failures. Keep setup/teardown ownership explicit. Cleanup must not race with another test still using the resource. [Playwright parallelism](https://playwright.dev/docs/test-parallel).

## Race and reliability tests

Use barriers or controlled scheduling to overlap competing operations. Assert a specific invariant, such as exactly one reservation succeeds or a repeated idempotency key creates one order. Inspect final state through the relevant contract. Repeating a sequential happy path is weak evidence for a race.

Test duplicate/delayed/out-of-order messages, lost responses after successful writes, optimistic-lock conflicts, retry storms, lease expiry, and cancellation according to the design. Inject time or network faults at a narrow boundary for deterministic reproduction, then verify the relevant real dependency. A passing artificial schedule does not prove every possible interleaving.

Classify flakes by evidence. Record attempt count, random seed, resource contention, and failures before rerunning. A retry pass does not erase the initial failure. Quarantine needs an owner, reason, and exit condition. Use bounded retries only when the runner or product contract calls for them; preserve the initial failure evidence. [Playwright retries](https://playwright.dev/docs/test-retries) distinguish a first-pass success from a flaky retry pass. Arbitrary sleeps and blanket retries are not repairs.

## Load and performance

Use the existing load runner, or a tool such as [k6](https://grafana.com/docs/k6/latest/using-k6/scenarios/) when sustained load is required. Define target, duration, rate/concurrency, data shape, thresholds, and abort criteria before running. Stay within the user's authorized environment. Keep CI test parallelism separate from load generation.

Concurrent users and request arrival rate are different models. Choose the model that represents the workload. Report offered and achieved rate, dropped work, latency percentiles, errors, and saturation. A slow load generator can hide overload. Include warmup and steady-state measurement; compare equivalent builds and environments.

Synthetic journeys provide repeatability. Real-service smoke tests catch credentials, transport, deployment policy, and integration differences. Existing production telemetry can show actual traffic distributions without generating new load. State which evidence each result uses. Don't route synthetic orders, notifications, or emails to real users. Fault injection and expensive distributed load require an explicitly suitable target, never an inferred production target.
