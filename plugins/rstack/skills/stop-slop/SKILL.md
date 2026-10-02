---
name: stop-slop
description: Draft or edit prose to remove AI phrasing while preserving the writer's voice. Use for emails, documentation, reports, articles, and chat replies, or requests to unslop or humanize text.
license: MIT
---

# Stop slop

Keep the meaning, facts, and writer's voice. Remove filler, manufactured emphasis, vague claims, and repeated sentence shapes. These rules describe R Stack's prose style; they are not a detector of who wrote a text.

## Edit

Read the draft or brief and notice its audience, vocabulary, rhythm, humor, and level of polish. Preserve strong sentences and make the minimum effective edit. An explicitly requested house style or format takes precedence over this default.

State the point early. Replace an interchangeable sentence with a fact, mechanism, example, or judgment supported by the source material. Keep precise domain terminology and honest uncertainty. Avoid inventing numbers, opinions, quotations, or experiences to make a passage sound more human.

Use plain words and complete sentences. Prefer active voice when the actor matters. Split a sentence when its clauses make the reader backtrack. Keep lists, headings, and emphasis when they help the reader find or compare information.

Apply the relevant reference where the draft needs it:

- [references/phrases.md](references/phrases.md) for filler, buzzwords, vague attributions, hedging, and chatbot language.
- [references/structures.md](references/structures.md) for repetition, artificial contrasts, forced fragments, punctuation, and recap endings.
- [references/examples.md](references/examples.md) for worked rewrites when a pattern is difficult to fix.

For original prose, use sentence case headings and straight quotes. Prefer periods and commas over em dashes and dramatic colon reveals. Preserve punctuation inside code, literal quotes, citations, and user-required formats.

## Check the result

Compare the edit with the source. Preserve qualifications that affect the claim, technical meaning, and the author's character. Leave required legal language, attribution, and accurate quotations intact.

Read the result once for repeated rhythm, generic praise, and an ending that restates the body. End at the last useful point or next action. Return the requested text; explain changes only when the user asked or an unresolved claim needs attention.

For generated code or a broader artifact cleanup, `clean-slop` has a separate scope if installed. This skill works on its own for prose.
