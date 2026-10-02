---
name: clean-slop
description: Remove unnecessary generated material from a scoped code diff, document, website copy, or design while preserving behavior and meaning. Use for artifact cleanup or a de-slop pass. Test-suite coverage and deduplication, general correctness, and security audits are separate workflows.
license: MIT
---

# Clean slop

Remove unnecessary material while preserving behavior, meaning, and the project's style. For prose drafting and sentence-level editing, use `stop-slop` if installed; the references here also work on their own.

Cleaning wording or redundant code inside a test fits this scope. Deciding which tests to add, merge, or remove requires coverage and failure-detection evidence; use `test` if installed, or assess those behaviors directly. Do not delete a test because its setup looks repetitive.

## Establish scope

Identify the artifact and the baseline before editing. Use the user's selected diff or revision. Otherwise inspect the repository's default branch and merge base rather than assuming `main`. Include working changes only when they are part of the request. For documents and design, use the brief and nearby examples.

Choose the relevant reference; do not load every mode:

| Artifact | Read | Focus |
| --- | --- | --- |
| Code diff | [references/code.md](references/code.md) | Unnecessary comments, redundant checks, type escapes, dead code, premature abstraction |
| Commit or PR | [references/commits-and-prs.md](references/commits-and-prs.md) | Concrete outcome, reviewer context, relevant validation |
| Document or report | [references/documents.md](references/documents.md) | Repetition, filler, formatting, unsupported claims |
| Website or marketing copy | [references/copy.md](references/copy.md) | Specific claims backed by real evidence |
| Design output | [references/design.md](references/design.md) | Brief, hierarchy, brand, usable layout |

## Edit and verify

Make the smallest useful cleanup. Match surrounding conventions. A single-use helper, popular font, gradient, or defensive check is a candidate to inspect, not proof of slop. Preserve boundary validation, accessibility, meaningful abstractions, and licensing notices.

Keep claims grounded in supplied evidence. Cut an unsupported claim or flag it for the user; replacing it with an invented statistic, quote, logo, or testimonial creates another problem.

Keep behavior unchanged. Report a discovered bug separately unless the user's task also authorizes fixing it. Run the repository checks relevant to code changes. For visual changes, inspect the affected view at the relevant sizes. Review the final diff for accidental scope growth.

Finish with a short account of what changed, what was checked, and any unresolved issue. A general review, dependency upgrade, redesign, or PR split needs its own task scope.
