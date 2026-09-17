---
name: clean-slop
description: Remove AI slop from code, diffs, documents, copy, and design output. Use when reviewing a branch, generated code, or produced artifacts to strip AI-generated cruft and match human style.
---

# Clean Slop

Remove AI-generated slop from an artifact without changing what it does or says.

## When to use

Checking a branch against main, reviewing generated code, documents, reports, website copy, or design output. Use after most non-trivial changes.

## Process

1. Establish the baseline. For code, the diff against main. For text and design, the project's existing style and the brief.
2. Scan the artifact against the patterns below and in the reference files.
3. Fix: remove cruft, keep behavior and meaning identical.
4. Self-audit the result. Does it look like a person made it?
5. Report what you changed in 1-3 sentences.

## Guardrails

- Keep behavior unchanged unless you are fixing a clear bug.
- Make minimal, focused edits, not broad rewrites.
- Match the surrounding file, codebase, or brand style.
- Never invent facts, metrics, quotes, logos, or testimonials to replace slop. Use a labeled placeholder or cut the element.
- Prefer the plainest correct implementation.

## Code

- Extra comments that are unnecessary or inconsistent with local style.
- Defensive checks and try/catch blocks that are abnormal for trusted code paths.
- Casts to `any` used only to bypass type issues.
- Deeply nested code that should be simplified with early returns.
- Unused variables, imports, parameters, and dead code.
- Over-abstraction with a single call site, and reimplemented library functions.
- Style drift: naming, spacing, and error handling that don't match the file.

See [references/code.md](references/code.md) for the full list.

## Documents and reports

- Restated sections: "as we saw above", a conclusion that repeats the body.
- Stone signs showing: bold-first bullets, emoji headings, headers over tiny sections.
- Filler transitions: "it's worth noting", "importantly", "in conclusion".
- Punctuation tells: em dashes, colon reveals, curly quotes.
- Generic structure: every section the same shape.

See [references/documents.md](references/documents.md).

## Copy and website content

- Vague claims without numbers or sources: "trusted by thousands".
- Fabricated metrics, logos, testimonials, and case-study counts.
- Buzzwords and fake-strong verbs: leverage, seamless, serves as.
- Patronizing analogies: "think of it as", "it's like a".
- Stacked tricolons and punchy fragments for manufactured emphasis.
- Copy that could sit unchanged on any competitor's site.

See [references/copy.md](references/copy.md).

## Design

- The gradient hero with white centered text.
- One default font (Inter, Roboto, Open Sans) doing display and body work.
- The icon-tile card grid as the default section shape.
- Symmetric everything with no layout bias.
- Fake browser chrome and device frames.
- Fabricated metrics, logos, and testimonials.

See [references/design.md](references/design.md).

## Reference files

- [references/code.md](references/code.md)
- [references/documents.md](references/documents.md)
- [references/copy.md](references/copy.md)
- [references/design.md](references/design.md)