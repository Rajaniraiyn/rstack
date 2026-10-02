# Commits and pull requests

Follow the repository's commit convention and PR template. Write for a reviewer who has not seen the conversation. Keep accurate claims, the reason for the change, and relevant validation.

## Commit message

Name the concrete change in the summary. Use the project's casing and prefix convention. A body earns its place when it explains a non-obvious reason, compatibility constraint, or migration. Preserve required trailers and attribution.

A measured improvement can be a useful summary, such as "cut deploy time from 40 minutes to 4". Use it only when the measurement exists. Otherwise name the mechanism, such as "reuse build artifacts during deploy".

## PR description

Lead with the problem and resulting behavior. Explain a consequential tradeoff when it affects review. Include checks that establish the change works and material limitations, such as an integration test that could not run. CI status complements this evidence; it does not replace context for the reviewer.

Use a short paragraph for a simple change. For a larger change, group concrete outcomes and validation so reviewers can scan them. A fixed bullet count or mandatory format adds noise when the repository already has a template.

Cut effort narration, praise, generic claims, and requests to "please review". Link the issue without forcing the reviewer to reconstruct the implementation from it. Use screenshots for visual changes and label what changed.

## Large changes

Keep each PR coherent. Recommend splitting independent work when it improves review, while preserving the user's requested scope. Creating, pushing, or rebasing a stack is a separate action from editing a PR description. Dependency-ordered PRs require compatible tooling and branch management; do not assume every host provides a native stacking workflow.

## Example

Before:

> This PR significantly enhances performance through comprehensive improvements. Please review.

After, when supported by the actual diff and test run:

> The deploy runner now downloads independent artifacts in parallel and keys its cache by the lockfile hash. The runner tests pass; production timing has not been measured.
