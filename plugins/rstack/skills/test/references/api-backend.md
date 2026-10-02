# APIs and backend behavior

Use the project's client/test runner first. Playwright's request context is useful when an API creates fixtures or verifies effects of a browser journey. A context associated with a browser can share cookies; use a separate context when account isolation matters. [Playwright API testing](https://playwright.dev/docs/api-testing).

Define independent expected results from the public contract, examples, or product behavior. Cover method/status, headers/content type, payload shape and meaning, validation errors, pagination/filtering, authorization, and durable side effects. A 200 response or schema match alone does not establish correctness. GraphQL can return errors with HTTP 200; RPC status and stream completion may carry failures elsewhere.

Use distinct tenants and roles to check unauthorized reads/writes and object-level access. Exercise invalid/expired credentials without exposing tokens in logs. For uploads, webhooks, SSE/WebSockets, and streaming RPC, test framing, cancellation, reconnect, duplication, limits, and partial failure as relevant. Do not log secrets or private request bodies into shareable evidence.

## Choose real and simulated dependencies

| Question | Appropriate check |
| --- | --- |
| Validation or algorithm edge case | Deterministic unit/component test |
| Consumer/provider agreement | Contract test with actual provider verification |
| Queries, transactions, cache, queue behavior | Integration test using the relevant engine/version |
| Credential, network, provider policy, deployed wiring | Small authorized sandbox/staging smoke test |
| Failure difficult to trigger reliably | Controlled fault/stub plus an explicit statement of what it substitutes |

[Pact](https://docs.pact.io/) supports consumer/provider contract checks. [Testcontainers](https://testcontainers.com/guides/getting-started-with-testcontainers-for-nodejs/) can provision disposable real dependencies. Check container runtime availability, wait for readiness, use allocated ports, and keep a unique database/namespace per worker. Match production semantics where the bug depends on them; an in-memory substitute doesn't establish real transaction or indexing behavior.

For jobs and distributed state, assert eventual outcomes with a bounded wait, correlation ID, and useful timeout evidence. Check retry/backoff, deduplication, poison messages, dead-letter handling, cancellation, restart recovery, and ordering. Verify migrations and transaction rollback when implicated. Control clocks/randomness for deterministic cases; keep actual integration checks for serialization and transport.

Use [concurrency.md](concurrency.md) for conflicting writes, duplicate requests, isolation, throughput, and load. A fake dependency and a real one answer different questions; report both when used.
