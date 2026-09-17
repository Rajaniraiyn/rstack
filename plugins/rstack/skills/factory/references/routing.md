# Routing

Route each task to a harness, a model, and an effort level. The cheapest workable option wins; escalate only when the workhorse tier fails or the task is known-hard.

## Effort levels

Effort selects how much reasoning the model spends. Treat the scale as transitive across harnesses:

- `low`: mechanical edits, renames, boilerplate, simple factual answers.
- `medium`: normal implementation, tests, conventional refactors.
- `high`: architecture, tricky bugs, multi-step plans, reviews.
- `xhigh` / `max` / `ultracode` (Claude) or `max` (OpenCode `--variant`): frontier problems, long-horizon agent work.

Match the knob per harness: Claude Code `--effort`, OpenCode `--variant`, Codex reasoning via its model or profile settings, Amp and Copilot through their model and mode settings. Do not quote level names across harnesses; translate the intent.

Always-on thinking models (for example Claude Fable) cannot disable thinking, so they are wrong for high-volume cheap work even when their price is fine.

## Model tiers

The exact model list changes every few months. The tiers are the durable part:

- **Cheap tier**: high-volume, mechanical work. Haiku-class models, or the cheapest family member of the provider in use. Low effort. Good for bulk triage, summaries, renames.
- **Workhorse tier**: normal implementation. Sonnet-class models on Claude, the standard GPT model in the provider's harness (for example the GPT family served by Codex). Medium effort. This is the default for most tasks.
- **Frontier tier**: hard reasoning, long-horizon agentic work, adversarial review, rare bugs. Top models (Claude Fable 5.1, GPT-6 Astra, Opus-class) with high or max effort. Price per token is several times the workhorse tier, so use it only when the workhorse failed or the task is known-hard.

## Routing rules

1. Classify the task: mechanical, normal, or hard.
2. Assign the cheapest tier that can plausibly finish it.
3. Run. If the result is wrong, stuck, or the task turns out harder than classified, escalate one tier and rerun that step. Prefer forking the failed session at the higher tier where the harness supports it instead of restarting cold; see [subagents.md](subagents.md).
4. For work that has to be right (releases, security, user-facing copy), spend one extra tier up front: run the review gate from [reviews.md](reviews.md) with a different harness or model at high effort.
5. Parallelize independent tasks across worktrees so cheap models finish batches while one frontier model handles the hard core. See [worktrees.md](worktrees.md).

## Cost controls

- Set a dollar cap wherever the harness supports it (Claude Code `--max-budget-usd`; Codex and others via profiles or limits).
- Prefer cheap tier for the bulk of a batch; a few frontier calls should not dominate the bill.
- Re-run reduced: when a task fails, retry with the same or one tier higher, never max effort by default.
- Watch auto-compact and thinking budgets: long context pushes cost even on cheap models. Shorten the task text before escalating models.

## Escalation ladder example

Mechanical bugfix on an unfamiliar codebase:

1. Workhorse, medium effort, one worktree.
2. If diagnosis is wrong: frontier tier, high effort, same worktree.
3. If the fix is risky: add a review gate with a second harness at high effort before handing back.

Report the route you took and why, so the user sees the cost decision and can change the defaults.