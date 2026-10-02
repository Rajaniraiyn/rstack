# Formal models and Lean

Use formal modeling when a small, consequential rule is hard to establish through examples: accounting, permission transitions, parsers, retry/idempotency logic, bounded arithmetic, or concurrent protocols. Start with the smallest useful boundary. Lean is optional tooling; keep ordinary implementation tests and runtime checks.

## Establish the specification first

Identify the authoritative specification: an agreed user requirement, protocol, repository contract, or reviewed design. State inputs, outputs, permitted errors, state transitions, and intended guarantees in plain language. Separate required behavior from observations of the current code; a buggy implementation cannot define its own expected result.

When that existing specification settles the behavior, proceed without requesting the same approval again. When a new model introduces unresolved semantics, show the concrete choices and examples to the user and obtain confirmation before treating dependent proofs or behavior-changing fixes as authoritative. Continue independent reproduction and tooling inspection while clarification is pending. Label speculative models as exploratory.

Give the model extra review before spending time on tactics. Keep the reviewed statement stable while developing its proof; never change preconditions, definitions, or quantifiers merely to make the theorem pass. A second review should check the formal statement against the agreed examples and excluded cases.

## Check fidelity and useful obligations

Map each modeled field and transition to the implementation boundary. Review:

- Reachability and vacuity: exhibit valid initial states and interesting reachable transitions. Contradictory preconditions or an empty event set can make a theorem meaningless. An assumption that already contains the desired guarantee proves little.
- Arithmetic: distinguish unbounded `Nat`/`Int` from machine widths, wraparound, checked overflow, signed conversion, truncating natural subtraction, division by zero, floating-point rounding, and serialization. Lean's fixed-width types use bitvector models; choose the semantics of the actual implementation. See [natural numbers](https://lean-lang.org/doc/reference/latest/Basic-Types/Natural-Numbers/) and [fixed-precision integers](https://lean-lang.org/doc/reference/latest/Basic-Types/Fixed-Precision-Integers/).
- Environment: include invalid input, authorization context, exceptions, cancellation, persistence boundaries, crashes, and resource bounds when they affect the guarantee. Write omissions explicitly.
- Concurrency: preserve permitted interleavings, duplicate/reordered events, partial failure, and nondeterminism. A sequential happy path does not model a concurrent service.
- Safety and progress: prove initial validity and preservation under every allowed transition. Treat termination, eventual delivery, fairness, and liveness as separate obligations with explicit environment assumptions.

Check known positive and negative examples against the model. Deliberately perturb a transition or postcondition and ensure the obligations notice the defect. Small exhaustive exploration or an executable reference model can expose specification mistakes before proof work; bounded exploration is evidence only for its stated bounds. A failed tactic alone is not a counterexample.

## Validate the proof and its trust boundary

Use the repository's pinned `lean-toolchain`, dependency manifest, and build targets. Record the revision and tool versions; avoid silently updating dependencies. Inspect local help before version-sensitive commands. Typical project commands are:

```sh
lake env lean --version
lake --help
lake build
lake env lean Models/Invariant.lean
```

Replace the file with the actual module. Ensure every claimed proof is included in a checked target. Preserve diagnostics: build success may coexist with incomplete-proof warnings. Lake manages workspace dependencies and build configuration; see its [official reference](https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/).

Inspect `#print axioms Namespace.theoremName` for every claimed guarantee, including transitive dependencies. Reject `sorryAx`, unfinished proofs, and unexplained custom axioms. Ordinary Lean axioms such as `propext`, `Classical.choice`, and `Quot.sound` are distinct from assumptions invented for this model. Native-evaluation axioms enlarge the trusted computing base; report them and check the pinned version's behavior. Text searches for `sorry` alone cannot establish completeness. See [Lean's axiom reference](https://lean-lang.org/doc/reference/latest/Axioms/).

Keep kernel checking enabled. Inspect imported definitions, notation, and instances for changed meanings. Lean tactics and build code can execute actions; inspect untrusted dependencies and generated metaprograms before building, and isolate untrusted proof execution from credentials and the working project. For stronger assurance, use the installed toolchain's `lean4checker --fresh` workflow; for high-risk or untrusted proof submissions, consider a separately reviewed challenge and supported `lake comparator` external-checker workflow. These checks do not validate the intended meaning of a theorem. Follow the version-specific [proof validation guide](https://lean-lang.org/doc/reference/latest/ValidatingProofs/).

## Turn model findings into local bug evidence

For a suspected violation, minimize the input or event trace and replay it against the real implementation. Compare observable outputs and state with the reference model; retain serialization, overflow, and failure semantics in that adapter. Distinguish an implementation bug from a mistaken model, an invalid input assumption, or an unmapped integration behavior.

When a fix is authorized, repair the implementation and keep the smallest durable regression plus any useful model obligation. Recheck both the proof and the affected runtime boundary. Report the exact property, assumptions, checked commands, local counterexample, and remaining mapping gaps. A proof about an abstraction establishes its stated theorem; proving production refinement requires an additional checked correspondence to the actual implementation.
