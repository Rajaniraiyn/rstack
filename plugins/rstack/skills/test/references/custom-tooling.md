# Custom tooling when the stack needs it

First establish what the available drivers can observe and control. Missing accessibility nodes, a closed shadow tree, canvas input, a native bridge, or an embedded engine can justify a small app-specific helper. Do not add a framework simply because the skill lists it.

Choose the smallest reusable approach:

1. Extend the repository runner or expose stable accessibility identifiers.
2. Add a test-only adapter around an existing public interface or native automation API.
3. Build a narrow driver for the required operations when no supported route exists.

A helper should declare its supported host/builds and provide capability discovery, structured results, finite deadlines, useful errors, and cleanup for owned resources. Keep app/window/device/session identity explicit. For a local protocol, bound input and bind locally; avoid a generic arbitrary-code execution endpoint when a few named operations suffice.

Separate operations from assertions. The helper drives input or observes state; the test derives expected results from a contract. A test hook that returns the same computed value as the implementation is not an independent correctness check. Verify one real input-to-effect journey so bypassing the UI doesn't hide broken event wiring.

Keep test hooks and debug ports out of production builds unless they are an intentional product interface. Avoid secrets in helper output. Document permissions and setup in the project's existing development docs. Host adapters belong with their host; portable instructions should describe the behavior and requirements.

Validate the helper against an actual failing case and a passing case. Check timeout, missing target, stale handle, teardown, and malformed input. Reuse existing error/result conventions. Don't create an always-on MCP server, service, hook, or remote account if a command or temporary process can do the job.

When the host is unavailable, continue with useful logic, contract, or renderer checks and report the exact native checks that remain blocked. Building a mock host is a valid intermediate test, but it doesn't remove that limitation.
