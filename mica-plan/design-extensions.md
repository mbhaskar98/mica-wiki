---
tags: []
created: 2026-10-15
description: Infrastructure requirements and conditional architecture extensions triggered by measured reader bottlenecks or resource limits.
aliases:
  - Mica Design Extensions
  - design-extensions
---

# Implementation work and conditional design extensions

**Updated:** 2026-10-14. This document distinguishes completed implementation/studies from proposed infrastructure and conditional changes. Predicate-first execution is implemented and evaluated; this reconciliation makes no code change and runs no experiment. The [[evidence|evidence audit]] is the authority for what exists today; [[experiments|experiments.md]] defines the evidence that would justify further work.

**Recommendation.** Evaluate the credible existing contribution before adding mechanisms: Mica makes fine-grained pruning practical through its metadata organization and reader execution. First build the E01 granularity controls and the comparison support needed to establish S2 against the closest systems. The fact that individual indexing techniques have precedents is not a reason to add complexity. Extensions are warranted by measured limits in the intended workload, correctness or resource behavior; current evidence does not justify a distributed scheduler, a learned optimizer or a new format revision.

1. **Required to run the proposed studies, not claimed as novel**

| Work | Why it is needed | Concrete acceptance evidence |
|---|---|---|
| Metadata lifecycle instrumentation and benchmark caches | E03 must separate serialized bytes, parsed objects, reconstruction and query-private allocations. | Cold/warm-byte/reused-object tests show the intended state; accounted memory includes retained shared allocations and does not double-count them; both formats can reuse legitimate metadata. |
| Known-row retrieval adapters | E01 needs a discovery-free diagnostic with equal logical selection. Mica's public predicate scan is not a general take API. | Mapping handles variable row counts after page bisection, charges every format its own mapping/codec dependencies, and matches exact reference values. |
| Reader, sidecar and compatible-layout controls | E02a separates unchanged-file improvements, metadata organization and data rewriting before claiming an integrated-format advantage. | Hashes verify P0/P1/P2 data identity; common candidate intervals match; sidecar identity/fallback is correct; P3 boundaries and format conformance are checked when that variant is needed. |
| Dependency trace and candidate-manifest adapter | E02b identifies the residual cost of mapping, locating and decoding the same candidates. | All required locator/codec state remains charged; traces distinguish speculation from dependencies and CPU from elapsed overlap; the matched-candidate path and native path both return exact results. |
| Clean factorial controls | Old bundled ablations cannot identify individual mechanisms or interactions. | Explicit controls independently change membership availability and metadata loading; writer variants verify alignment versus independent boundaries. Every lane preserves exact outputs. |
| Cost and artifact schema | E01/E05 need candidate, metadata, mapping, I/O and decode attribution; every paper number needs provenance. | Raw event and result records reconcile with total bytes and declared overlap; profiling overhead is measured; archived results can be regenerated from preserved inputs/configuration. |
| Multi-query workload driver | E08 needs shared budgets, queueing, reuse and exact output beyond isolated runs. | Fixed offered-load schedule, bounded worker allocation, backlog/drop accounting and recorded memory residency; correctness survives concurrent execution and cancellation. |

Implement the P0/P1/P2/F pilot and dependency trace first. Build P3 only when a measured layout cost warrants it, before claiming that compatible data layouts cannot recover the advantage. Preserve source patches, manifests and conformance checks as study artifacts. These changes can live mostly in evaluation code. Do not describe the cache harness as a deployed Mica cache, or a research aligned-Parquet writer as a stock baseline. The main reader need only expose the minimum accurate counters and reusable-object boundaries necessary for fair experiments.

2. **If discovery work still scales badly, improve the measured representation**

Trigger: E05 shows that dense bitmap scans, repeated coarse scoring or materialized per-column plans dominate at fixed final candidate count. The target is the measured cost, not an absolute claim that total work depends only on survivors.

Possible changes include group-segmented bitmaps, immutable shared coarse summaries, incremental location/plan construction, or an additional summary level when the coarse layer itself is too large. Each is established in general form. The contribution would need to concern a new consequential interaction in this execution setting, not merely using a sparse bitset or another tree level.

Retain dense execution for dense candidates. Compare the current representation, a simple sparse list/run representation and the proposed hybrid. Test fixed-P/fixed-K/run-count cases, dispersed metadata reads, empty results, full scans and memory peaks. Require exact results and account for representation conversion. If the current term is small in realistic workloads, retain it and correct the complexity wording instead of implementing an unnecessary replacement.

3. **If refinement pays more than it saves, define a real decision problem**

Trigger: E01/E03/E04 show frequent and material losses caused by loading another fine summary or membership layer. Current thresholds are heuristics; they are not a calibrated latency optimizer.

A scoped extension would choose whether to refine a candidate region or read/filter its data. Inputs can include resident metadata status, remaining candidate intervals, physical metadata range count/bytes, projected bytes, codec dependencies and previous measured selectivity. Predictions must not use exact future survivors or untimed query-specific profiles. Estimate both extra metadata work and avoided data/decode work, including another dependency round.

Compare against always-refine, never-refine, the current fixed thresholds, and a simple calibrated cost rule before considering a more elaborate policy. An offline best-action oracle is a diagnostic bound, not an executable baseline. Test held-out predicates, reuse changes, another device and uncertain/correlated filters. Report decision regret and the cost of computing the decision, not only end-to-end gains.

Cost-based access-path selection is prior art. This extension strengthens the paper only if a specific unresolved decision and mechanism are established relative to that literature. A learned predictor or an “adaptive” label is not evidence of novelty. Keep correctness independent of the prediction: skipping a pruning index must fall back to exact data filtering, never infer absence of rows.

4. **Completed: predicate-first projection reads, retained as experimental**

This extension is implemented and its bounded study is complete. The decision and evidence report retains explicit experimental staging and empty-skip modes while rejecting default promotion. The execution guide records the tested guarantees and deferred production controls; it is not a mandate to finish exhaustive allocator accounting. Existing Arrow, ORC, ClickHouse, Lance and current DuckDB paths are direct precedents; neither staged reads nor a history-based selector is independently new.

The original trigger was avoidable projection work after exact filtering. That question has now been tested: explicit staging omits projection-page I/O for exact-empty pages, while combined-empty-skip isolates the decode-only shortcut. This is completed work, not a future implementation task.

The explicit two-stage path now reads predicate data, computes exact row selections, then fetches only necessary projection units. It must handle columns that are both predicates and outputs, partially selected pages, shared dictionaries, limits, ordering and output assembly. It introduces a dependency round and can reduce I/O parallelism. Keep the combined default. The measured dense grouped queries regress by about 19–23% under staging, so no automatic selection policy is adopted in this study.

Recorded validation covers exact outputs, stage barriers, issued bytes/requests, decode work, selected lifetimes/cancellation and complete-query latency. Time-to-first-batch, concurrent tails and strict public aggregate admission were not established. Retain the completed study and its losses; these deferred quantities are not retroactive completion blockers. Further implementation requires a concrete defect, invalid comparison or unmet original requirement. Automatic selection and pipelining remain deferred; no new implementation task is added here. Late materialization remains established prior work; the paper contribution here is the measured execution tradeoff.

5. **If shared boundaries are expensive, reconsider alignment honestly**

Trigger: E07's added unqueried string column substantially increases page count, metadata or compression cost for unchanged numeric queries, and the case is realistic for the intended workload. E05 must also measure whether alignment actually saves enough read-time work to justify that cost.

Possible responses are to choose a different page cap, limit the supported schema regime, or allow several physical fragments within a common logical row partition. The latter requires an explicit mapping between logical selection intervals and per-column fragments. It changes the contract and reintroduces translation; it must be compared with ORC, Lance and Vortex mechanisms that already separate logical rows from physical units.

Do not preserve shared page identity as a novelty claim if efficient independent boundaries perform as well. A simpler design can sharpen the paper around the metadata/reader choices that actually matter. A weak alignment result narrows that design claim without automatically defeating the fine-grained pruning contribution. Any format change needs versioning, exact cross-column selection tests, codec dependency accounting and storage/write-cost comparison. Do not implement it before measuring the tradeoff.

6. **If concurrency exposes unbounded resources, close the execution gap**

Trigger: E08 finds oversubscription, excessive outstanding I/O, retained result buffers or cancellation that fails to release work. Existing window/scan budgets do not prove an aggregate bound across concurrent requests.

Use engine-owned scheduling, shared admission accounting and backpressure to bound the specific resource. Verify that metadata, plans and output buffers are charged as well as I/O windows. Test cancellation during open, refinement, read and output delivery; ensure no use-after-free of outstanding I/O buffers and no false completion. Compare throughput and class-specific tails before calling the policy useful. This is system completeness work unless it establishes a new scheduling problem and solution.

7. **What not to add as a substitute for novelty**

Do not add cluster coordination, transactions, remote-object storage, arbitrary nested types, vector search or a learning component solely to look broader. Each would require its own workload, correctness and prior-art argument. Flat immutable files are a defensible boundary if the core result is consequential.

Do not invest in every conditional extension. Run the decisive gates, identify the cause that limits the target result, and choose the smallest design change that addresses it. Then repeat the relevant causal controls and prior-art comparison. Reconsider the strong-venue claim if the closest established organization already achieves the same practical result at comparable cost and no distinct systems insight remains. Familiar ingredients, portable implementation or additive performance effects alone do not warrant that conclusion.

---

## Vault Navigation & MoC Context

- [[Mica]]: Central Level 3 Project Hub for Mica paper notes and core concepts.
- [[README|Mica Plan Overview]]: Master roadmap and synthesis of the SOSP/OSDI research plan.
- [[storyline|Mica Storyline]]: Proposed SOSP/OSDI research storyline and core claims S1–S3.
- [[prior-art|Mica Prior Art]]: Primary-source positioning and novelty analysis.
- [[experiments|Mica Experiments]]: Comprehensive experimental campaign E00–E09.
- [[evidence|Mica Evidence]]: Implementation status audit and empirical evidence synthesis.
- [[stress-test|Mica Stress Test]]: Stress-test ledger and falsification criteria.

