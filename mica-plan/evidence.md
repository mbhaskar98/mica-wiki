---
tags: []
created: 2026-10-15
description: Implementation audit and empirical evidence synthesis reconciling code capabilities with the completed predicate-first bounded study.
aliases:
  - Mica Evidence
  - evidence
---

# Implementation and experiment evidence

Updated 2026-10-14. The original format/code audit inspected `b00564d810596a8bd2361fcbacbf4a7abaa19ee4` on 2026-09-28; its source-line references are historical navigation aids, not a fresh audit of every current line. The completed predicate-first study freezes experimental core at `cbb11fc` and closes in `5fb5225`; the linked manifest records per-program source and binary identities. This reconciliation ran no new experiment and does not constitute an exhaustive correctness audit. The manuscript and September assessments are working-tree documents; the implementation and archived measurements are the primary evidence below.

<a id="current-assessment"></a>

## What the current evidence supports

Mica has a credible systems contribution in making fine-grained pruning practical. This is an assessment of the inspected organization and recorded evidence, not a new measurement or a conclusion that all SOSP/OSDI evidence requirements have passed.

| Evidence | Supported interpretation | Remaining limitation |
|---|---|---|
| Shared row partitions, direct-addressed detail metadata and separately batched reads in code | The contribution has a concrete format/reader implementation. | Implementation alone does not establish distinctiveness or the importance of every choice. |
| May 11 granularity diagnosis | Finer Parquet pages reduced decode work but increased latency in the tested reader; Mica demonstrated inexpensive access to a small subset of fine metadata. | Readers had different pruning information; tuning, reuse and matched-information controls remain necessary. |
| Same-Mica eager-metadata ablation | Selective metadata access contributes to recorded latency gains without changing the underlying format. | It does not isolate alignment or prove the whole organization is novel. |
| September exact-output engine comparison | The implemented path benefits complete queries in the recorded cold, uncompressed comparison. | It does not settle compressed native alternatives, workload coverage or concurrent resource behavior. |
| Prior-art review | Hierarchies, shared row groups and selective access have predecessors. | Component overlap does not establish equivalence of complete designs or their costs. |

The next discriminating result is E01's granularity sweep with tuned native readers, eager-metadata Mica and full Mica, supported by E02 information controls and E03 reuse states. Alignment remains a testable explanation, and storage, construction, codec and total-memory costs remain part of the claim.

## Evidence for introducing a format

The granularity experiment establishes overhead in the tested reader. The eager-metadata ablation establishes the value of selective access within Mica. Neither isolates the incremental benefit of replacing the data format. Current source inspection identifies format choices that enable the reader, but does not establish that a compatible representation cannot supply those choices at comparable cost.

The [[experiments#e02a|E02a comparison]] and [[experiments#e02b|E02b dependency controls]] are proposed work, not completed results. S2a concerns the metadata/reader organization; S2b concerns the integrated layout's additional benefit and adoption cost. Until those studies run, the supported wording is that Mica introduces a jointly designed format and reader, not that a new format has been shown necessary or preferable to every compatible alternative.

## What the implementation establishes

| Mechanism | Inspected implementation | Defensible statement and limit |
|---|---|---|
| Shared row partition | Writer bisection (`writer/facade.rs:164`), commit of all column results (`writer/facade.rs:243`) | The writer encodes the same RecordBatch slice for every column, collects all successful column results before committing that page, and bisects the entire slice when any column overflows. Page ordinal therefore refers to the same row interval across columns. One large value can force smaller intervals for all columns. A single row exceeding the page budget is rejected. |
| Fine metadata with direct location | V3 layout (`writer/layout.rs:117`) | V3 stores coarse and fine zone maps and per-column detail blocks containing fixed-width page-index entries, membership information, and optional FSST tables. Directly addressable metadata permits selective detail access. It does not imply every detail is accessed individually or only after final survivors are known. |
| Page-level membership | Writer membership generation (`writer/facade.rs:302`), index selection (`writer/layout.rs:53`) | The writer builds per-page Bloom filters and chooses Bloom or low-cardinality bitmap representation according to distinct tracking. A bitmap states value presence at page granularity, not exact row position. Intersecting page memberships still requires exact row filtering. |
| Hierarchical, deferred metadata | Adaptive metadata open (`reader/mod.rs:2850`), predicate preparation (`reader/mod.rs:2023`) | Adaptive open can defer fine zone maps and page locations. Coarse survivors select fine metadata groups, and subsequent membership refinement operates on intermediate candidates. This is substantial implemented functionality. |
| Selective page-location resolution | Page-index planner (`reader/mod.rs:4700`), sparse/full decision (`reader/mod.rs:6220`) | The reader derives selected page ordinals and runs, estimates physical metadata bytes after coalescing/alignment, and chooses sparse or full page-index access. It constructs per-column locator vectors afterward. |
| Exact rows and hidden predicate columns | ReadRequest contract (`reader/types.rs:29`), predicate sink (`reader/execution/executor.rs:490`) | Output projection and predicate-only columns are distinct. The windowed predicate sink can evaluate hidden columns without constructing their full public output arrays. Exact filtering is implemented, but this path does not establish that rejected projection pages avoid physical I/O. |
| Bounded execution and engine scheduling | Scan split contract (`reader/scan_plan.rs:8`), execution budgets (`reader/budget.rs:9`), public scan source (`scan.rs:59`) | Prepared scans expose splittable work and shared prepare/scan budgets. Window limits bound an individual window. They do not alone bound all concurrent query memory or prove fairness under contention. |
| DataFusion integration | Filter classification (`datafusion/lib.rs:505`), execution task production (`datafusion/lib.rs:380`) | Supported predicates are exact; extractable conjuncts can be inexact; unsupported expressions remain with the engine. Existing tests cover partial pushdown, exact filters on hidden columns, empty projection and same-column OR. These are adapter tests, not proof for every SQL expression. |
| Polars integration | Anonymous scan (`polars/lib.rs:658`), residual filter (`polars/lib.rs:681`) | Polars passes supported predicates and projection through an anonymous scan. Inexact translation re-applies the original predicate using Polars. The September comparison uses canonical `single` mode, not forced partitioned or native-task-stream modes. |

### Qualifications that should affect the design section

1. The shared partition is a row interval, not a fixed physical byte size. Default rows per page are 200, but recursive bisection changes actual intervals. The default page-size field is 8 KiB while the default maximum encoded page budget is 16 MiB. Do not call every data page an 8 KiB page. format constants: `format/mod.rs:37`, writer defaults: `writer/config.rs:18`.
2. V3 is explicitly selected in the evaluated lane. The generic `WriteConfig::default()` currently selects format minor version 2. Any experiment must record the actual writer and reader versions. writer defaults: `writer/config.rs:18`.
3. A page is independently accessible subject to explicit codec dependencies. Optional FSST decoding uses a shared per-column symbol table. The reader loads those tables for projected string columns. Avoid an unqualified claim that every page is entirely self-contained. FSST writer training: `writer/facade.rs:196`, FSST loading: `reader/mod.rs:2917`.
4. `COARSE_ZM_GROUP_SIZE` is compiled as 1,024 pages. It is a design parameter, not a writer option. constant: `format/mod.rs:63`.
5. Per-column encoded page data is represented by a `u32` size, with a maximum of `2^32 - 1` bytes. The table writer rolls to another file on `FileLayoutOverflow`. Large-file and wide-column experiments must account for this partitioning rather than silently treating a table as one unlimited file. representation: `format/column_meta.rs:3`, rollover: `writer/table_writer.rs:149`.
6. The metadata policy is partly heuristic. The default deferred-index gate refines only above 64 surviving pages. Sparse page-index access with a read config requires at least 10% estimated byte savings after planning. The open path also speculatively loads small Bloom sections below 2 MiB. These rules are not a calibrated model of expected end-to-end latency. gate: `reader/mod.rs:2064`, constants: `reader/mod.rs:945`, sparse decision: `reader/mod.rs:6220`, speculative load: `reader/mod.rs:2890`.
7. Predicate order is selected using coarse pruning and estimated metadata cost. It can scan coarse entries and clone the current dense bitmap while scoring alternatives. Do not charge only the final chosen predicate's metadata work when describing discovery cost. ordering: `reader/mod.rs:3680`.

## The actual complexity boundary

The current representation does not support the draft's strongest survivor-only formulation.

- `PageBitmap::all_true(P)` initializes `ceil(P/64)` words. AND, OR, popcount and scans touch file-sized bitsets. `selected_pages_and_runs` returns both a vector of selected ordinals and a vector of runs. bitmap: `reader/predicate.rs:13`, extraction: `reader/predicate.rs:189`.
- Coarse summaries grow with `P/1024` per column. Prepared-file open (`reader/mod.rs:1509`) reads them for every schema column; request-aware adaptive open (`reader/mod.rs:2835`) can select relevant predicate/equality columns. Distinguish total schema width from queried width and identify the path measured. Fine metadata depends on admitted groups and intermediate candidates, which can be much larger than final candidates.
- Physical plans contain `Vec<PageLocator>` per column, with page ordinal, file offset, byte size and row count. Additional execution representations also retain per-page references. locator plan: `reader/types.rs:621`, execution references: `reader/planner/query.rs:88`.
- Read batching amortizes request/setup overhead. Page headers, codec work and output bytes remain. The existence of contiguous runs does not make decode cost depend only on run count.

A useful measurement decomposition separates total page count P, coarse groups inspected H, detailed metadata bytes M, intermediate candidates K1, final page candidates K2, physical runs R, projected columns C, encoded bytes B and exact selected rows S. The costs can overlap, so report CPU work and wall-clock critical path separately. A constant-S scaling experiment must vary P, and a constant-K2 experiment should separately vary R and C.

### Discovery versus known-row retrieval

The current main path starts with column predicates and discovers page candidates. `RowSelection` is a compact representation used after exact row evaluation; its existence is not evidence of a public `take(row_ids)` retrieval path. A search of the inspected public scan API did not find such an API. row selection: `reader/row_selection.rs:104`, scan options: `scan.rs:79`.

An equal-known-rows control therefore needs a small benchmark adapter. Supply the same logical row IDs or row intervals to every format and include each format's mapping work, codec dependencies and result assembly. For Mica, bisection means ordinal `row_id / configured_rows_per_page` is not generally valid. Either provide a measured row-to-page mapping or disclose that the control supplies already-resolved page locations and tests a narrower stage. Free, precomputed locations for Mica while charging competitors for row mapping would invalidate the comparison.

### Implemented projection modes and their limits

The default combined path still fetches candidate projection data before exact filtering. Two explicit experimental modes now separate the alternatives: `combined_empty_skip` avoids projection decoding for an exactly empty chunk, while `predicate_first` reads predicates, builds exact selections and issues only surviving projection-page reads with overlap reuse. Generic/no-exact-filter/empty-projection cases retain visible fallbacks. The completed bounded study verifies exact outputs, read ordering, issued data ranges and decode work. Public strict aggregate admission remains unsupported; the experiment uses common CPU and process address-space constraints.

The sink-enabled clustered control reduces requested data from 12,498,336 to 376,128 bytes and improves warm latency by 73.01% versus combined-empty-skip. Dispersing the same 2,048 survivors saves no requested data. Real NYC compound-wide saves 4.69% of requested bytes but increases requests from 24 to 150; full dense grouped queries regress by 18.81% in DataFusion and 22.55% in Polars. Read savings are therefore conditional and do not imply a general end-to-end win. Defaults stay conservative. This execution evidence strengthens the physical-selectivity argument without establishing format necessity.

<a id="predicate-first-results"></a>

## Completed predicate-first study: results and paper claims

The final report, manifest, protocol and completion journal are the authority for this study. It is complete under its selected single-query contract; automatic/default promotion was rejected.

Three explicit modes separate combined reads, the combined-empty-skip decode shortcut, and predicate-first read staging. Mode selection is independent of the exact predicate sink. The production configuration remains `combined` with that sink disabled; the following headline comparisons enable the sink in both compared modes. They compare predicate-first with combined-empty-skip, not with the production default or Parquet.

| Recorded case and cache condition | Requested-data or execution evidence | Predicate-first latency change versus combined-empty-skip |
|---|---|---:|
| Clustered synthetic survivors, warm | 12,498,336 to 376,128 requested data bytes; 2,048 surviving rows. | -73.01% |
| Same clustered case, advisory eviction | Observed mean process block reads fall from 13,082,624 to 1,196,032 bytes, including metadata/readahead. | -64.09% |
| Dispersed synthetic survivors, advisory eviction | Same 2,048 surviving rows; no requested-data reduction. | +3.86% |
| NYC compound-wide, advisory eviction | Requested data falls 4.69%; requests rise from 24 to 150. | +1.99% |
| ClickBench Q19 predicate-wide, warm | Requested data falls from 292,716 to 39,171 bytes. | -0.14%, descriptive interval [-0.88%, +0.72%] |
| Dense grouped full query, DataFusion | Same requested data and materialized-page decode counts across modes. | +18.81% |
| Dense grouped full query, Polars | Same requested data and materialized-page decode counts across modes. | +22.55% |

Negative changes mean lower latency. The report includes all cases and descriptive 95% intervals from six paired randomized blocks of five runs per cell. Do not pool synthetic reader cases, real reader cases and full SQL into one headline speedup. The warm NYC dense-wide reader improves 8.77% despite identical I/O and page-decode counts; its cause is unresolved, so it is not evidence of pruning benefit. The final current-versus-historical default comparison retains a +0.38% clustered-control cost with an interval above zero; other intervals cross zero. No regression-free claim is supported.

The accepted measurements total 3,750: 2,160 reader, 900 full-engine, 450 advisory-eviction and 240 actual-default timings. All 72 reader exact cells, 30 engine/layout exact cells and eight final-default exact cells pass; 18 engine traces confirm stage barriers. Invalidated timing attempts remain archived and excluded under the frozen interference rules. These checks establish the selected paths, not arbitrary SQL correctness.

Runs use one CPU and a common 16 GiB process address-space ceiling, with measured RSS. This is not a resident-memory quota, filesystem-cache budget, strict public aggregate admission or concurrent service guarantee. Advisory eviction does not prove cold device caches. The full-engine study includes DataFusion and Polars with two enabled Parquet layouts, 1M/20K and 64K/2K row-group/page targets. The selective-query advantage over those Parquet configurations already exists in combined mode and cannot be attributed to staging. These are whole-system comparisons, not equivalent-information or strongest-format proofs.

**Supported:** exact staging can omit projection-page I/O; equal row retention can produce different physical savings; saved bytes need not improve query latency. This supplies measured execution evidence for S1 and a boundary on S3.

**Not established:** a general staging speedup on the selected real engine queries, new late materialization, the S2a metadata-organization advantage over matched alternatives, the S2b integrated-format advantage, strict aggregate memory admission or an automatic staging policy. First-batch latency, concurrent throughput/tails and reader-reuse deployment behavior were not measured. Keep those separate from completed scoped correctness and performance work.

## Existing measurements and what to reuse

### Full-query framework comparison

The strongest existing system-level evidence is the September comparison CSV, supported by methodology documentation, quality reports and benchmark runner.

Settings are nine common ClickBench/NYC queries, DataFusion 53.1.0 and Polars 0.54.4, 30 measurements per format/engine/query in six blocks, matched 32-thread budgets and affinity, balanced format order, fresh registration/open included, cold data preparation before each execution, direct I/O disabled, and original row order. Parquet is uncompressed with one-million-row groups and 20,000-row pages. Mica uses `v3_single`. The host is ruby2, Xeon Gold 6530, approximately 251.6 GiB RAM, Linux 6.8.0-139, schedutil governor. See the research journal for exact controls.

| Query group | Existing result | What it establishes |
|---|---|---|
| Nine queries within DataFusion | Parquet/Mica median ratios 2.643 to 5.054 | A complete engine path can benefit in this cold configuration. |
| Nine queries within Polars | Ratios 1.057 to 5.355 | Benefits depend on query and engine; Q41 is near parity. |
| All measured outputs | Archived report says 1,080 exact logical outputs checked, including multiplicity and ordering where required | Stronger correctness evidence than row counts. It covers these inputs and queries. |

Reuse the benchmark methodology and exact-output verifier. Preserve the old table as historical evidence; rerun after implementation/baseline changes and add compressed, tuned alternatives and held-out parameters. A full refresh is necessary before a submission-wide headline. Do not combine this range with single-core reader results. Query output row counts after aggregation/LIMIT are not scan selectivity.

### Metadata and execution ablation

The ablation summary reports 1,040 profiles across 16 workloads. Raw JSON exists at `exp/mica-reader-ablation/results/raw/`. The inspected current-default ClickBench artifact records five cold iterations, core 2, direct I/O disabled, adaptive metadata, sparse secondary indexes and adaptive-v1 data-read policy. The runner and setup documentation document host preparation and the 1 GiB pre-read.

Relative to current, aggregate geomean latency ratios are 1.390 for eager metadata, 1.181 for forced generic execution, 1.031 for static data policy and 1.008 for legacy bitmap ordering. Full-materialization/generic lanes have larger effects but change several mechanisms simultaneously. Byte-exact cap splitting is faster than current in aggregate at 0.957, and on the NYC full-filter workload at 0.736.

Reuse the raw profiles to select diagnostic cases and avoid overemphasizing nearly neutral policies. Repeat matched one-factor ablations and interactions under the final exact-output and baseline configuration. These measurements support sparse metadata access much more directly than they support every adaptive policy.

### Granularity diagnosis

The May 11 journal analysis and nine locally present profile JSON files under `dataset/prepared/native-format-bench/nyc-fhv-guardrail/analysis/analysis_20260511_parquet_granularity_structural_diagnosis/` provide a useful motivating case.

For the same NYC point-query workload in the recorded uncompressed, original-order cold experiment, Parquet with one-million-row groups increased from 9.773 ms median latency at a 20,000-row page target to 195.863 ms at a 200-row target, while selected decode rows fell from 40,960 to 19,880. These medians establish the motivating tradeoff in that reader, not a universal format limitation.

For the NYC point query, the recorded Mica profile reduces 59,543 pages to 100 after zone maps and 6 after membership refinement; the median is 2.460 ms over five cold iterations, with 25,016 deferred Bloom bytes and 288 page-index bytes. Parquet's 1M-row-group/200-row-page diagnostic profile spends 216.863 ms opening/building metadata and 25.348 ms evaluating page indexes, versus 2.39 MiB of data reads. That Parquet breakdown is one profile iteration, not a robust median. Smaller pages clearly exposed software cost in that implementation; the result does not establish an unavoidable lower bound for Parquet.

Reuse as a reason to run the controlled granularity experiment. Rebuild with compressed alternatives, tuned current readers, matching membership information where possible, independent metadata residency and exact query outputs. Show direct phase measurements before calling any cost format-imposed.

### Other experiments

| Existing experiment | What remains useful | Why it does not settle the revised question |
|---|---|---|
| Cold reader benchmark | Exact/coarse contracts, native Lance and Mica-matched Lance lanes, Parquet variants; raw outputs are present | Mostly uncompressed and selected workloads; reader latency is not full-query latency. Re-run decisive baselines in final configuration. |
| Warm page-cache study | `mincore` before/after accounting and warm comparisons | Measures whole input-tree OS residency. It does not independently budget parsed metadata, metadata bytes and data bytes, nor demonstrate cache hit rates under a changing query working set. |
| Cap sweep | Existing workload dependence and dense losses | Does not support a universal 256 KiB optimum or saturation guarantee. Use for sensitivity and failure cases. |
| In-memory study | Candidate materialization cost and exact/coarse distinction | Candidate materialization is not peak full-query memory; streaming output and concurrent requests change the memory contract. |
| Large-strided-read motivation | A starting point for a hardware diagnostic | Existing blocking padded reads versus precise batched reads confound bytes, overlap and concurrency. Replace the motivating claim with deduplicated, API-matched controls. |
| Scheduler studies | Negative results caution against adding scheduling as an assumed contribution | Historical scheduler had approximately parity aggregate results across tested multifile regimes. This neither proves all scheduling useless nor supports adding an unevaluated scheduler to the paper. |

## Artifact availability audit

The commit named `clean up results` did not remove these artifacts. Its only change is three `.gitignore` lines, including `*/**/results`. Inspection on 2026-09-28 found the following local files, counting all recursively nested regular files.

| Directory | Files | JSON | CSV |
|---|---:|---:|---:|
| `eval/framework-comparison/results/2026-09-08-fair-cold` | 1,426 | 1,327 | 26 |
| `exp/mica-reader-ablation/results` | 54 | 28 | 0 |
| `exp/mica-cap-sweep/results` | 120 | 60 | 0 |
| `exp/cold-read/results` | 151 | 37 | 21 |
| `exp/warm-page-cache-size/results` | 209 | 87 | 25 |
| May 11 granularity analysis directory | 9 | 9 | 0 |

Presence is not a checksum or provenance audit. Raw directories are ignored, so a clean checkout need not contain them. Create an explicit artifact release with input identities, executable/source hashes, query definitions, commands, controls and raw outputs. Preserve historical versions rather than overwriting them during reruns. Old absolute prefixes in raw paths need a documented relocation mapping.

## Consequences for the new research plan

The code and historical measurements support centering the paper on making fine-grained pruning economical through metadata organization and reader execution. Establishing this systems contribution does not require a new index algorithm, unique necessity of alignment, or a new-format impossibility argument. The evidence also does not support survivor-only complexity or universal sparse-query benefit. Remaining studies must establish the relative advantage, its cause and its useful operating region.

The main discriminating evidence still needed is equivalent-information competing designs, controlled metadata residency, locality/correlation sweeps, and a decomposition that distinguishes discovery from known-row retrieval. Add wide-column and FSST-dependent cases to test shared partition and codec costs. Count per-file rollover in scale experiments. Use the completed explicit-stage tradeoff results when discussing projection I/O. New metadata levels, policies and further integration remain conditional on separate evidence; the staging study does not replace the discriminating metadata/layout comparisons.

---

## Vault Navigation & MoC Context

- [[Mica]]: Central Level 3 Project Hub for Mica paper notes and core concepts.
- [[README|Mica Plan Overview]]: Master roadmap and synthesis of the SOSP/OSDI research plan.
- [[storyline|Mica Storyline]]: Proposed SOSP/OSDI research storyline and core claims S1–S3.
- [[prior-art|Mica Prior Art]]: Primary-source positioning and novelty analysis.
- [[experiments|Mica Experiments]]: Comprehensive experimental campaign E00–E09.
- [[design-extensions|Mica Design Extensions]]: Infrastructure requirements and conditional architecture extensions.
- [[stress-test|Mica Stress Test]]: Stress-test ledger and falsification criteria.

