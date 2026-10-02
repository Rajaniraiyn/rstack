# Evaluate a skill

Validate the structure, then the decisions and artifacts. A valid frontmatter block and resolvable links do not establish good task behavior.

## Routing cases

Use realistic requests rather than keyword-only prompts:

- A clear match using the user's natural wording.
- A match phrased without the skill name.
- A nearby request outside scope.
- A multi-skill request with separable outcomes.
- An explicit invocation for a skill whose host policy disables automatic selection.

Record expected selection and the reason. Evaluate automatic selection on a host that actually implements the policy. A manual reading cannot prove host routing reliability.

## Task cases

Give the executing agent the request, installed skill directory, and minimum input files. State the permitted workspace and side effects. Use temporary directories for generated artifacts. Test missing prerequisites and changed user preferences where these affect a branch.

Judge observable results: factual claims preserved, correct artifact, no unexpected dependency or publishing, checks run, resources available after standalone install. Avoid assertions about exact headings, wording, or tool-call order unless they are part of the required output contract.

For a complex or consequential workflow, an independent execution adds confidence when delegation and cost are authorized. Do not give the evaluator the intended answer. Otherwise perform an in-session walkthrough and label it as such. No evaluation should silently provision credentials, call a paid API, or modify a live system.

## Compare revisions

When a performance or quality claim matters, run the same cases with the previous and revised skill in isolated directories. Record outputs, failures, elapsed time, tool use, and actual cost if available. Review the artifacts against the same criteria. Add repeated runs only when variance would change the decision.

Keep failed cases and repair the cause. Prefer a structural fix or a narrow instruction over a universal rule derived from one example. Report whether evidence came from static checks, a manual walkthrough, or actual host execution.
