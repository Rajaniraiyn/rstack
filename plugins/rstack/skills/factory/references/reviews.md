# Reviews

Review the worker's artifact against its original brief and a fixed base commit. A different harness or model can add another perspective; it does not guarantee correctness. If only one route is available, run a separate review pass and report that limitation.

## Review contract

Give the reviewer the brief, diff or commits, relevant source, and check results. Ask for findings with file locations, the concrete failure, and evidence. Review correctness, regressions, missing validation, and scope drift. Keep stylistic preferences separate from defects.

Enforce read-only execution using the supported sandbox or tool permissions. Use [harnesses.md](harnesses.md) to resolve the current commands. Inspect the review output yourself; process exit zero is not an approval of the code.

## Repair loop

Fix confirmed defects within the task's scope. Run the affected checks and review the changed area again. The worker brief sets the retry and budget limits; stop and report unresolved findings when either limit is reached. Avoid repeating a full review after an unrelated wording edit or when no new concern remains.

Before integration, run the required checks on the combined changes. Worker checks alone do not cover interactions between branches. For consequential changes, include the failure modes and the evidence that addresses them in the handoff.

## Handoff

Report completed outcomes, branch or worktree, checks, review findings, unresolved concerns, and known cost. Link the local artifact, or a PR when its creation was authorized. Publishing a transcript can expose task data and requires the user's request.
