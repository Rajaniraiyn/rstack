# Comparable skills and upstream references

Consult this index when choosing a tool or refreshing guidance. Verify commands and platform support against installed help and current upstream docs.

## Skills worth comparing

| Source | Useful comparison |
| --- | --- |
| [Matt Pocock TDD](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd) | Behavior at public boundaries and regression sensitivity. Adapt the technique to the user's scope; don't inherit unrelated mandatory approval steps. |
| [OpenClaw test-audit](https://github.com/openclaw/openclaw/tree/main/.agents/skills/test-audit) | Evidence for suite cleanup, duplicate removal, assertion sensitivity, and retaining real contracts. Adapt to this repository's tooling and requested scope. |
| [Anthropic webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | Server lifecycle and browser reconnaissance. Verify waiting advice against current Playwright docs. |
| [OpenAI Playwright CLI](https://github.com/openai/skills/tree/main/skills/.curated/playwright) and [interactive Playwright](https://github.com/openai/skills/tree/main/skills/.curated/playwright-interactive) | CLI-first exploration and persistent browser/Electron sessions. Host-specific setup stays optional; don't inherit a different skill's global configuration requirements. |
| [Currents Playwright best practices](https://github.com/currents-dev/playwright-best-practices-skill) | Runner structure, diagnosis, and repeatable end-to-end checks. |
| [hzijad Playwright skills](https://github.com/hzijad/playwright-agent-skills) | Smaller suite for writing, reviewing, and debugging tests; compare assertion sensitivity and failure diagnosis. |
| [Vercel agent-browser](https://github.com/vercel-labs/agent-browser) | Agent-driven browser exploration, snapshots, sessions, and tool-specific skills. |
| [anomalyco browser-control](https://github.com/anomalyco/browser-control) | Existing-browser identity, sessions, and authenticated workflows. |
| [remorses tuistory](https://github.com/remorses/tuistory/tree/main/skills/tuistory) | PTY sessions and programmatic TUI testing. |
| [anomalyco terminal-control](https://github.com/anomalyco/terminal-control) | Alternative terminal automation and capture workflow. |
| [indrasvat shux](https://github.com/indrasvat/shux) | Alternative session control to compare when terminal tooling is missing. |
| [Microsoft WinApp](https://learn.microsoft.com/en-us/windows/apps/develop/ai-assisted/testing) | Native Windows agent testing and generated regression tests. |
| [trycua/cua](https://github.com/trycua/cua) | Background desktop delivery, platform refusals, CLI/SDK usage, and isolated desktops. |
| [Flutter agent plugins](https://github.com/flutter/agent-plugins) | Flutter-specific workflows to compare with the official integration runner. |

Evaluate tools against the required boundary, not install counts, skill titles, or claims of universal platform support.

## Discovery without installation

```sh
bunx --bun skills -h
bunx --bun skills find testing
bunx --bun skills find terminal
bunx --bun skills find desktop
bunx --bun skills find mobile
bunx --bun skills find embedded
bunx --bun skills find firmware
bunx --bun skills find testing --owner vercel-labs
bunx --bun skills add remorses/tuistory --list
bunx --bun skills add anomalyco/browser-control --list
```

Search also by framework, runner, platform, and missing capability. Listing a repository does not install its skills. Read the selected upstream skill and executable docs before adopting it. Check license, freshness, host requirements, hidden service dependencies, cleanup behavior, and whether its assertions prove the desired behavior. Record the exact version when a tool is used in a durable test setup.

For tools beyond browser/terminal exploration, use [tools.md](tools.md). Find hardware and domain-specific sources in the target references.

## Models, simulation, and measurements

Use [formal-models.md](formal-models.md) for official Lean proof/trust/build references and [simulation-fuzzing.md](simulation-fuzzing.md) for TigerBeetle VOPR, protocol-aware DST, TigerStyle, Loom, and native fuzzing documentation. Use [performance.md](performance.md) for profiling, tracing, workload models, and the USE method.
