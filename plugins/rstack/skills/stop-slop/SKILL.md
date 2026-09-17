---
name: stop-slop
description: Cut AI tells from anything you write or say. Use when drafting, editing, or reviewing text to remove predictable AI patterns and keep the writer's voice.
---

# Stop Slop

Edit text to remove AI patterns. Use when drafting, editing, or reviewing anything you write or say, from chat replies and emails to docs and reports.

When the text lives inside code (comments, docstrings, error messages, commit messages) or your output includes code, pair this with the `clean-slop` skill: it owns the code-side patterns.

## Process

1. Scan for the patterns below and in the reference files.
2. Rewrite. Keep the meaning and the writer's voice.
3. Self-audit: "What makes this read like AI?" Fix the rest.

## Patterns to detect and fix

### Content

- **Superficial -ing phrases.** "highlighting...", "underscoring...", "reflecting...", "showcasing...". Delete or expand with the real consequence.
- **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete.
- **Vague declaratives.** "The implications are significant". Name the specific implication or drop it.
- **Sycophantic tone.** "Great question! You're absolutely right!" Respond directly instead.
- **Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!". Remove.

### Language

- **AI vocabulary.** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant, leverage, utilize, seamless, robust (vague). Replace with plain words.
- **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Just say "is" or "has".
- **Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". "It is important to note that" gets deleted.
- **Excessive hedging.** "could potentially possibly be argued that it might" becomes "may".
- **Empty adverbs.** "significantly", "crucially", "importantly", "notably", "simply", "just", "actually", "truly". Cut them when they add nothing; keep them when they carry real emphasis or uncertainty.

### Style

- **Em dashes.** Avoid entirely. Use periods or commas only (no parentheses, no en dashes, no hyphen-as-dash substitutes). If a thought needs separation, end the sentence or use a comma.
- **Colon overuse.** Colons are fine before a list or example. Not as mid-sentence connectors. No "colon reveals" (a noun phrase, a colon, then a lowercase dramatic reveal).
- **Bold-first bullets.** Every list item starting with a bolded keyword. Remove the bold leads.
- **Title case headings.** Use sentence case.
- **Decorative emojis.** Remove from headings and bullets.
- **Curly quotes.** Replace with straight quotes.
- **Rule of three.** Forcing ideas into groups of three. Use the natural number. One tricolon is fine; stacked tricolons are not.
- **Binary contrasts.** "It's not X, it's Y." State Y directly.
- **Negative listings.** "Not a X. Not a Y. A Z." Just say Z.
- **Synonym cycling.** Protagonist, main character, central figure, hero in one paragraph. Pick one and repeat it.
- **False ranges.** "from X to Y" where X and Y aren't on a meaningful scale. List topics directly.
- **Self-posed rhetorical questions.** "The result? Devastating." Fold into a statement.
- **Dramatic fragments.** "X. And Y. And Z." Use complete sentences.
- **Meta-joiners.** "In this section, we'll explore...", "The rest of this essay...", "Let's dive in". Delete and let the text move.
- **Fake-profound kickers.** The final "deep" line that turns the point into a metaphor or mic-drop. Delete it. End on the clearest concrete sentence.
- **Summary-recap endings.** "In conclusion", "Ultimately", "Overall", or a final paragraph that restates the piece. End on the last concrete point or next action.

### Jargon

- **Abstract metaphor nouns.** Substrate, wedge, vector, locus, vantage, nexus, primitive (as noun), harness (as metaphor), surface (as in "API surface"), bedrock, scaffolding (as metaphor), modality, paradigm, gold-plating, ratchet (as metaphor), evacuate (for moving code), endgame, north star, flywheel. These read as technical but usually have a plainer concrete word. "Substrate" becomes "base". "Wedge in" becomes "add". "Vector" becomes "way" or "method". "Endgame" becomes "the last phase". Pick the concrete word.
- **Business buzzwords.** Ecosystem (abstract), landscape, synergy, circle back, move the needle, low-hanging fruit, best-in-class, world-class, mission-critical, bandwidth, touch base. Cut or name the actual thing.

### Plain speech

- **Say what it does, not how it feels.** "the database stays close at hand", "SQL you can read" name a feeling. The fix names the mechanism or a number: "`.toSQL()` returns the exact string sent to the database", "a column rename fails the build". Ask what the sentence tells the reader to do or know, then write that. If you can't restate it as a concrete instruction, fact, or number, cut it. One more check: if the sentence could appear unchanged in another project's docs, it says nothing about this one. Cut it.
- **Use the portability test.** A sentence that could move unchanged to another person, company, or product is probably filler. Replace it with a fact, example, mechanism, or judgment specific to this subject.
- **Shorten or split dense sentences.** If the reader has to backtrack to parse a sentence, break it in two or drop clauses. One idea per sentence.
- **Active voice.** Prefer it. "queries are validated" becomes "the compiler validates queries". Passive is fine only when the actor is unknown or genuinely doesn't matter.
- **Cut adverbs, or use a stronger verb.** "runs quickly" becomes "is fast" or the number. "significantly improves" becomes the measured delta. An adverb propping up a weak verb means the verb is wrong.
- **Over-compression.** Dropped articles, verbless fragments, symbol-speak. "Parser rejects bad date → exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing." Write whole sentences.

## Keep the writer's voice

- Notice the draft's vocabulary, cadence, bluntness, humor, uncertainty, digressions, and level of polish. Keep the traits that feel personal.
- Make the minimum effective edit. Leave strong human sentences alone.
- Keep the user's meaning. Don't invent claims, examples, stats, quotes, or opinions. If something is unclear, ask.
- Preserve useful edge and character: strong opinions, blunt language, humor, honest admissions. Don't replace them with safer or more professional wording.
- Open it up, don't dumb it down. Keep the substance, nuance, and precision. Strip only what makes it hard to read.

## Reference files

- [references/phrases.md](references/phrases.md): full list of words and phrases to cut or replace.
- [references/structures.md](references/structures.md): sentence and paragraph shapes to break, with fixes.
- [references/examples.md](references/examples.md): before and after transforms.