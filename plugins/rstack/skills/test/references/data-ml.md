# Data pipelines, numerical code, ML, and AI workflows

## Data and analytics

Use representative small fixtures with independent expected records or aggregates. Test schema/types, nulls, duplicates, ordering, encoding, timezone/DST, currency/units, and referential rules where relevant. Validate values and provenance, not just row count or a successful job exit. [dbt data tests](https://docs.getdbt.com/docs/build/data-tests) are one route for declared SQL models.

Exercise incremental versus full rebuild, rerun/idempotency, late or corrected data, checkpoint/restart, partial writes, and migration from a prior format. Keep source/input and output partitions isolated per run. Match the actual database/query engine when collation, transactions, types, or SQL dialect matters. An in-memory result doesn't establish warehouse behavior.

For scientific/numerical work, use known solutions, dimensional checks, conservation or other justified invariants, boundary conditions, and an independent reference. Define absolute/relative tolerance based on the algorithm and input scale. Record precision, backend, seeds, and conditioning; rounding until results match hides instability. Compare CPU/GPU and optimized implementations when the change depends on them.

## ML and inference

Pin model artifact/hash, tokenizer/preprocessing, dataset revision, runtime/provider, precision, and relevant seeds. Check input validation, shape/dtype, batching, output meaning, and error handling. Use held-out evaluation cases with meaningful slices and fixed metrics/acceptance criteria. Avoid training/evaluation leakage and judging only an average that hides failed classes. Split correlated samples by the relevant entity/time boundary; randomly splitting rows can leak one subject or event into both sets.

Reproducibility differs by hardware, kernels, and parallelism. Compare semantic metrics and justified numerical tolerances rather than requiring identical bytes everywhere. Verify quantized or optimized models against an appropriate reference and representative inputs. [ONNX Runtime APIs](https://onnxruntime.ai/docs/api/python/api_summary.html) and [quantization guidance](https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html) describe one execution route.

Measure cold/warm latency, throughput under the intended batching/concurrency, memory, and timeout/OOM handling when relevant. Keep evaluation quality separate from serving integration and deployed-performance evidence.

## AI agents and nondeterministic workflows

Evaluate observable task success, tool arguments/effects, schema validity, boundary adherence, cancellation, recovery, and resource use. Stub tool responses for deterministic cases, then run a small authorized real integration set. Include malformed tool results, unavailable tools, repeated actions, and untrusted content where they affect the workflow. Do not send test messages/payments or use paid model APIs merely to create coverage without authorization.

Separate deterministic orchestration checks from model-quality evaluations. Use multiple justified runs for variable outcomes, preserve failing traces, and report sample size and actual cost when known. Keep a held-out set when tuning prompts, tools, or judge rubrics; repeated tuning against the same cases can overfit the evaluation. An evaluator model is fallible; combine rubrics and programmatic checks with review of consequential outputs. Synthetic computer tasks such as [Cua Bench](https://cua.ai/docs/cua-bench) provide controlled evidence, not proof of every real desktop task.
