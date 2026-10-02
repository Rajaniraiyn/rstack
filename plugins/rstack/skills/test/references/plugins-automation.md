# Plugin hosts, developer tools, and automation

This route covers editor plugins beyond VS Code, DCC/CAD/office extensions, build plugins, language servers, task automation, bots, and scheduled workers. Identify the real host version, loaded artifact, permissions, lifecycle, and API/ABI. A standalone script that uses the same code doesn't prove the host loaded or invoked the plugin.

Reuse the host's headless/test mode when it covers the required behavior. Otherwise run a test-owned host profile or isolated desktop and exercise registration, commands, events, persisted settings, errors, and disposal. Check packaging/install, restart, host updates, conflicting plugins, and missing assets according to the compatibility promise. Keep user's documents, profiles, and installed plugins outside the fixture.

For editor/language-server/debugger tooling, test protocol framing and lifecycle as well as language features. Check initialize/capability negotiation, document versions, incremental edits, cancellation, stale responses, diagnostics, and shutdown. Use real client/host integration for behavior it owns. The [Language Server Protocol](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/) defines an applicable contract; stdout protocol traffic must remain separate from diagnostics on stdio transports.

For build/task plugins and code transformations, use small consuming projects with representative files. Check clean versus incremental execution, cache invalidation, dependency graphs, parallel builds, watch/restart, generated-file ownership, and failure exit status. A cache hit shouldn't conceal an invalid fresh build. Verify generated output builds or performs its expected behavior.

For automations/bots/scheduled workers, control clock/events and use test destinations. Check duplicate events, retries, cancellation, missed schedules, overlapping runs, timezones/DST, and recovery after restart. Verify exactly-once product claims through durable effects; transport delivery promises may be weaker. Never send test email/chat messages to real people without authorization. Use sandbox accounts/endpoints or stubs, then a bounded authorized real integration check.

If the host has no usable driver, add the narrow helper described in [custom-tooling.md](custom-tooling.md). Keep protocol, headless-host, and actual UI coverage separate. Use [cli.md](cli.md), [api-backend.md](api-backend.md), or [os-automation.md](os-automation.md) for the corresponding interaction boundary.
