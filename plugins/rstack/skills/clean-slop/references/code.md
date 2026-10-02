# Code cleanup

Remove unnecessary code while preserving the observable contract. Inspect each candidate in its callers and runtime context; generated appearance alone does not establish that it is redundant.

## Comments and diagnostics

Remove comments that merely narrate the adjacent code and obsolete commented-out implementations. Keep non-obvious reasons, workarounds, examples used as documentation, and required attribution or license notices. Preserve established section markers when they help navigation.

Remove temporary debug output when it is outside the project's logging contract. Keep operational diagnostics, audit events, and CLI output that users or automation rely on. Check whether a logger evaluates arguments with side effects before deleting a call.

## Checks and types

Remove a defensive check only when an established invariant guarantees its condition. Static types do not validate data arriving from JSON, storage, plugins, FFI, or network boundaries. Optional chaining on nested data is not redundant merely because it repeats.

Keep exception handling that translates errors, performs cleanup, retries, or protects a boundary. Check the library's actual failure modes before removing a catch. A default is redundant only when omission gives the same behavior, including null handling and version compatibility.

Replace a type escape with the correct type or validated narrowing. Avoid replacing `any` or a non-null assertion with another unchecked cast. Preserve intentional typing of dynamic data and public compatibility constraints.

## Structure

Simplify nesting when an early return preserves evaluation order, cleanup, and error behavior. Inline a single-use helper only when its name and boundary do not improve comprehension or isolate a dependency.

An `async` function returns a promise and turns thrown exceptions into rejections even when it has no `await`. Remove `async` only when callers and the public contract permit that change. Replacing local code with a library call also requires matching edge cases, side effects, and dependency constraints.

Remove unused code after checking references outside the file. Public exports, reflection, plugin registries, generated consumers, and dependency injection can hide usage from a text search. Treat an uncertain export as a question to resolve, not dead code.

Consolidate duplication when the blocks represent the same behavior and should change together. Similar-looking code for separate contracts can stay separate. Preserve measured performance work and compatibility paths still required by supported targets.

## Verify

Match the project's naming, formatting, and error conventions. Name a literal when the name explains its role; avoid constants that merely repeat a value.

Inspect the diff for changes to return types, exceptions, output, resource lifecycle, and public interfaces. Run the checks that cover any behavior touched by the cleanup. Test selection and removing duplicate coverage need a separate assessment of protected behavior and failure sensitivity.
