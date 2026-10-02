# Concurrency, realism, and load

## Parallel test execution

Parallelize tests only when their mutable resources are isolated. Assign each worker its own account/profile, schema or namespace, files, ports, device/session, and artifact directory as needed. Serialize operations that truly share an exclusive device, foreground window, terminal, or migration lock. Avoid solving collisions by retrying the whole suite.

Bound workers to available CPU/memory, container/device capacity, connection pools, and provider limits. More workers can create harness failures rather than app failures. Keep setup/teardown ownership explicit. Cleanup must not race with another test still using the resource. [Playwright parallelism](https://playwright.dev/docs/test-parallel).

## Race and reliability tests

Use barriers or controlled scheduling to overlap competing operations. Assert a specific invariant, such as exactly one reservation succeeds or a repeated idempotency key creates one order. Inspect final state through the relevant contract. Repeating a sequential happy path is weak evidence for a race.

Test duplicate/delayed/out-of-order messages, lost responses after successful writes, optimistic-lock conflicts, retry storms, lease expiry, and cancellation according to the design. Inject time or network faults at a narrow boundary for deterministic reproduction, then verify the relevant real dependency. A passing artificial schedule does not prove every possible interleaving.

Classify flakes by evidence. Record attempt count, random seed, resource contention, and failures before rerunning. A retry pass does not erase the initial failure. Quarantine needs an owner, reason, and exit condition. Use bounded retries only when the runner or product contract calls for them; preserve the initial failure evidence. [Playwright retries](https://playwright.dev/docs/test-retries) distinguish a first-pass success from a flaky retry pass. Arbitrary sleeps and blanket retries are not repairs.

## Simulation and performance routes

When reproducibility requires control over clocks, scheduling, randomness, network, or storage, use [simulation-fuzzing.md](simulation-fuzzing.md). A seeded workload on an uncontrolled runtime isn't automatically deterministic simulation; preserve real-adapter checks.

Use [performance.md](performance.md) for workload models, arrival rate versus concurrency, generator saturation, latency, profiling, and comparable measurements. Keep load generation separate from CI worker parallelism. Synthetic journeys provide repeatability; real-service smoke checks and existing telemetry address different integration and traffic questions. Label their evidence and avoid delivering synthetic orders, notifications, or emails to real users.
