# Artifact analysis

Read this for native or managed code, archives, resources, and firmware. Use a parser appropriate to the format before assuming an executable architecture.

## Inventory without execution

Record file size, digest, format, architecture, endianness, and build identifiers when present. Inspect headers, sections, imports/exports, symbols, relocations, and resources. Stripped symbols and strings suggest search seeds; their absence is not evidence that a feature does not exist.

List archive members before extracting. Check declared and expanded sizes, entry counts, nesting depth, absolute paths, traversal, links, and duplicate names. Use a new owned output directory with limits supported by the selected extractor. Parser or extractor subprocesses are not automatically safe for hostile input. Do not run package installation hooks, open an app, or load a library to identify it.

Inspect configuration and resources alongside code when they affect the question. A bundled URL is not proof that a runtime contacts it. Do not fetch it automatically. Preserve opaque payloads as byte ranges with digests rather than fabricating a decoded meaning.

## Native code

Select the actual ISA, ABI, and loader mapping. Distinguish file offsets, relative virtual addresses, analysis addresses, and relocated runtime addresses. Use imports, exports, string references, or a known call as an entry point; follow only the relevant callers and callees.

Recover argument roles and data flow before giving anonymous functions confident names. Check calling convention, signedness, integer width, overflow, floating-point conversion, packing, alignment, and compiler transformations where they change the result. Pseudocode can conceal flags, truncation, aliasing, or indirect calls. Corroborate those claims with assembly and referenced data.

Record the engine/version and analysis options. Renaming symbols in an owned analysis database can aid investigation but is not evidence from the original binary. Preserve existing user databases; do not save over them or close their GUI sessions as cleanup.

## Managed code and mixed packages

For .NET, inspect assembly metadata, method bodies, resources, and declared P/Invoke dependencies. Reflection, generated code, unresolved assemblies, and dynamic dispatch can leave gaps. A native import declaration does not show that the call executed. NativeAOT is a native-code route, not a promise of recoverable managed source.

For JVM/DEX and mixed packages, map the manifest or metadata entry point through managed calls and any native boundary. Recover one requested method or feature instead of dumping every class. An obfuscated name or a decompilation failure should remain an unknown, not an invented implementation.

## Firmware

Separate container regions, compressed filesystems, executable payloads, configuration, and signatures. Record each extracted member's parent digest and offset when the tool exposes them. Entropy and signature matches are candidates until format parsing corroborates them.

Use supplied images and local static tooling first. Emulation can need a matching architecture, memory map, peripherals, and boot state. Record assumptions and unsupported behavior. Do not flash hardware, probe a connected device, or drive physical actuators without authorization for that specific action.
