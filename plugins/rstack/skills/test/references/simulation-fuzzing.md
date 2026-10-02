# Simulation, fuzzing, and invariant-driven testing

Use these methods for parsers, protocols, storage, schedulers, retry logic, resource ownership, and stateful systems where examples miss combinations. Start with a concrete contract and observable failure. Existing runners, narrow injected dependencies, and a small harness usually beat building a simulator for an unrelated feature. Agree unresolved domain semantics before making them the oracle.

## Deterministic simulation testing (DST)

[TigerBeetle's VOPR](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/internals/vopr.md) runs production logic against controlled environmental boundaries. Apply the method where the architecture permits it: inject virtual time, seeded randomness, an explicit event queue/scheduler, network delivery, and storage behavior. Record every remaining source of nondeterminism, including threads, iteration order, wall-clock calls, and external services. Repeating a seed while those inputs vary is not deterministic replay.

Generate operations and faults together: partitions, duplication, delayed acknowledgements, restarts, partial writes, and recovery. Model only faults permitted by the actual storage/protocol contract; invented durability guarantees can conceal defects. Check safety after relevant transitions; check progress within stated healthy conditions and bounds. A permanently partitioned system need not satisfy unconditional liveness. For internal state, use justified protocol invariants as well as user-visible outcomes; [TigerBeetle's protocol-aware DST](https://tigerbeetle.com/blog/2026-08-20-protocol-aware-dst/) illustrates this distinction.

Keep replay records containing seed, source revision, harness/toolchain versions, configuration, initial state, operations, fault decisions, event order, and failed invariant. A seed alone may stop reproducing after implementation changes. Minimize the failing trace while preserving its preconditions and violation; retain both the original and reduced reproducer. Fix the local defect, rerun the reproducer, then explore additional seeds. Promote the smallest meaningful case into an owned regression.

For an idempotent writer, one useful scenario is: persist a write, lose its acknowledgement, restart, then retry the same key. Check one committed effect and the specified reply. This makes the failure actionable rather than reporting merely that a random run crashed.

Finite simulation campaigns provide bounded evidence, not proof. Validate real adapters and environmental assumptions separately; [TigerBeetle's Vortex](https://tigerbeetle.com/blog/2025-02-13-a-descent-into-the-vortex/) tests actual infrastructure. For narrower concurrency exploration, [Loom](https://docs.rs/loom/latest/loom/) explores schedules through its instrumented Rust primitives; it does not automatically control arbitrary OS I/O or replace full-system DST.

## Fuzzing harnesses and campaigns

Choose the smallest entrypoint that reaches the risky behavior. Seed it with valid, malformed, boundary, and historical failure inputs. Combine structure-aware generation with mutations when checksums or grammars otherwise block deeper paths. Separate public-input rejection from internal preconditions: fuzz both accepted states and rejection behavior without bypassing the contract accidentally.

Define an oracle beyond “did not crash”: round-trip rules, an independent reference implementation, conservation laws, state-machine transitions, bounded resource consumption, or specified error classes. Do not copy implementation logic into the oracle. Reset mutable state between independent inputs; for stateful bugs, explicitly encode operation sequences and reset between sequences. [AFL++ persistent-mode guidance](https://github.com/AFLplusplus/AFLplusplus/blob/stable/instrumentation/README.persistent_mode.md) explains why incomplete resets produce misleading results.

Useful starting points are [Go's built-in fuzzing](https://go.dev/doc/security/fuzz/), [cargo-fuzz](https://rust-fuzz.github.io/book/cargo-fuzz.html) for Rust, and [AFL++](https://github.com/AFLplusplus/AFLplusplus) for suitable native targets. Retain an effective existing LLVM harness: [libFuzzer](https://llvm.org/docs/LibFuzzer.html) receives important bug fixes, although its original authors stopped major feature development. Match the engine, instrumentation, and supported target platform; “modern” alone does not justify migration.

Set explicit wall-time, CPU, worker, memory, input-size, and timeout budgets. Isolate filesystem/network effects and never fuzz an inferred production target. Instrument native code with appropriate sanitizers. Preserve minimized crashes, hangs, leaks, sanitizer findings, and semantic failures with their environment; distinguish harness defects from product defects. Keep a compact coverage corpus and replay saved failures in ordinary CI; longer campaigns can run separately. Deduplicate failures by cause without discarding distinct violated contracts.

## Applying TigerStyle carefully

[TigerStyle](https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md) motivates explicit invariants, bounded queues/work, simple state transitions, and reasoning before randomized execution. Adapt those principles to the repository. Do not impose its assertion counts, allocation policy, naming conventions, or Zig-specific rules on another stack.

Test valid-to-invalid transitions, exhaustion, overflow, cancellation, and recovery. Prefer understandable ownership and explicit units over redundant state. Assertions express programmer invariants; external malformed input and expected operating errors require ordinary validation and handling. Review whether assertions execute in release builds, have side effects, disclose secrets, or turn attacker-controlled input into process termination. Production fail-stop behavior requires the system's safety and availability design. Fuzzing supplements human reasoning and reviewed specifications; a silent campaign does not establish correctness.
