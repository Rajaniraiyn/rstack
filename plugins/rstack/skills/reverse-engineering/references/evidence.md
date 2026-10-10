# Evidence and specifications

Read this for format/protocol recovery, comparisons, reimplementation, or an investigation that needs retained evidence.

## Keep claims traceable

Use a compact ledger when several findings need reconciliation. For each claim record:

- Target digest/build and the question answered.
- Observation, inference, or unknown, with a reason for the confidence.
- Source file and line, byte offset/range, function address and module mapping, capture record, or tool evidence ID.
- Tool/version, relevant options, input/state, and coverage limits.
- Supporting and contradicting evidence, and the next discriminating check if unresolved.

Keep original evidence separate from summaries and redacted exports. Do not label shell output as REA Evidence. Session-local IDs need retained records or an exported bundle for later use; an ID alone is not a portable citation. Truncated output is incomplete evidence. Page or export existing results rather than rerunning expensive analysis.

Negative conclusions need a search boundary. "No reference in these decoded methods" does not mean "never called." Incomplete extraction, unresolved indirect calls, missing network bodies, and unsupported formats remain explicit unknowns.

## File formats and protocols

Start from caller-supplied sample files or saved traffic. Preserve producer, timestamp when relevant, original ordinal, direction, byte range, and digest. Treat HAR URLs as historical data; do not fetch or replay them automatically. Redact cookies, authorization headers, tokens, and personal payloads before exposing captures to a model or report.

Determine framing before assigning field meanings. Distinguish transport boundaries from message boundaries and stored representation from decoded content. Infer length, endian order, signedness, version, checksum, compression, and encoding using asymmetric samples or controlled changes. One captured value cannot establish a general range or formula.

Specify request/response relationships, state transitions, retries, errors, optional fields, and unknown opcodes only as far as the evidence supports. Encrypted payloads and omitted bodies do not reveal their contents. Decryption needs authorized keys and a permitted method, not an access-control workaround.

For bytecode interfaces such as EVM, distinguish dispatch selectors and static argument candidates from source-level names and executed chain behavior. Offline analysis does not authorize a chain query, transaction, or wallet interaction.

## Reconstruction contract

Describe inputs, outputs, state, preconditions, failure behavior, and observable side effects. Include numeric widths, overflow/truncation, layout/alignment, ordering, timing tolerances, and platform dependencies when they affect compatibility. Mark every unconfirmed assumption rather than making the specification silently stricter than the observations.

Compare the reconstructed implementation against independent observations of the original using relevant normal, asymmetric, boundary, error, and stateful cases. Control environment differences and nondeterminism. Record mismatches and permitted tolerances. Behavioral agreement on finite cases, instruction similarity, and byte-identical compilation are different claims; say which one was tested.

Use the project's testing workflow for test design and regression selection.
