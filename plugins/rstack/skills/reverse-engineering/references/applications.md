# Application feature tracing

Read this when a shipped app or website, rather than a complete source repository, is the authority for a feature.

## JavaScript and Electron

Inventory the supplied tree or ASAR without executing entry points or dependency scripts. Locate package metadata, main/preload/renderer boundaries, bundles, source maps, routes, and native add-ons. Use source maps as candidate mappings; verify that they belong to the supplied bundle and retain their original locations. A map can be stale, incomplete, or contain source the destination project is not permitted to copy.

Start from the user action or an identifiable handler. Trace renderer calls through preload exposure, IPC channels, main-process handlers, and native or filesystem operations. Inspect serialization and validation at each relevant boundary. A matching channel name on two sides is a lead; establish the handler binding and payload transformation.

For minified bundles, inspect a focused module or function. Do not feed a whole bundle into context or assume beautification recovered the original source. Dynamic imports, computed properties, runtime-generated code, and missing native dependencies limit static conclusions.

## Websites

Use supplied assets or saved captures for offline questions. For live observations, select the authorized page and profile and follow the runtime reference. Inspect the requested interaction, relevant scripts, DOM state, and network exchange. A screenshot shows appearance; it does not establish the backend algorithm.

Separate client behavior, server responses, and inferred server implementation. Similar results can come from different algorithms. If the server is unavailable, specify only the observed interface and state the missing authority. Do not crawl unrelated pages or replay requests with session credentials to infer hidden behavior.

## Android and Apple applications

For APKs, separate manifest declarations and resource decoding from DEX/JVM method analysis and native libraries. Read the relevant activity/service, resource identifier, method references, and bridge before inferring a feature. JADX and Apktool serve different purposes; resource decoding does not prove code behavior. Permission declarations do not establish permission use or current device grants.

For Apple bundles, inspect the bundle manifest, executable slices, linked frameworks, resources, and available symbols. Objective-C selectors and Swift metadata supply leads, not executed call paths. A signed or encrypted artifact can limit recoverable code. Report the limit rather than promising full source recovery.

Use a supplied emulator, device, or test account only within the authorized scope. Static APK/bundle analysis does not authorize installation, launch, data extraction, or device-state changes.

## Comparing releases

Match the same product, architecture, packaging role, and configuration. Compare member digests before analyzing changed modules. Preserve duplicate-member identity and complete inventory coverage when claiming absence. Paths and addresses can change without behavior changing; stable names can conceal changed behavior.

Trace a candidate difference to the requested feature. Use comparable runtime inputs when a behavioral conclusion requires them. If one build cannot run, report a static change and its likely effect as an inference, not a demonstrated regression.
