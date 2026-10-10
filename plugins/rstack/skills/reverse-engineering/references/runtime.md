# Runtime boundaries

Read this before launching, attaching, or interacting with a target. Use the host's browser, desktop, and device guidance where applicable; this reference does not replace its permissions.

## Prepare a bounded observation

Identify the selected executable, process, page, device, or endpoint and the exact scenario. Record the starting state, input, build identity, environment, permitted network access, output directory, deadline, and cleanup ownership. Keep existing authorization, but ask before a new effect outside it.

Run unknown or potentially hostile targets in a disposable environment with no personal credentials, mounted private directories, or uncontrolled egress. A container, debugger, PTY, emulator, or REA process capture is not by itself a security sandbox. If suitable isolation is unavailable, stay with static evidence and report the runtime gap.

Attaching a debugger can pause or change a process. Instrumentation, injected code, breakpoints, TLS interception, and debug ports have stronger effects than reading existing logs. Do not enable them under a passive-observation request. Avoid exposing an unauthenticated debugging endpoint beyond the intended local interface.

## Capture the discriminating event

Choose the smallest scenario where competing hypotheses predict different outputs. Record before state, action, after state, relevant logs or traffic, and timing. Repeat from a known state when caching, randomness, scheduling, or persistence could change the result.

For browsers and Electron, bind the selected page or renderer to its app and build. Prefer existing passive inspection for read-only requests. Even a DOM read or evaluation can invoke getters; do not assume arbitrary JavaScript evaluation is side-effect free. New interactions, navigation, downloads, or submissions must fit the user's scope.

For processes, capture argv, working directory, environment differences, stdin, stdout/stderr, exits, and relevant filesystem changes. Distinguish root-process exit from descendant termination. Avoid terminating an existing user process to reset a fixture.

For debugger observations, bind addresses to the loaded module and relocation map. Record thread, breakpoint, registers, and relevant memory with enough context to reproduce the finding. A branch not reached in one run remains unobserved, not dead code.

For devices and emulators, distinguish host simulation from physical execution. Preserve user data and account state. Hardware IO, firmware writes, destructive resets, and physical actuation need their own authorization and safe setup.

## Reconcile and clean up

Static evidence suggests possible behavior; runtime evidence establishes what happened under the recorded conditions. Explain mismatches using build identity, configuration, dynamic loading, state, or analysis gaps before claiming a contradiction is resolved.

Stop only launched processes, captures, debug endpoints, and disposable environments this run owns. Restore owned temporary settings when safe, preserve original artifacts and user sessions, and report resources whose cleanup could not be verified.
