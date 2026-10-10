# Tools and integrations

Read this when selecting an analysis method or troubleshooting an integration.

## Prefer the smallest existing capability

| Need | Possible local route | Evidence boundary |
| --- | --- | --- |
| Identity and archive inventory | Format-aware parsers, hashing, archive listing | Metadata and members, not execution |
| Native layout and instructions | `readelf`, `objdump`, platform equivalents | Headers, symbols, assembly, not recovered source |
| Native decompilation and cross-references | Existing Ghidra, Hopper, IDA, or REA provider | Engine-dependent approximations and coverage |
| Managed methods | Existing .NET IL/decompiler tools, JADX for DEX | Static code and metadata, not runtime dispatch |
| Resources and firmware | Existing Apktool, Binwalk, Unblob, bundle parsers | Declarations or extracted regions, not observed behavior |
| Browser/process/device observations | Host-approved browser tools, debugger, PTY, emulator, adb | The selected scenario and host only |
| Multi-artifact evidence and feature tracing | Connected REA MCP or installed CLI | Actual advertised operations and provider prerequisites |

Check installed versions, command help, and supported target/host before using a route. Avoid wrappers that merely rename an upstream command. Missing decompilation does not block useful inventory or assembly inspection. Never claim an engine ran because its command was listed.

## Optional REA route

Use an existing REA connection or CLI. Configure REA and its prerequisites separately when needed. Do not run setup before every investigation or overwrite this skill with upstream instructions.

For a connected MCP, discover real tool schemas. Examples from the inspected upstream revision include `analyze_javascript_application` for a tree/ASAR, `inspect_managed_artifact` for .NET, `inspect_android_package` for APK code, and `open_binary` for native active-target analysis or archive inventory. Availability differs by release, provider, and host. Target-free operations take explicit inputs; do not create a native session for them. IDA does not supply every Hopper/Ghidra overview operation.

Start with summary output when supported. Follow evidence references into focused module/function views. Preserve returned limitations and unknowns. A retained reference belongs to its connection; separate CLI calls need saved complete evidence. A transport truncation or timeout is not evidence that analysis failed or stopped. Inspect state before repeating work.

For an installed CLI, confirm `rea --version` and `rea --help`, then the chosen command's help. The inspected upstream documents this static JavaScript route:

```sh
rea analyze-javascript-application /absolute/path/to/app --json > app-evidence.json
```

Choose a new output path in the authorized workspace, preserve existing files, and check the exit status before consuming JSON. This command analyzes supplied files, not the application's runtime. Native commands need the selected engine. Verify declared claims in the result rather than treating exit zero as complete coverage.

## Missing tools and setup

Distinguish missing client registration, stale connection, host approval rejection, missing launcher/PATH, incompatible runtime, and unavailable provider. Repair only the observed blocker. A client-policy denial does not justify bypassing approvals or installing an engine.

If REA registration is actually requested, consult current [installation documentation](https://github.com/morluto/rea/blob/main/docs/installation.md) and the client's supported configuration. Inspect the scoped setup dry-run first, including changed paths, backups, and replacement skill. Apply only authorized changes and verify an actual tool call afterward. Package acquisition can execute installer code; do not use an unreviewed `npx ...@latest` invocation as a silent fallback.

Keep provider configuration and credentials in the host adapter/client. Filter exposed MCP tools to the operations needed when the host supports filtering. Use upstream schemas and report whether the connection was tested.
