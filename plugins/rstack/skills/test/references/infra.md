# Infrastructure and deployment checks

Identify the environment, account/project, region, namespace, deployment revision, and resource ownership before running changes. Reuse the repository's CI/IaC tooling. Static validation, a plan, local containers, and a deployed smoke test establish different things.

Start with configuration/schema checks and the existing IaC validation/tests. Then exercise the relevant deployed boundary in a disposable environment when authorized. Do not apply a production plan, mutate live IAM, restart shared services, or inject faults merely because a general testing task exists.

Inspect Terraform test files before running them. `terraform test` defaults to applying real resources; a `command = plan` run and mocked providers have different effects. Test-specific state does not make cloud usage free or remove the need for a suitable target.

Choose checks according to the failure:

- Container build/start, health/readiness, port binding, writable paths, non-root identity, architecture, resources, and shutdown. A listening port is weaker evidence than the intended service becoming ready.
- Deployment routing, DNS/TLS, ingress, auth/secrets injection, outbound connectivity, dependency readiness, and log/metric availability. Distinguish localhost, container network, cluster service, and public edge paths.
- Database migration from the prior supported version, safe rerun, rollback/recovery assumptions, durable volumes, and restart behavior. Use a fixture backup for restore testing; backup creation alone does not prove recovery.
- Rolling update, drain, termination deadline, leader handover, queue redelivery, and temporary dependency outage where relevant. Define the permitted disruption and recovery deadline first.
- IAM/RBAC boundaries and denied operations using test identities. Successful admin credentials do not prove the app's identity has correct permissions.

Create a unique run identifier and label resources. Collect logs/events before teardown, then remove only owned resources and check cleanup. Treat leftover cloud resources as an explicit result, not a reason to broadly delete the environment. Keep budget, duration, and resource ceilings for provisioned infrastructure.

Use the provider's current test/validation facilities and the actual deployment version: [Terraform tests](https://developer.hashicorp.com/terraform/language/tests), [Kubernetes probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/), and [Docker health checks](https://docs.docker.com/reference/dockerfile/#healthcheck). Read [concurrency.md](concurrency.md) before parallel provisioning, fault injection, or load testing. Local emulators don't establish real IAM, managed-service limits, or cross-region behavior.
