# Reviews

Gate every handoff with a review pass from a different harness or model than the one that produced the work, run read-only, then hand back the final URL.

## Why a second pass

The writer's own harness shares its blind spots: the model that wrote the code tends to approve it. A reviewer from a different family (for example Codex reviewing Claude-written code, or a Claude frontier model reviewing Codex output) catches real defects and style drift the writer missed.

## Run the gate

1. Collect the artifact into a reviewable unit: a branch, a diff, a PR, or a directory.
2. Review with a different harness or model at high effort, read-only. Examples:

```sh
# Claude Code, read-only review of the current diff
claude -p "Review the diff against main for bugs and correctness. Read-only." \
  --model sonnet --effort high --allowedTools "Bash(git diff),Bash(git log),Read"

# Codex, read-only review in workspace
codex exec "Review the uncommitted changes for correctness, tests, and edge cases." \
  --sandbox read-only --ask-for-approval never -o review.txt

# OpenCode review with a different model family
opencode run "Review the current branch against main." -m openai/gpt-5.5#high

# Copilot with a dedicated review agent
copilot -p "review the current diff" --agent code-review
```

3. Fix what the review finds: run the fix in the same worktree, then re-run the gate until it passes.
4. For release-critical work, run a second gate with a frontier-tier model before final handoff.

## Review scope

- Correctness: does it do what the task said?
- Regressions and edge cases the task did not mention.
- Test coverage for changed behavior.
- Style and slop: apply the `clean-slop` skill to generated code and prose before the gate, so the reviewer is not the only guard.

## Guardrails

- Keep review passes read-only unless the user asked for autonomous fixing. A review that edits is no longer a review.
- Do not let the reviewer rewrite for taste. Flag, fix minimally, preserve the writer's ownership.
- Never skip the gate for work that touches money, releases, security, or user data. Those get the frontier-tier pass.

## Hand back the final URL

End with the link the user can act on:

- The pull request, for code.
- A share link from the session (the harness's session share command) for long-running or review-output sessions.
- The review report file for analysis-only runs.

Summarize in one paragraph: what shipped, on which branch or worktree, what the gate found, and the cost tier used. That is the factory's accounting back to the user.