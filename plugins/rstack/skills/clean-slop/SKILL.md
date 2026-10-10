---
name: clean-slop
description: Removes generated clutter from code diffs, documents, website copy, and designs while preserving behavior and meaning. Use for artifact cleanup or a de-slop pass.
license: MIT
---

# Clean slop

Remove unnecessary material while preserving behavior, meaning, and the project's style. For prose drafting and sentence-level editing, use `stop-slop` if installed.

Before adding, merging, or removing tests, assess coverage and failure detection with `test` if installed or the project's testing workflow. Do not delete a test because its setup looks repetitive.

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

Cut unsupported claims or flag them for the user. Do not invent statistics, quotes, logos, or testimonials.

Keep behavior unchanged. Report a discovered bug separately unless the user's task also authorizes fixing it. Run the repository checks relevant to code changes. For visual changes, inspect the affected view at the relevant sizes. Review the final diff for accidental scope growth.

Report what changed, what was checked, and any unresolved issue. Do not expand cleanup into a general review, dependency upgrade, redesign, or PR split unless requested.
