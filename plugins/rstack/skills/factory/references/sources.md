# Sources

Feed the factory from the issue and reporting sources the user configured. When the user pastes a link or names a source, fetch it with the matching CLI or MCP instead of guessing.

## GitHub issues

```sh
gh issue list --repo owner/repo --state open --limit 50 --json number,title,labels
gh issue view 123 --repo owner/repo --json title,body,labels,comments
```

Use `gh` for anything GitHub-first: issues, PRs, and cross-referenced data. GitHub MCP servers work too when the user has one wired.

## Sentry

Sentry surfaces errors to fix, not features to build. Use the Sentry CLI against the user's org and project:

```sh
sentry-cli issues list --org ORG --project PROJECT
```

Classify by frequency, impact, and stack: a top issue is a fix task, not a design discussion. Sentry MCP servers can pull event detail when configured.

## Jira

```sh
jira issue list --query 'project = X and status = Open' --limit 25
```

Pull the ticket, its acceptance criteria, and linked issues. Route a ticket's sub-tasks to different tiers when it mixes mechanical and hard work.

## Linear

Use the Linear CLI or MCP the user has installed. List open issues or a single issue by identifier, then route by status and scope.

## MCP servers

If the user pointed at an MCP server for a source, use its tools directly. MCP is the escape hatch for sources without a CLI here: Notion, Slack, internal trackers. Prefer the configured or named source over probing for one.

## Open-ended intake

When the user gives a link or a description instead of a configured source:

1. Identify the source from the link (GitHub, Sentry, Jira, Linear, or whatever it is).
2. Fetch it with the right CLI or MCP. If no tool reaches it, say so instead of fabricating.
3. Classify into a routing unit: goal, constraints, expected output, rough size, and tier.

## Classification

For each item, state:

- Type: bug, feature, task, review.
- Priority and impact: what breaks if it is not done.
- Rough size: minutes, hours, or days of agent work.

That is the input to [routing.md](routing.md). Keep intake raw and complete; do not summarize away the acceptance criteria the implementer needs.