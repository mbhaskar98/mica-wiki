---
tags: []
created: 2026-10-15
description: Comprehensive experimental campaign E00-E09 evaluating granularity sweeps, baseline comparisons, metadata lifecycle, and engine queries.
aliases:
  - Mica Experiments
  - experiments
---

# Experiments for the Mica storyline

**Updated:** 2026-10-14. **Status:** mixed completed evidence and proposed broader studies. The bounded predicate-first implementation and evaluation completed on 2026-09-29; this documentation reconciliation runs no experiments. The matrix below distinguishes completed substudies from open E00–E09 requirements. All measurements retain their recorded settings. Claims S1–S3 are defined in [[storyline|storyline.md]]; source/artifact availability is recorded in [[evidence|evidence.md]].

1. **Run the experiments that can change the thesis first**

| ID | Question | Claim | Reuse status | Priority and paper role |
|---|---|---|---|---|
| E00 | Are configurations, semantics and evidence trustworthy? | All | Extend exact-output harness and artifact checks. | First; blocks publication of other results. |
| E01 | Does Mica make finer pruning economical, and why? | S1, S2 | Reuse Parquet sweep/profilers and eager-metadata control; rerun matched lanes. | First contribution pilot and motivation. |
| E02 | Is the benefit beyond established indexing and existing layouts? | S2 | Reuse Parquet/Lance infrastructure; add alternatives and interventions. | Early novelty decision; main paper. |
| E03 | Does the benefit survive realistic metadata reuse? | S1, S2 | New controlled cache/lifecycle study; old warm-cache experiment is insufficient. | Early deployment decision; main paper. |
| E04 | Which distributions preserve useful physical pruning? | S1, S3 | Completed clustered/dispersed execution control; extend locality/correlation coverage. | Early scope decision; main boundary plot. |
| E05 | Which mechanism and interaction cause the gain? | S1, S2, S3 | Staging-mode study complete; metadata/alignment factorial remains open. | Main explanation after E02/E03 screening. |
| E06 | Does it improve complete engine queries? | S3 | Completed scoped staging engine study plus historical cohort; broader evaluation remains open. | Main end-to-end result. |
| E07 | What storage, indexing and writing cost purchases the benefit? | S2, S3 | Reuse size analyzer and writer; add portfolio and stress sweeps. | Main tradeoff and design-cost evidence. |
| E08 | Does the reader remain useful with concurrency and resource limits? | S3 | Reuse execution budgets; add service workload driver. | Systems robustness and throughput/tail plot. |
| E09 | How much depends on device, I/O API and request policy? | S1, S3 | Replace old motivation control; reuse cap-sweep infrastructure. | Hardware boundary; promote only a demonstrated causal finding. |

First perform E00 and the controlled E01 granularity pilot, adding focused E02/E03/E04 controls on representative archetypes. Use tuned native readers, eager-metadata Mica and full Mica at each feasible granularity; preserve the same file and pruning information in the Mica pair. This first figure tests the proposed contribution directly before committing to the full campaign. In E02 include at least one closest modern native competitor and both simple and equivalent-information alternatives before optimizing Mica further. Expand to complete experiments after inspecting the failure branches. An unavailable critical comparator leaves the associated claim unresolved; do not silently omit it or choose a weaker substitute and mark the gate passed.

<a id="evaluation-status"></a>

**Evaluation status after the completed predicate-first study**

The final report and manifest close the selected execution study. The summary below maps that evidence to the broader paper plan; it does not reopen the execution guide's historical checklist.

| Study | Completed evidence available | Remaining obligation |
|---|---|---|
| E00 | Scoped exactness: 72 reader, 30 engine/layout and eight default cells; 18 engine traces, recorded source identities and accepted-run audit. | Correctness/provenance for newly introduced sidecars, writer variants, workloads and comparisons. E00 is not globally passed. |
| E01 | Historical granularity diagnosis and new staged data/decode/request counters. | Controlled granularity and discovery-versus-known-row matrix; staging is not the eager-metadata ablation. |
| E02 / E02a / E02b | Two enabled native Parquet engine layouts provide a bounded whole-system reference. | Improved-reader/sidecar/compatible-rewrite ladder, equivalent information, common candidate retrieval and closest native designs. S2a/S2b remain open. |
| E03 | Warm and advisory-eviction endpoints with observed process block I/O. | Persistent parsed-reader reuse, budgeted metadata caches, file admission and total-memory deployment. A process address-space ceiling does not complete E03. |
| E04 | Equal-retention clustered/dispersed synthetic pair and selected real workload boundaries. | Broader retention/locality/correlation distribution and independent workload coverage. |
| E05 | Combined, combined-empty-skip and predicate-first comparison is complete under the bounded contract. | Metadata/membership/alignment factorial, scaling terms and residual format-dependency attribution. Do not rebuild staging as a prerequisite. |
| E06 | Completed single-CPU DataFusion/Polars study: three queries, three Mica modes and two Parquet layouts, with exact outputs and mixed/negative staging results. Earlier 32-thread results remain a separate cohort. | Broader held-out and compressed comparisons, strongest compatible alternatives, suite coverage and representative budgets. No general real-query staging gain established. |
| E07 | Issued-work and observed-resource counters can support mechanism analysis. | Storage/index portfolios, writer/alignment stress and adoption amortization. |
| E08 | Selected-path lifetime/cancellation checks and bounded single-query measurement. | Concurrent service throughput/tails, shared budgets, strict public aggregate admission and first-batch responsiveness were not established. |
| E09 | One configured request policy/device and observed stage-induced request changes. | Controlled API/granularity/device and cap/depth studies. |

**Claim decisions.** Retain the completed execution result as evidence for S1 and a qualification of S3. The proposition that predicate-first generally improves the selected real full queries is unsupported, and automatic/default promotion was rejected. S2a and S2b are untested by these same-format mode interventions. G0 is satisfied only for the recorded scoped study; G1, G2 and G3 remain open for the broader paper. The scoped execution study is complete even though those paper-wide gates remain open.

**Reuse and next work.** Reuse the accepted measurements and traces without rerunning merely to change wording. Refresh affected results only if source, settings, inputs or a validity finding require it, preserving the archived cohort. Continue the E01/E02a pilot and E03/E04 controls. Do not add an automatic selector, pipeline or exhaustive allocator-accounting program to force the mixed staging outcome into a win. Reopening the completed execution study requires a concrete defect, invalid comparison or unmet original requirement.

2. **Shared experimental contract**

**Workloads.** Use NYC FHV and ClickBench as existing real-data anchors. Use GH Archive as the third independent corpus, with the concrete preparation and query specification below. Do not invent a production trace. Its events are real, but the proposed query sequence is synthetic and must be labeled accordingly.

**Third-corpus specification.** [GH Archive](https://www.gharchive.org/) publishes hourly JSON event archives. Acquire 2024-01-01 through 2024-01-07 UTC, preserving every parsed event in hourly-file then source-line order. Record missing/corrupt hours explicitly, input checksums and parse counts; never silently drop them. Build one flat table with event_id, event_type, created_at as UTC microseconds, actor_id, actor_login, repo_id, repo_name, nullable org_login and public. Preserve identifiers as strings to avoid numeric conversion ambiguity. Omit nested payloads from this flat-table study and state that scope. This preparation is proposed, not implemented or downloaded in this session.

Partition identically by UTC day for all formats. Query families are actor activity within a time range, repository activity, repository plus event_type, actor plus repository conjunction, event-type counts by day, and an unfiltered grouped-count control. Project either the relevant three columns or all nine; use exact count/grouping and deterministic ordered outputs as needed. Use days 1–3 for choosing configuration and query templates; freeze parameters/frequency-bin sampling rules before testing days 4–7, preserving naturally occurring empty matches. If a larger working set is needed, extend chronologically through January rather than duplicating a file and calling it independent real data. Record that expanded acquisition before running the test. No production-query frequency is asserted from this corpus.

Define six archetypes: clustered range; rare equality on a non-leading column; membership/IN with dispersed matches; compound range plus equality; a compound predicate whose per-column candidates intersect but no row qualifies; and a dense filtered scan/projection control. Include absent, rare and frequent values. For real queries sample literals from measured frequency/quantile bins using saved seeds. Keep a training set for parameter choices and a disjoint held-out set. A zero-output query is a useful correctness/control case, not the entire selective workload.

Separate scan input rows, rows passing filters, and final SQL output. A LIMIT 10 or COUNT returning one row is not 10-row or one-row scan selectivity. Use existing source-defined predicates from native-format bench (`workload.rs`) and selectivity profiles (`selectivity.json`) only after E00 checks their agreement.

**Comparison layers.** Native deployment comparisons let each implementation use its best legitimate reader, codecs, indexes, reader reuse and planning. Match CPU/memory limits and logical data; expose its own storage and build cost. Mechanism comparisons deliberately match row order, pruning information and encoding where possible to isolate a cause. Do not interpret a common custom reader as the fastest available product. Treat DuckDB or ClickHouse native storage comparisons as system-level alternatives, not format-only causality.

**Execution modes.** For future metadata/layout attribution, hold projection mode, exact-sink setting and physical I/O policy fixed across matched Mica lanes. Distinguish the production combined/sink-disabled configuration from sink-enabled study controls. Report explicit staged sensitivity separately; no automatic selector exists. Never pool modes or attribute a combined-mode cross-format gain to staged projection reads.

**CPU and device.** Record CPU model, NUMA placement, core and SMT allocation, governor, frequency policy, filesystem, kernel, scheduler, readahead, device/firmware, dataset placement and background load. Use one CPU budget in a mechanism experiment and matched engine budgets in macros. Record actual workers and I/O concurrency; equal environment variables alone do not prove equal resource use. Buffered I/O is the primary fair lane unless both implementations have equivalent supported direct-I/O paths. O_DIRECT is a separate controlled comparison.

**Output and timing.** Exact filtering is enabled for all headline results. Compare logical values, nulls, duplicate multiplicity and ordering where SQL requires it. Freeze deterministic tie handling without silently changing query meaning. Preserve a reference result outside measured execution. Time query admission to complete materialization for macros; separately measure preparation, first-batch and scan execution where helpful. Charge initial reader construction once in reused-reader modes and show its amortization. Do not include cache setup in a query timer or hide required index builds from lifetime cost.

**Residency.** Distinguish stored metadata, fetched metadata bytes, serialized cached bytes, parsed resident objects, query-private metadata and pinned I/O buffers. Report each plus total process and page-cache memory. E03 defines independently controlled diagnostic states and a deployment-like total-memory experiment. Do not call fadvise alone a verified cold state, or unrelated-file reads a guaranteed SSD-cache flush.

**Metrics.** Record wall time, CPU time, peak/live allocated memory, process RSS, file/cache residency, candidate groups/pages after every stage, logical row intervals, logical bytes requested, unique physical ranges, file-read bytes, block/device traffic where attributable, read count/size, queue depth, metadata wait/parse/evaluation, plan allocations, dictionary dependencies, decoded pages/rows/bytes and exact outputs. Classify metadata versus data at the file-range layer; process read_bytes alone cannot do that. Report overlapping stage spans as spans, not as additive latency components. Validate profiling overhead against uninstrumented runs.

**Statistics.** For isolated latency, start with six independent randomized blocks of five measured repetitions per cell, preserving block and process identity. Use paired block comparisons and confidence intervals; add independent blocks only according to a stopping rule chosen before inspecting winners. Do not pretend 30 correlated samples are 30 independent hosts. Report per-query medians, absolute changes and uncertainty; use geometric means only for an explicitly defined query set and ratios. Also report total workload time with declared weights. Outliers stay unless a documented external event invalidates the entire affected block. E08 has a separate tail-sampling protocol.

**Artifacts.** Each experiment produces a manifest, logical dataset fingerprint/order hash, physical file/index sizes and hashes, source revision and dirty patch, library versions, command/config snapshots, raw per-run events/results, correctness output, analysis script and table/plot source. Requested new cache drivers, writers and baselines are not available commands today. Implement and document their actual CLI before running; do not copy hypothetical commands from this plan into a paper as reproduction evidence. Preserve artifacts intentionally because several results directories are ignored by Git.

<a id="e00"></a>

3. **E00: correctness, provenance and a reproducible starting point**

**Hypothesis and role.** The compared queries implement identical semantics, and every reused number has a verifiable artifact and configuration. This is a prerequisite, not a scientific contribution.

**Setup.** Inventory current code and every candidate source artifact using [[evidence|evidence.md]]. Run the existing framework verifier against the September archive. Check query literals and intervals, type casts, projection/hidden predicate columns, LIMIT/ORDER BY, codecs, row ordering and index construction. Reconcile storage totals including external indexes and codec tables. Pin explicit Mica v3 settings; the current writer default must not be assumed to be v3.

**Run.** Use small differential cases for null/all-null pages, zero results, page and coarse-group boundaries, high/low cardinality, duplicates, long strings, NaNs and supported floating comparisons, timestamp boundaries, unsupported/partial pushdown, file rollovers and truncated inputs. Test equivalence of prepared versus reopened readers and policy overrides. Test no-false-negative metadata pruning against exact row evaluation. These tests must cover the proposed semantics, not simply repeat implementation branches.

**Analyze and deliver.** Publish an audited workload/configuration manifest and the exact scope of passed correctness checks. Correct the Figure 1 provenance, Table 3 storage accounting, appendix query and memory-result label. Existing verifier output only proves its nine-query contract, not arbitrary SQL or writer correctness.

**Failure rule.** An output mismatch blocks the affected comparison and must be diagnosed; it is not a performance outlier. A missing raw artifact makes the associated historical claim provisional until restored or rerun. Do not manufacture a replacement value from manuscript text.

<a id="e01"></a>

4. **E01: locate the granularity cost and separate discovery from retrieval**

**Hypothesis.** In a meaningful part of the intended workload, finer metadata avoids data work but increases discovery and execution overhead. Mica's organization preserves enough of the pruning savings to improve end-to-end cost. The experiment identifies which costs change and whether the useful granularity range changes.

**Setup.** NYC point/range and ClickBench point/compound plus a dense control. Sweep Mica row-page caps across 50, 200, 800 and 3200, measuring actual encoded sizes and splits. For Parquet independently sweep page row targets of 200, 2000 and 20000 and row-group targets of 1k, 16k, 256k and 1M, subject to writer feasibility. Keep data order identical. Include a sensible native baseline and its reuse-capable reader. Use both absent and resident parsed metadata as defined in E03. Do not infer exact boundaries from a writer size target.

At every Mica granularity run an eager-fine-metadata lane and the full selective-metadata reader on the identical file, with identical membership information, codec settings, predicates and physical-read policy. Verify the loading switch does not change candidate sets or exact results. This is the minimum causal control for the central figure. Include E02's equivalent-information alternative at representative granularities to distinguish cheaper use of metadata from simply having stronger indexes. Add independently mapped boundaries through E05 if alignment remains a headline contribution; the initial metadata test does not require a new writer variant.

**Run.** For each representative layout execute normal predicates, then a diagnostic supplied the same exact logical survivor rows/ranges computed outside timing. The latter includes per-format mapping and required decode dependencies but excludes discovery by design. Mica needs a benchmark adapter for this mode; after coordinated bisection, dividing a row ID by the configured rows-per-page is not a valid general mapping. Charge the mapping data structure and access cost, or label a separately supplied physical-page control as a narrower experiment. Preserve instrumentation of normal execution. Add a min/max-only lane, since extra membership information is a distinct cause.

**Analyze and deliver.** Produce M1 with end-to-end latency and data/metadata/CPU curves for tuned native readers, eager-metadata Mica and full Mica. Identify the measured best granularity for each lane, with uncertainty, without assuming Mica must prefer the smallest pages. Report both each system's tuned choice and same-information controls. Record where data savings are consumed by discovery overhead and where selective access preserves them. Include a dependency ledger recording which metadata objects were needed to locate each class of data reads. Report cold-byte I/O, parsing, metadata evaluation, mapping and data/decode costs separately. Compare logical exact-row retrieval without asserting equal physical work. Never label the difference between independently timed medians “the discovery time”; paths and overlap differ.

**Reuse.** Parquet granularity diagnosis, native-format profiler and Parquet latency/cache-control scripts are starting points. The old curves need verification and new controls, not automatic republication.

**Falsifier.** If optimized resident/reused native readers remove the apparent wall, report that condition. If Mica wins only through membership discrimination, S2 needs E02 to establish why its indexing is more than known index information.

<a id="e02"></a>

5. **E02: strongest alternatives, matched information and portability**

**Hypothesis.** Mica's organization makes fine pruning economical beyond the effect of adding index information or changing cache state alone. The closest systems have a measurable remaining access cost or different resource tradeoff. Portability to an existing format is a possible positive result; a new format is not assumed necessary.

**Setup.** Establish these alternatives, with versions and enabled paths verified in traces:

| Alternative | Configuration and purpose |
|---|---|
| Native Parquet | Tuned page/row-group sizes, relevant page indexes/Bloom, legitimate late materialization and reusable parsed metadata. Tests improvements to existing deployment. |
| Indexed Lance | Native indexes chosen for each training workload family, including exact row-location access when available, plus a min/max-only or index-matched diagnostic. Do not force a weaker index to mimic Mica. |
| Vortex | Default and supported finer layout/zoning configurations, native filters and metadata reuse. Determine actual access dependencies from code/traces. |
| ORC | Tuned row-index stride, stripes and compression blocks, native statistics/Bloom and selective reader. Verify whether indexes lead to independently readable/decodeable units. A separate native reader is acceptable; identify language/runtime confounds. |
| Simple indexed-Parquet control | An ordinary value/range-to-row-location index for selected hot columns, with normal Parquet retrieval and cached metadata. Tests whether familiar access methods suffice. |
| Hierarchical Parquet sidecar | Mica-equivalent row-interval membership and coarse/fine summaries, direct-addressed entries, and mappings to Parquet pages. Tests whether the proposed organization can be expressed without replacing data encoding. |
| Mature indexed engine | [DuckDB native table with eligible ART indexes](https://duckdb.org/docs/current/guides/performance/indexing) for point/IN work, or an appropriately configured [ClickHouse MergeTree setup](https://clickhouse.com/docs/reference/engines/table-engines/mergetree-family/mergetree). This is a system-level application alternative, clearly separated from format-only claims. |

Nimble/Pixels require source-level dependency analysis in [[prior-art|prior-art.md]]. Nimble's verified grouped selective-metadata machinery already warrants a focused metadata-open/refinement test under E03 states, unless a pinned-source explanation establishes that the relevant path cannot serve this workload. Do not wait for proof of whole-contract equivalence before testing a close partial mechanism. Promote Pixels to a focused experiment if its verified pixel metadata path targets the measured dominant cost. FastLanes is relevant for retrieval/partial-decode controls; lack of an equivalent predicate interface is a disclosed boundary, not permission to call it incapable.

**Run, matched-information study.** First construct the same row-interval summaries and membership information for Mica and the sidecar from one source partition. Validate identical candidate sets before physical mapping. Charge sidecar file identity/version validation and on-disk space. Map candidate intervals through each format's actual boundaries and dictionary dependencies. Use one projected numeric column and then 8/32 mixed-width columns. Add an aligned-Parquet writer variant only after verifying equal row boundaries; target page size alone is insufficient. Mark this as a modified format writer, not a native feature guaranteed by every writer.

**Run, native portfolio study.** Allow each system to use stronger information and best supported access paths. Compare one hot indexed column, four predicate columns, and broad schema coverage, with a fixed workload mix of equality/range/compound predicates, including predicates on non-leading dimensions. Report index size/build cost and permit per-format Pareto choices. Tune on training queries and freeze settings for held-out queries. Report an oracle best-per-query result separately from a deployable fixed configuration.

**Analyze and deliver.** Produce a mechanism capability/dependency matrix with verified source and measured cost. Compare both same-information controls and best-native outcomes. A sidecar is a mechanism intervention, not a replacement for native competitor evaluation. Do not force identical Bloom bits if that makes one system arbitrarily weak; include an index-space sweep in E07.

**Decision rules.** If the sidecar implements the substantive proposed organization and matches Mica, this supports portability and removes the need for a format-replacement claim. If a simple familiar index matches across the intended predicate portfolio at comparable storage, build and memory cost, reassess which parts of Mica are needed. A matching point lookup alone does not settle a broader portfolio claim. If an existing design already offers the same organization and tradeoff, faster Mica code alone does not establish originality. If alternatives lose, trace the loss to a verified dependency instead of naming the entire format as the cause. The contribution need not be impossible to reproduce with existing-format extensions.

<a id="e02a"></a>

**E02a: compare increasingly invasive alternatives.** This study answers S2a and identifies whether S2b requires a data-layout change. Begin with one clustered range, one dispersed equality and one compound query plus a dense control on the existing corpora. Use narrow and wide projections, original row order and E03 M0/M2 states; add M3 before making a deployment claim. Tune on training queries and freeze settings. Keep the simple exact-index and closest native-format comparisons above; the following lanes serve causal diagnosis and do not replace them.

| Lane | What changes | What remains fixed | Question answered |
|---|---|---|---|
| P0: tuned native reader | Supported settings and legitimate reuse. | The chosen Parquet input bytes. | What can an existing deployment do today? |
| P1: improved reader | Profile-driven improvements to parsing, caching, range planning or supported selective loading. Publish the source patch. | Byte-identical P0 files and pruning information. | How much of the problem is avoidable reader overhead? |
| P2: equivalent-information sidecar | Add directly addressable coarse/fine summaries, membership and interval-to-page locations to P1. | Byte-identical P0 data files; same logical fine intervals and pruning information as the matched Mica lane. | Can external metadata provide the proposed benefit without rewriting data? |
| P3: compatible rewritten layout | Where P2 exposes a consequential boundary/decode cost, rewrite using verified aligned fine boundaries within the existing format and retain the sidecar as needed. | Logical values/order, common pruning intervals and information. | Does a writer/layout policy suffice while preserving the format specification? |
| F: full Mica | Mica metadata and data organization. | Logical values/order, queries, common information in the mechanism lane and resource limits. | What benefit remains from the integrated organization? |

P1 is an optimized feasible control, not a promise to implement every conceivable reader. Record the profiled bottleneck, the concrete patch and the residual cost. If the selected native reader already performs the proposed optimization, P0 and P1 may coincide; do not build an artificially weak variant. P3 is necessary before attributing a material P2-to-F gap to incompatible data boundaries, but need not be built if no such cost is observed. Verify format conformance and actual boundaries. An unavailable writer feature is a tooling limitation until the specification or encoded dependencies establish otherwise.

Hash P0/P1/P2 data files to verify they are unchanged. Build the P2 sidecar from a common interval manifest; verify candidate-interval equality against matched Mica before physical mapping. Charge location tables, discovery metadata, initialization and retained state. Sidecar publication must bind metadata to the immutable data identity. Use an explicit validation lifecycle and charge required work where it occurs; do not require an arbitrary full-file checksum on every lookup. Missing or mismatched sidecars must fail explicitly or fall back safely to an exact native scan, with fallback runs labeled separately.

Run each lane both end-to-end and with stage instrumentation. Report absolute latency, uncertainty, metadata bytes fetched/parsed/resident, mapping CPU/allocations, data bytes, decoded rows/bytes, shared codec state, requests and exact outputs. P0-to-P1 isolates a reader change on fixed files. P1-to-P2 can add information as well as change its representation, so add an eager-sidecar control with identical entries if attributing that difference to addressability. P2-to-P3 changes layout and may change compression. P3-to-F can still change encoding and reader implementation. These latter contrasts are not single-factor causal effects.

<a id="e02b"></a>

**E02b: identify and substitute the residual dependency.** For a representative query in every surviving lane, record a dependency trace: metadata needed before an offset is known; fine entries evaluated; interval-to-column mapping; data ranges and codec state fetched; decoded units; physical requests; and critical-path waits. Distinguish required work from speculative prefetch, and CPU work from overlapping elapsed spans. Attribute a residual cost only after inspecting the relevant source and stored layout.

Supply the same candidate row-interval manifest to P2/P3/F in a retrieval-only control, while retaining each format's necessary mapping, locators and codec state in timing and memory accounting. These are pruning candidates, including false positives, not oracle exact rows. Keep E01's exact-known-row diagnostic separate. A shared sidecar evaluator can provide an additional common discovery front end; include its cost in the corresponding end-to-end diagnostic. Preserve best-native paths separately.

Use E05 to test the suspected cause. Examples are efficient independent-boundary mapping versus aligned boundaries at matched information, or eager versus selective access to identical detail records. Use a common physical I/O policy where feasible. An uncompressed diagnostic removes codec differences but does not equalize page headers, byte layout or metadata, and does not replace compressed native results. If a common executor would handicap a native reader, retain both the diagnostic and best-native results. No speedup difference between independently timed medians may be labeled the isolated format benefit.

**Analysis and deliverables.** Produce Figure M4, a dependency ledger with source/configuration references, and a verdict for each intended workload region:

| Observed outcome | Supported paper claim |
|---|---|
| P1 recovers the benefit at comparable costs. | Reader improvement; format replacement is not justified by this result. Assess whether the reader technique itself is a distinct contribution. |
| P2 recovers the benefit using the substantive proposed organization. | Portable metadata/reader organization; a new data format is optional. Compare the organization with prior work. |
| P3 recovers the benefit but P2 does not. | Coordinated writer/layout policy matters; a new format specification is not established as necessary. Charge rewriting and compatibility costs. |
| F retains an explainable benefit over the strongest compatible lane and native competitors. | An integrated-layout advantage in the measured regime, subject to E07 adoption costs. This does not prove all existing formats incapable. |
| A gap remains but substitutions cannot identify its cause. | Implementation-level performance evidence only; S2b remains unresolved. |

Matching means practical equivalence under predeclared workload tolerances and comparable resource costs, not merely a statistically nonsignificant difference. Report confidence intervals and configurations; insufficient precision is unresolved evidence. A native format that already provides the same organization challenges originality even if the Parquet ladder favors Mica.

**Execution order.** Build the P0/P1/P2/F pilot and trace it before implementing P3 or a large format-variant matrix. If a residual layout cost motivates P3, prioritize that test before expanding macrobenchmarks. Promote the strongest compatible alternative into E06 and E07. Complete the broader E02 portfolio and E03/E04 controls before claiming practical significance.

<a id="e03"></a>

6. **E03: metadata lifecycle, cache budgets and realistic file admission**

**Hypothesis.** Fine metadata addressability provides value over a realistic range of reuse and memory budgets, not only after forced reconstruction on every query.

**Diagnostic setup.** Independently distinguish four metadata states: M0, absent metadata bytes and no parsed objects; M1, resident serialized metadata bytes but reader objects rebuilt; M2, persistent parsed metadata/prepared readers reused; M3, finite shared metadata budget with eviction and reuse. Cross M0–M2 with cold and warm data when technically separable. M2 includes dictionaries, locators and persistent preparation needed for the query, and charges construction once. Do not call warm OS bytes M2.

Keep a long-lived process in M2/M3, allow both competitors and Mica their legitimate reusable objects, and measure owned/retained parsed allocations. Do not assume MicaPreparedFile retains every lazily loaded object across queries; inspect and instrument actual ownership. Cache wrappers must avoid unintentionally sharing final query results or predicate-specific plans unless the same capability is offered and measured for all systems.

For data-cold/metadata-warm diagnostics, keep parsed metadata and evict only known data regions where possible. Page-aligned metadata/data overlap must be identified and charged, not assumed away. If range eviction is unreliable, use an instrumented controlled I/O cache for the diagnostic and label it as such, then validate the conclusion in the total-memory buffered-I/O study. Avoid claiming physical independence that the filesystem does not provide.

**Deployment setup.** Use a deterministic table-level admission layer with identical logical file statistics and layout for all formats. Vary files admitted per query over 1, 8 and 64 where meaningful, and include an effective partition-pruning case. Vary reuse distance and skew with uniform and hot-set workloads, plus shifts in hot set. The relevant working set is metadata actually reachable after admission and projection, not all table metadata. Preserve original file partition boundaries across formats or explicitly isolate their differences.

Start with absolute metadata budgets of 16, 64, 256 and 1024 MiB plus no retained metadata and sufficient-memory endpoints, subject to the testbed and observed working-set size. These are exploratory budget points, not claims about production provisioning. Include schemas/footers/coarse summaries, serialized cache and parsed objects in the accounting; keep a separate fixed query-execution allowance and report any uncacheable residency floor. Add a total-memory experiment where each system may allocate its own metadata/data split. Pinning a competitor to an unhelpful split is not a fair deployment comparison.

**Cache policy and enforcement.** In the mechanism diagnostic use a common byte-accounted LRU admission/eviction rule at each reader's supported metadata-object boundary. Account for fixed roots, cache entries, allocator overhead estimates and shared ownership once. Evicted objects still retained by readers or in-flight queries remain charged until released. An entry larger than the cache budget is nonresident: process it transiently, charge its peak allocation, and do not retain it. If fixed roots or unavoidable pinned allocations exceed the declared allowance, report that cell as infeasible rather than excluding them from accounting. Release or reconstruct prepared-reader handles when their retained state prevents the selected budget from being respected. This is a controlled diagnostic and may restrict native reuse; report best-native policies separately.

For total-memory deployment runs, use a verified process-group memory limit that includes charged filesystem cache, such as a dedicated cgroup on the test host, and report anonymous/file/kernel charges and limit events. Establish cache ownership before measurement so preexisting shared file-cache pages are not invisible to the limit. Verify the mechanism's availability during setup. If enforcement cannot be established, report observed memory curves only and leave a hard-budget claim unvalidated. Match swap policy and output buffering; count oversized-entry transients and in-flight buffers against total memory. Do not mistake a nominal cache capacity or process RSS for an enforced whole-system budget.

**Run.** Execute predeclared sequences long enough to expose steady-state reuse and transitions. Measure first query, amortized sequence cost and budgeted steady state. Report cache admissions/evictions, hit/miss bytes, parse reconstructions, actual live memory, admitted files and projected/predicate columns. Use repeated independent sequences and retain warm-up separately. Test at least one sequence whose reuse favors traditional persistent readers.

**Analyze and deliver.** Produce M2 as latency versus equal absolute budget, with separate total-memory results and observed cache states. Plot amortization against queries per prepared reader. Explain precisely whether a win comes from fewer metadata bytes, less parsed-object memory, fewer reconstructions or less metadata evaluation.

**Reuse.** Existing warm-page-cache experiments and Parquet metadata controls help instrument endpoints. They do not measure this matrix. New bounded cache/lifecycle support is required; see [[design-extensions|design-extensions.md]].

**Falsifier.** If normal parsed-reader reuse eliminates the benefit in the independently motivated workload, limit the result to a consequential cold-start use case if one exists. If file admission makes detailed metadata comfortably resident, do not claim table-size pressure creates a need. A synthetic random-file sequence alone does not prove broad deployment significance.

<a id="e04"></a>

7. **E04: selectivity, locality, correlation and useful workload coverage**

**Hypothesis.** Benefits occupy a meaningful predefined region, and their boundaries follow page occupancy and index discrimination rather than final output size alone.

**Setup.** Hold logical rows constant within each comparison. Use original order, a reasonable time/entity clustering policy, and controlled random permutations at 0%, 10%, 50% and 100% of rows. Record actual candidate locality rather than assuming a shuffle percentage predicts it. Sweep row retention on a logarithmic grid from approximately one match through 0.001%, 0.01%, 0.1%, 1%, 5%, 20% and 100%, constrained by row count. Include predicate frequency skew and long IN lists. These controlled datasets explain mechanisms; they do not replace real-data workloads.

Construct positively correlated, independent and anticorrelated two-column predicates with comparable marginal selectivities. Add a low-cardinality value present on almost every page, an absent value, and a non-sort-key range whose coarse min/max covers the whole domain. Include both narrow and wide projections. Give every format the same row order in each cell.

**Run.** Execute representative native baselines, the strongest E02 alternative and Mica with fixed settings selected on training queries. Collect stage candidate counts including pages rejected only during exact row filtering. Use enough independent layout seeds to separate placement effects from one favorable permutation.

**Analyze and deliver.** Plot latency ratios and absolute metadata/data bytes across the grid, with losses shown. Compare candidate-page fraction with the independent-occupancy reference `1 - (1-s)^r`; this reference assumes exact membership and independent row placement, so it is neither a prediction for clustered files nor a bound on min/max selectivity. For each application workload report the fraction of queries and baseline time falling inside the observed benefit region. Do not redefine the intended workload after seeing the heatmap.

**Falsifier.** If only tiny cold point queries benefit, prioritize exact native indexes in E02 and assess their cost. If plausible query sequences lie mostly outside the useful region, narrowing the narrative does not make the original significance goal pass.

<a id="e05"></a>

8. **E05: causal interventions and scaling terms**

The scoped predicate-first study is now complete. Reuse its exact and performance evidence for combined, combined-empty-skip and sequential predicate-first execution, including enabled Parquet baselines and dense losses. Its common process envelope supports the selected single-query comparison, not strict production aggregate admission. Automatic policies and pipelining were not needed to answer that question and remain deferred. These measurements do not complete the metadata/layout factorial below or establish a format contribution.

**Hypothesis.** The retained design choices reduce identifiable costs in realizing fine-grained pruning. Where the paper claims complementarity, interventions establish it. Useful additive effects are legitimate; neither superadditivity nor novelty of every component is required.

**Setup and run.** Build a small factorial study across min/max-only versus equivalent membership information, eager versus directly addressable sparse fine-metadata handling, and aligned versus independent column boundaries. Alignment requires separately written files and validated row mapping; it cannot be a same-file toggle. Keep logical values, row order and codec choices fixed, record actual encoded sizes, and include a bytes/decoding-matched diagnostic where layout changes compression. Match membership on a common logical interval domain for the information control. Supply efficient row-range mapping to the independent-boundary reader; do not implement an intentionally quadratic competitor.

Run the central factorial on clustered range, dispersed equality and compound workloads, at coarse and fine granularity. Report interaction contrasts on raw latency or CPU cost with uncertainty. Use the prior-art mechanism matrix to distinguish originality from efficacy. Report additive effects or absent interactions faithfully. A null alignment effect narrows the contribution to the supported metadata/reader organization; it does not by itself falsify that broader contribution. Use the residual-cost ledger from [E02b](#e02b) to choose substitutions. Eager versus sparse loading within Mica establishes how its reader uses the representation; it does not independently establish an advantage from changing the file format. Cross-format gaps require their own dependency controls.

Separately use existing same-file controls for eager versus sparse secondary loading, generic versus eligible run decode, optional gates and coalescing. The historical `full_materialize_generic` lane changes several dimensions and is not a clean single-factor sparse-index ablation. Use an actual isolated switch or label the result as a bundled comparison.

For scaling, vary total P with fixed K, then vary K with fixed P, then arrange the same K pages into 1, 8, 64 and fully scattered runs where possible. Vary relevant columns over 1, 8 and 32. Separately grow schema width over 8, 32, 128 and 512 scalar columns while holding the queried columns, row partition and their values fixed. The prepared-file path reads coarse maps for all schema columns, while request-aware adaptive opening can select relevant columns; compare those lifecycles and account for all retained preparation state. Include two P-growth regimes: added regions excluded by coarse maps, and added regions that defeat coarse maps. Record fixed/shared dictionaries separately. Account for Mica's per-column file-size limit by distinguishing within-file growth from manifest-backed multi-file growth.

**Analyze and deliver.** Report metadata entries visited, bitmap words processed, plan objects, allocations, requests and decode work. State which costs remain functions of P, candidate A, projected columns C and K. If alignment adds little benefit after efficient row-range mapping, demote it to an implementation choice. If only page membership contributes, do not attribute the speedup to the entire reader co-design. Drop contribution claims for gates whose benefits are within uncertainty or outweighed by regressions.

**Reuse.** Ablation scripts, profiles and historical summaries are reusable infrastructure and hypothesis evidence; clean controls and a pinned rerun are needed.

<a id="e06"></a>

9. **E06: full-query engine evaluation**

**Completed subset.** The September 29 study reports exact complete DataFusion/Polars queries with enabled Parquet 1M/20K and 64K/2K layouts. Compound staging effects have intervals crossing zero; Polars point staging loses 6.74%; dense grouping loses 18.81% and 22.55% in DataFusion and Polars versus combined-empty-skip. The selective cross-format advantage already exists in combined mode. Reuse the full results table with these losses. The proposed expansion below remains open.

**Hypothesis.** S1/S2 improvements affect complete queries, including engine preparation and execution, beyond one favorable reader.

**Setup.** Extend the matched framework comparison harness. Preserve the nine common query definitions as one historical cohort. Add held-out parameters, range/equality/compound coverage from E04, dense controls, broader projections and at least one relevant aggregation or join where scan savings can be diluted. Inventory the full chosen benchmark suite: implemented, unsupported and excluded queries with reasons. Report the supported suite and target selective subset separately. Do not label predicate/projection fragments “full ClickBench queries.”

Use DataFusion and Polars to test whether benefits survive distinct engine paths, and nearest native-format comparators in a compatible engine or their canonical reader at a separately labeled boundary. Fix training-selected configurations, include compressed deployment choices, and run on both low and representative matched core budgets. Match query semantics and account for genuine physical representation differences such as Utf8 versus Utf8View instead of forcing unnecessary conversions.

**Run.** Include the strongest compatible E02a alternative in a supported engine path for the representative queries used to justify format adoption. If only a reader-level adapter exists, leave the full-query adoption comparison unresolved and state that boundary. Use E03 cold, reusable-reader and one relevant budgeted workload state. Validate exact outputs outside timing, record plans and pushdown decisions, measure first-batch and complete-query times. Explain why gains differ between engines using scan/plan/compute evidence; do not pool their numerical ranges.

**Analyze and deliver.** A per-query table with absolute times, ratios and uncertainty; target-subset and full supported-suite totals; peak memory and CPU; explicit losses and unsupported coverage. Show the historical near-parity Polars Q41 rather than suppressing it. Four-order candidate-materialization reductions are secondary diagnostics, not equivalent-output peak-memory claims.

**Reuse.** The September archive supplies a strong historical exact-output result under its particular no-compression, 32-thread, cold protocol. Refresh it if the measured source or relevant settings change and add the missing controls. It does not need to be discarded simply because the final study is broader.

**Falsifier.** If gains vanish outside reader-only timing, the full-query claim fails. Explain a narrow scan-bound benefit only if it still meets the independently chosen application need.

<a id="e07"></a>

10. **E07: storage, index portfolios, writer cost and alignment coupling**

**Hypothesis.** The benefit is an attractive resource tradeoff, rather than unaccounted index space or loss of compression.

**Setup.** Compare page sizes from E01; native codecs including uncompressed and supported LZ4/Zstd/Snappy choices as applicable; Bloom precision and bitmap cardinality thresholds; one/four/broad predicate-column coverage. Use best-native exact indexes as well as matched-information controls. Do not imply every codec exists in every format. Plot each implementation's supported choices rather than forcing a single codec as the deployment answer.

Add a controlled wide-schema pair: the same queried numeric columns and rows, with and without one unqueried heavy-tailed string column. Include moderate and page-overflow-triggering string distributions. Test a row above the supported page budget as a documented failure case. Shared bisection can change every column even when the added column is never queried; this is a direct stress test of the central invariant.

**Run.** Measure writer throughput, total CPU, peak memory, temporary files, bytes written, index construction time, final data/metadata/dictionary bytes, final page sizes/counts and full-scan performance. Record attempted encodes/retries if available. Measure query results under equal total storage allowances where configurations are feasible. For index portfolios, report the build/storage cost of covering the workload's predicates; do not index only the competitor's least favorable column.

**Analyze and deliver.** Plot latency versus total stored bytes, with points annotated by resident metadata and build cost. Avoid a scalar score that hides a dominated configuration. Evaluate adoption against the strongest compatible E02a lane, not only against default Parquet. Report incremental conversion/index-build CPU and wall time, peak temporary storage, retained source copies, final stored bytes and reader/integration requirements. Separate preexisting-file conversion from greenfield writing; both alternatives have construction costs in the latter case. Count sidecar creation/validation and compatible rewriting where applicable.

For a fixed query sequence, let Delta B be Mica's initial construction cost minus the compatible alternative's cost in the same stated unit. Compare Delta B with the cumulative measured query-cost savings over the expected reuse horizon. Include negative per-query savings and first-open costs. Do not mix CPU seconds with wall seconds or monetize storage without a stated model. If average savings are nonpositive, report no positive-cost amortization; if Delta B is nonpositive, report that directly rather than inventing a positive break-even. Show whether the observed horizon reaches break-even, and report storage/compatibility burdens separately. Latency savings alone do not establish an acceptable adoption cost. Full-scan regressions and storage expansion belong in the main tradeoff discussion. A slow scan with more bytes is not proof that the reader has no overhead; use E01/E05 to attribute costs.

**Reuse.** Disk-space analysis, writer and cap sweeps can be reused after E00 accounting checks. Existing 981 versus 369 MiB figures describe one uncompressed NYC representation, not the space relationship under optimal deployment codecs.

**Falsifier.** If a simple existing index portfolio dominates at relevant latency, storage, memory and build cost, the current combination lacks a compelling deployment case. If an unqueried wide column causes severe amplification, quantify the practical distribution where it occurs before proposing a different alignment design.

<a id="e08"></a>

11. **E08: concurrency, shared budgets and full-query memory**

**Hypothesis.** Candidate-oriented execution remains useful under engine contention and does not purchase isolated latency through unbounded resources.

**Setup.** Fix total worker/CPU and memory budgets across all concurrent queries, rather than giving every query the isolated full budget. Use selective-only, dense-only and two declared mixtures such as 90/10 and 50/50 selective/dense requests. Include both equal logical query proportions and measured CPU/I/O shares, since one scan can dominate a count-based mix. Use M3 realistic reuse and a resident-reader control. Vary concurrency 1, 2, 4, 8, 16 and 32 where resources permit.

**Run.** First measure saturation throughput. Then use an open-loop arrival process at common absolute offered rates below and near the lowest shared sustainable region, plus per-system saturation curves reported separately. Include queueing in response time and report dropped/failed requests and backlog. Avoid coordinated omission. For p99, collect at least 10,000 completed requests per chosen operating point and multiple independent runs, lengthening if tail confidence is poor; disclose the actual duration and sample count. For expensive scans use a longer run or report a lower quantile rather than inventing p99 from ten observations.

Instrument cancellation, maximum outstanding I/O, live metadata/plan/buffer bytes and engine worker usage. Distinguish total RSS from output payload and candidate-buffer memory. Use the same output-consumption/backpressure behavior for every implementation.

**Analyze and deliver.** Throughput against response-time quantiles, memory, CPU and fairness by query class. Investigate whether batching blocks short queries behind scans. A resource cap is a control, not a proven hard memory bound unless all relevant allocations are charged and enforced.

**Falsifier.** If isolated gains disappear with contention or memory amplification causes failure, S3 needs a concrete execution fix or narrower substantiated scope. Do not describe unimplemented multi-tenant fairness or scheduling as an existing contribution.

<a id="e09"></a>

12. **E09: hardware and request-policy boundary**

**Hypothesis.** Hardware/request effects explain a measured part of Mica's usefulness, rather than merely supplying an attractive NVMe introduction.

**Setup.** Replace the old padded-range benchmark with selected logical intervals mapped into the union of required physical units for each granularity. Deduplicate and coalesce overlapping coarse units before I/O. Compare coarse/fine granularity crossed with synchronous pread and batched io_uring, at matched useful data and controlled CPU/concurrency. Include an efficient sequential fallback for dense access and separate fixed-byte I/O tests. Test two materially different available NVMe classes; identify unavailable hardware rather than making a universal claim.

**Run.** Use cache conditions from E03, supported buffered/direct variants separately, and request/depth sweeps. Measure actual unique/device bytes, CPU and achieved outstanding depth. Reuse Mica cap-sweep machinery across sparse, clustered and dense requests; include an uncapped condition. Do not tune per workload on the final test set.

**Analyze and deliver.** State the empirical device/request range where batching helps. If Mica works equally well with pread, retain a metadata/format result and reduce the claimed role of io_uring. If cap sensitivity is flat or mixed, call the cap a practical policy. Do not turn manufacturer's peak IOPS into evidence that tiny query runs saturate the device.

13. **Evidence and decision gates**

| Gate | Required decision evidence | Proceed condition | Failure response |
|---|---|---|---|
| G0 trust | E00 plus reproducible pilot manifests. | Equivalent semantics, resource attribution and source-linked results. | Repair or exclude invalid comparisons with disclosure. |
| G1 systems contribution | E01/E02a/E02b and central E05 controls plus prior-art source comparison. | S2a establishes the organization advantage. A new integrated-format advantage additionally requires S2b: a traced residual dependency and worthwhile benefit over the strongest compatible alternative, with E07 adoption costs. | Record reader-only, portable metadata, compatible layout, integrated-format or unresolved outcome. Do not treat S2a passing as S2b passing. Reconsider the broader claim if no distinct consequential advance remains. |
| G2 deployment | E03/E04 and pilot E07. | Benefit covers a credible predefined query/reuse region at acceptable storage/index cost. | Revisit the actual target or stop the broad strong-paper claim. Do not redefine every loss as out of scope. |
| G3 complete system | E06/E07/E08 and E09 scope checks. | Full queries benefit with exact output, accounted resources and disclosed losses. | Diagnose execution bottleneck; no substitution of reader-only results. |

There is no universal 3x threshold. Before full runs, freeze application weights and practical cost tolerances based on the deployment case, separately from statistical significance. Gate G1 requires an explained advance relative to verified prior systems. Benchmark success alone cannot establish originality, and component-level precedents alone cannot reject a systems contribution. No new constituent algorithm or proof of format necessity is required.

A failed hypothesis is a research result. Stop tuning the same workload to force it through a gate. Use the decision branches in [[storyline|storyline.md]] and record the outcome and configuration in the journal.

---

## Vault Navigation & MoC Context

- [[Mica]]: Central Level 3 Project Hub for Mica paper notes and core concepts.
- [[README|Mica Plan Overview]]: Master roadmap and synthesis of the SOSP/OSDI research plan.
- [[storyline|Mica Storyline]]: Proposed SOSP/OSDI research storyline and core claims S1–S3.
- [[prior-art|Mica Prior Art]]: Primary-source positioning and novelty analysis.
- [[evidence|Mica Evidence]]: Implementation status audit and empirical evidence synthesis.
- [[design-extensions|Mica Design Extensions]]: Infrastructure requirements and conditional architecture extensions.
- [[stress-test|Mica Stress Test]]: Stress-test ledger and falsification criteria.

