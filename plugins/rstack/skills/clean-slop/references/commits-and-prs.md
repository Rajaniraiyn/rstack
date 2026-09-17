# Commits and pull requests

Keep commits and PRs short, concrete, and unpolished in the right ways. The goal is that a reviewer or future reader can orient in seconds, not that the agent explains itself.

## Commit messages

- One commit per coherent change. If a diff contains unrelated changes, split it.
- The summary line names the outcome, not the effort: "cut deploy time from 40 minutes to 4", not "improve performance" or "update stuff".
- Use the imperative, active voice: "support custom scopes", "require Node.js 22", "drop legacy token fallback". Passive voice reads like a report, not a change.
- Lower case the summary unless a proper noun or identifier needs casing. No trailing period.
- Wrap code identifiers in backticks: `--json`, `toSQL()`, `parser`.
- The body is optional and only when the summary is not enough. Say why, not what. One or two sentences.
- Footers only for metadata: `BREAKING CHANGE:`, `Reviewed-by:`.

Conventional Commits shape when the project uses it:

```text
<type>[optional scope][optional !]: <description>
```

Useful types: `feat` (user-facing capability), `fix` (user-facing correction), `refactor` (behavior-preserving), `perf` (measured change), `docs`, `test`, `chore`. Mark breaking changes with `!` before the colon or a `BREAKING CHANGE:` footer.

Before:
> feat: integrated comprehensive enhancements and optimizations across the platform to significantly improve overall system performance and robustness

After:
> perf: cut deploy time from 40 minutes to 4

## PR titles

- State the outcome in a few words. Same shape as a good commit summary, one level broader.
- No framing as work done: no "Adds implementation for", no "Doing the needful", no "WIP on".

Before: "Improvements to the build system"
After: "Cut deploy time from 40 minutes to 4"

## PR descriptions

The PR body is how the developer talks to the rest of the team. It is not the agent's report back to the person who asked. The chat reply, the commit trail, and CI carry the proof. The PR body exists for reviewers and future readers to orient fast.

- Keep a short summary plus 3-6 bullets of what the PR changes. Fewer bullets if they fit.
- Bullets name concrete outcomes, not effort: "scheduler accepts plain-English schedules", "a column rename fails the build".
- Proof stays out of the PR: what you tested, which checks you ran, what you verified. Those go in your reply in the chat and in the CI status.
- No paragraphs of rationale. If a decision needs explanation, one sentence pointing at the issue or the code comment.
- No self-justification: no "this improves developer experience",
  no praise of the change.
- No filler: no "please review", no "any feedback welcome", no "I hope this helps". Ask for something specific or stay silent.
- Link the issue or ticket when there is one. Repeat the why only if the issue does not carry it.

Before:
> This PR significantly enhances the overall performance of the build system, making it more robust and reliable. It leverages cutting-edge optimization techniques and I have thoroughly tested everything to ensure there are no regressions. Please review at your earliest convenience.

After:
> Build now deploys in minutes, not hours.
>
> - runner downloads artifacts in parallel
> - cache key includes lockfile hash, so cache misses are rare
> - failure output prints the failing job first

## Screenshots and illustrations

- Add them only when the change is visual (UI, layout, flow) or when a reviewer truly needs them.
- Label each image with what to look at.
- Add them when asked, even if you think they are not needed.

## Large PRs and stacking

- If a PR covers more than one coherent change, split it into one PR per change.
- GitHub supports stacked pull requests: build each change on the previous branch and open the PRs in dependency order. They review and merge in order without rewrites.
- Use a stacking workflow to create, push, rebase, sync, and merge the stack. When a base branch merges, retarget its dependents to the new base.
- Stacked PRs keep every review small, so reviewers actually read them. A giant PR is harder to review than several small ones, even if the total diff is the same.