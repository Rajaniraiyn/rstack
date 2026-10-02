# Security and quality checks by requirement

Identify relevant trust boundaries, data sensitivity, identities/roles, supported clients, and externally supplied inputs. Select checks from the actual feature and its failure modes. Use [OWASP ASVS](https://owasp.org/projects/asvs) for applicable application requirements and [MASVS](https://mas.owasp.org/MASVS/) for mobile requirements. Neither is a universal checklist for every development task.

## Check the boundary that enforces the rule

Use positive controls as well as denied cases. Verify the intended security rule causes rejection and that no forbidden side effect occurs. An invalid token can reject a request before a broken tenant authorization check is reached; that does not prove tenant isolation. Repeat where the enforcing boundary differs, such as local host versus remote backend.

Choose relevant cases:

- Authentication/session expiry, authorization by role/tenant/object, privilege changes, and sensitive state after logout. Hiding a UI control doesn't establish backend access control.
- Input parsing, uploads, path handling, command/query injection boundaries, output escaping, and unsafe deserialization where implemented. Use controlled fixtures on owned test targets.
- Extension/webview message origins, CSP, native IPC capabilities, sandbox/filesystem access, and secret leakage to logs/traces or exports.
- Credential/config handling, transport verification, update/firmware integrity, and device permissions where those are explicit requirements. Test rejected artifacts without permanently altering device security configuration.
- Agent/tool workflows with untrusted content, data exfiltration attempts, repeated actions, and tool arguments outside the task boundary. Check observable actions, not only the model's verbal refusal.

## Automation and its limits

Use existing dependency/secret checks and targeted [Semgrep](https://semgrep.dev/docs/) or [CodeQL](https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-code-scanning) rules where appropriate. Inspect findings in the actual code path and retain useful regressions. Static findings are candidates to validate, and a clean scan isn't proof of security.

For web exposure, [ZAP baseline](https://www.zaproxy.org/docs/docker/baseline-scan/) combines crawling with passive scanning. Passive analysis still generates traffic through its crawler. Scope target, routes, accounts, and request budget. Active scanning, intrusive fuzzing, disruptive fault injection, and attempts to exploit external systems require a suitable authorized target and scope; don't infer production authorization from ordinary feature testing.

Keep secrets and private captures out of shared artifacts. Record the requirement, target, actual evidence, confirmed finding, and residual limits. Distinguish a control test, scan result, and penetration test. Do not claim compliance/certification or exhaustive security coverage from a selected automated suite.

For other quality dimensions, use [test-design.md](test-design.md), [games-media.md](games-media.md), and [concurrency.md](concurrency.md). Security scanning does not replace their requirements or evidence.
