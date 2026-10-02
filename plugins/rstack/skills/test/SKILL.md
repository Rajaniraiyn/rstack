---
name: test
description: Design, run, debug, and maintain meaningful tests for software, services, and devices. Use for test strategy, feature validation, regressions, suite cleanup, formal models, fuzzing, performance investigations, and quality checks on the intended runtime. Fix failures when requested; choose useful coverage rather than generating redundant tests.
license: MIT
---

# Test

Find failures that matter to users, reproduce them, and verify the result on the intended runtime. Honor report-only requests. When the task includes fixes, continue through the repair and regression check.

## Choose the boundary

Inspect repository instructions, build scripts, existing tests, lockfiles, and CI. Identify the behavior under test, observable expected result, supported runtime/build, and available host or device. Reuse useful existing tooling. For a new setup or justified replacement, read [tools.md](references/tools.md); check installed help and current upstream docs before using version-sensitive commands.

Read only the guidance needed for the task:

- [strategy.md](references/strategy.md) for risk, representative coverage, and assertion sensitivity.
- [test-design.md](references/test-design.md) when authoring tests or choosing layers and quality dimensions.
- [suite-maintenance.md](references/suite-maintenance.md) for requested cleanup, slow/flaky suites, or duplicated coverage.
- [security-quality.md](references/security-quality.md) for security requirements and trust boundaries.
- [formal-models.md](references/formal-models.md) for Lean modeling, agreed specifications, proof checks, and implementation mapping.
- [simulation-fuzzing.md](references/simulation-fuzzing.md) for deterministic simulation, fuzzing, replay, and invariant-driven testing.
- [performance.md](references/performance.md) for benchmarks, load/soak tests, profiling, and performance regressions.
- [test-lifecycle.md](references/test-lifecycle.md) for temporary probes, durable tests, and evidence retention.

A hybrid system may need several target references. For an unlisted stack, identify its input, state, outputs, lifecycle, and actual host. Avoid forcing native behavior into a browser workflow.

| Target or condition | Read |
| --- | --- |
| Web app, browser automation, authenticated browser | [browsers.md](references/browsers.md) |
| CLI arguments, streams, subprocess behavior | [cli.md](references/cli.md) |
| TUI, interactive prompt, terminal rendering | [tui.md](references/tui.md) |
| VS Code desktop, web, or remote extension | [vscode.md](references/vscode.md) |
| Chrome or other browser extension | [browser-extensions.md](references/browser-extensions.md) |
| Electron, Tauri, native desktop, nested webviews | [desktop.md](references/desktop.md) |
| Android app or embedded Android webview | [android.md](references/android.md) |
| iOS, iPadOS, watchOS, or native macOS | [apple.md](references/apple.md) |
| Flutter mobile, web, or desktop | [flutter.md](references/flutter.md) |
| MCU, bare metal, RTOS, embedded Linux, FPGA/HDL | [embedded.md](references/embedded.md) |
| Robotics, control loops, sensor fusion, physical actuators | [robotics.md](references/robotics.md) |
| SDK, package, compiler, generator, native/FFI, WASM, kernel code | [libraries-toolchains.md](references/libraries-toolchains.md) |
| Serial, USB, BLE, CAN, IoT, custom binary/network protocol | [protocols.md](references/protocols.md) |
| Database/ETL, analytics, numerical code, ML, AI agents | [data-ml.md](references/data-ml.md) |
| Game, simulation, GPU/canvas, audio/video, XR | [games-media.md](references/games-media.md) |
| Other editor/DCC/office plugins, LSP, build tools, automations | [plugins-automation.md](references/plugins-automation.md) |
| HTTP, GraphQL, RPC, streaming API, backend jobs | [api-backend.md](references/api-backend.md) |
| Deployment, containers, migrations, infrastructure | [infra.md](references/infra.md) |
| Parallel execution, races, load, real versus simulated dependencies | [concurrency.md](references/concurrency.md) |
| OS controls, background input, CUA, keeping the user's desktop usable | [os-automation.md](references/os-automation.md) |
| Missing tooling, custom controls, unusual stack | [custom-tooling.md](references/custom-tooling.md) |
| Selecting or refreshing comparable tools and skills | [sources.md](references/sources.md) |

## Reproduce, inspect, repair, verify

1. Establish a baseline with the command, revision/build, runtime, and fixture. Run relevant existing checks. Distinguish a product failure from unavailable tooling, devices, or setup.
2. Exercise the intended interface and assert its observable outcome. Inspect relevant logs, requests, exits, persisted state, host messages, or measurements. Wait for a specific state with a timeout; launch, idle, or a screenshot alone proves little.
3. Isolate mutable resources and clean up only resources this run owns. Preserve user sessions and services. For OS actions, prefer targeted background delivery or an isolated desktop; honor the user's nonintrusive requirement without a focus-stealing fallback. External writes and disruptive load must fit the authorized environment and scope.
4. Isolate the cause and make the smallest sufficient repair when requested. Retain a useful regression, demonstrate it catches the original failure when feasible, and never weaken assertions or silently accept snapshots to get a pass.
5. Rerun the failed journey and affected checks. Verify the packaged/native host when the failure crosses that boundary. A mock bridge or browser preview cannot establish native integration.
6. Report passed, failed, blocked, and not-run checks with commands and useful evidence paths. Label actual hosts, simulators/emulators, physical devices, and real versus simulated dependencies. Do not claim a platform passed because another did.

For broad requests, keep a compact working matrix of behaviors, targets, dependency mode, and status in the conversation. Scale coverage to risk and the support promise. Do not create an audit document unless requested.
