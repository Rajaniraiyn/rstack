# Performance tests and profiling

Start with a user-visible requirement and representative workload. A benchmark measures cost, a regression gate enforces an agreed limit, and a profile investigates where resources go. None replaces functional correctness. Don't add a performance suite solely because a helper can be timed.

## Choose the experiment

| Question | Useful evidence |
| --- | --- |
| Did a local algorithm get more expensive? | Optimized-build microbenchmark with meaningful inputs and outputs consumed |
| Does the application meet its response budget? | Representative feature/journey latency, including queuing and dependencies |
| What happens near capacity? | Bounded load/stress test with offered and achieved rates, errors, and saturation |
| Does behavior deteriorate over time? | Bounded soak with memory, handles, queues, storage, and recovery observations |
| Why is the operation slow? | CPU/wall-time, allocation, I/O, lock, or scheduling profile for that operation |
| Does the experience remain smooth? | Frame pacing, input latency, startup, and energy/resource observations on the supported device |

Define input sizes/distributions, dataset/cache state, build/configuration, hardware/runtime, metric, time/resource budget, and acceptance threshold before execution. Use an existing SLO or accepted specification. If the requirement is ambiguous, ask for the consequential decision; exploratory measurements can continue without inventing a release gate.

## Measure without manufacturing a win

Use the same workload and comparable builds/environments for baseline and candidate. Account for warmup/JIT, caches, GC, compiler elimination, background work, thermal throttling, power mode, and virtualization. Consume computed outputs and check correctness. Include cold startup when it is the requirement rather than discarding it as warmup. Keep setup and teardown outside the timed region unless they are part of the operation being measured.

Collect repeated independent samples sufficient for the decision, including spread, sample count, and errors. Alternate baseline/candidate runs when drift matters. Keep raw measurements and report units, absolute cost, relative change, and relevant percentiles. Don't report a p99 from a tiny sample as stable evidence, discard slow runs opportunistically, or call noise an improvement. A faster result caused by lost work or weakened durability is a correctness regression.

Shared CI hosts may justify a controlled comparison, wider noise-aware threshold, or a dedicated performance job. Keep exploratory profiles and unstable measurements separate from deterministic functional gates. Do not normalize away saturation or silently update a performance baseline to pass.

## Load and capacity

Use [concurrency.md](concurrency.md) for isolated workers and authorized targets. Choose arrival-rate or closed-user models deliberately. A closed workload can reduce offered load as latency rises, hiding overload through coordinated omission; an arrival-rate workload must report dropped iterations and generator saturation. [k6 workload models](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/).

Observe client and server: throughput, tail latency, errors/timeouts, backlog, pool pressure, CPU, memory, storage/network, and recovery after load stops. State whether latency includes queued/dropped work. Bound duration, data growth, concurrency, and abort criteria; preserve user services and don't infer permission to stress production.

## Profile the suspected resource

Start with the bottleneck hypothesis. Check utilization, saturation, and errors for relevant resources rather than assuming high CPU explains all latency; the [USE method](https://www.brendangregg.com/usemethod.html) is a useful investigation framework. Wall time includes waits that a CPU profile may miss. Allocation rate differs from retained memory; compare heap/handle observations across comparable completed cycles when investigating leaks.

Prefer the stack's existing profiler: browser DevTools, platform Instruments/Android tools, Go pprof, supported native sampling, or [Perfetto](https://perfetto.dev/docs/) for appropriate traces. Python's [cProfile documentation](https://docs.python.org/3/library/profile.html) explicitly distinguishes profiling from benchmarking. Sampling and instrumentation have different overhead; symbol/build mismatch or missing stack visibility can mislead either. Check installed help and host permissions; do not broaden kernel privileges or attach to unrelated processes merely for convenience.

Capture the smallest interval that includes the suspect work with build IDs/symbols and scenario markers where supported. Trace files can include private data. Compare representative traces, identify the actual bottleneck, make a focused change, and rerun correctness plus the original uninstrumented benchmark. A flame graph alone doesn't prove a speedup.

Retain a stable performance regression when a supported requirement needs ongoing enforcement. Keep diagnostic traces and one-off harnesses according to [test-lifecycle.md](test-lifecycle.md). Report measured results and limits; do not turn profiling output into an unearned universal performance claim.
