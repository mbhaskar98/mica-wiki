---
tags: []
created: 2026-10-15
description: Central index and Map of Content for Mica paper notes, SOSP/OSDI research plan, and core concepts.
---

# Mica

## Paper Notes

- [[0 Abstract]]: Summary of the Granularity Wall in legacy columnar formats and Mica's page-addressable hardware-software co-design.
- [[1 Introduction-The Hardware & Software Mismatch|1 Introduction: The Hardware & Software Mismatch]]: Analysis of the architectural mismatch between scan-oriented columnar formats and selective queries on modern NVMe drives.
- [[2 Background and Target Regime]]: Definition of the workload selectivity and NVMe storage regime required for Mica's fine-grained I/O advantages.
  - [[2 Background and Target Regime#2.1 Selectivity|2.1 Selectivity]]: Target workload conditions where high data selectivity permits skipping large portions of storage.
  - [[2 Background and Target Regime#2.2 NVMe-class Storage|2.2 NVMe-class Storage]]: Storage hardware profile characterized by high parallel queue depths and low latency for small reads.
  - [[2 Background and Target Regime#2.3 Software Stack for Batched Disk I/O|2.3 Software Stack for Batched Disk I/O]]: Asynchronous and batched kernel I/O mechanisms required to keep NVMe queues saturated.
- [[3 Granularity Wall]]: Empirical evaluation demonstrating how shrinking Parquet page sizes causes severe metadata and CPU execution bottlenecks.
- [[4 Mica - File Format Design|4 Mica: File Format Design]]: Detailed specification of Mica's file format including shared page domains, layered zone maps, and detail blocks.
  - [[4 Mica - File Format Design#4.1 Shared Page Domain Across Columns|4.1 Shared Page Domain Across Columns]]: Shared logical row boundaries across columns eliminating row-range translation.
  - [[4 Mica - File Format Design#4.2 Variable Physical Page Layout|4.2 Variable Physical Page Layout (editorial title)]]: Variable physical page byte sizes per column with independent addressability via page indexes.
  - [[4 Mica - File Format Design#4.3 Layered Pruning Metadata|4.3 Layered Pruning Metadata]]: Staged metadata pruning using coarse and fine zone maps to prevent metadata reading bottlenecks.
  - [[4 Mica - File Format Design#4.4 Per-Column Detail Blocks|4.4 Per-Column Detail Blocks]]: Detail block storage for fine zone maps, Bloom filters, presence bitmaps, and column dictionaries.
  - [[4 Mica - File Format Design#4.5 Page-Local Decode Self-Containment|4.5 Page-Local Decode Self-Containment]]: Self-contained page decoding using local page bytes and shared column state without cross-page dependencies.

## Experiments

- [[Projects/mica/experiments/E01-Test1|E01-Test1 — Data preparation]]: Original and new data locations, 19 completed configurations, three blocked cases, current scope, and batch commands.
- [[Projects/mica/experiments/E01-Test2|E01 — Test 2: Mica metadata loading]]: Completed NYC and ClickBench checklist covering 40 test groups, four metadata/index settings, output validation, and individual/combined report commands.
- [[Projects/mica/experiments/commands|Commands]]: Remote prerequisites, release build commands, and output paths for the preparation binaries.

## Workarounds

- [[Projects/mica/workarounds/Remote Dev Setup and Resync|Remote Dev Setup and Resync]]: Two-step rsync workflow to synchronize local codebase and vendored dependencies to remote nodes without .gitignore filtering bugs.
- [[Projects/mica/workarounds/Vendored Lance Build Fix|Vendored Lance Build Fix]]: Defensive dummy-file scaffolding workaround to bypass Cargo manifest parser failures for missing unused vendored binaries.

## Research & Publication Plan (mica-plan)

- [[README|Mica Plan Overview]]: Master roadmap and synthesis of the SOSP/OSDI research plan, experiment matrix, and evidence for Mica fine-grained columnar pruning.
- [[storyline|Mica Storyline]]: Proposed SOSP/OSDI research storyline, core claims S1–S3, and format justification for economical fine-grained pruning.
- [[prior-art|Mica Prior Art]]: Primary-source positioning and novelty analysis comparing Mica against SMA, Big Metadata, ORC, Parquet, Vortex, Lance, FastLanes, Nimble, and Pixels.
- [[experiments|Mica Experiments]]: Comprehensive experimental campaign E00–E09 evaluating granularity sweeps, baseline comparisons, metadata lifecycle, and engine queries.
- [[evidence|Mica Evidence]]: Implementation status audit and empirical evidence synthesis reconciling code capabilities with the completed predicate-first bounded study.
- [[design-extensions|Mica Design Extensions]]: Infrastructure requirements and conditional architecture extensions triggered by measured reader bottlenecks or resource limits.
- [[stress-test|Mica Stress Test]]: Stress-test ledger documenting rejected narrative candidates, two rounds of adversarial review, and falsification criteria.

## Concepts

- [[Parquet]]: Standard open-source columnar storage format designed for large-scale sequential batch analytics.
- [[Lance]]: Modern columnar data format optimized for random access, vector search, and selective machine learning workloads.
- [[Granularity Wall]]: Performance tipping point where reducing chunk size to save I/O is overwhelmed by metadata parsing and scheduling overheads.
- [[Single Page Bitmap]]: Shared bit vector tracking surviving page candidates across all columns to eliminate row-translation overhead.
- [[Layered Zone Maps]]: Two-tier metadata architecture combining coarse and fine zone maps to prevent metadata reading bottlenecks.
- [[Bounded IO Coalescing|Bounded I/O Coalescing]]: Optimization that merges nearby small reads into a single I/O request while strictly limiting wasted data transfer.
- [[Cost-Gated Secondary Indexes]]: Adaptive decision mechanism that loads secondary indexes only when estimated lookup cost is lower than scanning data pages.
- [[IO Selectivity|I/O Selectivity]]: Fraction of total physical dataset bytes that storage readers actually read from disk to evaluate a query.
- [[Data Selectivity]]: Fraction of dataset rows that satisfy a query's filter predicates and survive to downstream execution.
- [[Data Clustering]]: Physical sorting and co-location of related table rows to maximize the effectiveness of storage pruning.
- [[Predicate Pushdown]]: Query execution optimization that transfers filter predicates down to the storage layer to prune irrelevant data early.
- [[NVMe-class Storage]]: Solid-state storage devices offering high queue depths, deep parallelism, and fast random read capabilities over PCIe.
- [[IOPS]]: Measure of storage performance indicating the number of discrete read or write operations completed per second.
- [[Queue Depth]]: Number of pending, in-flight I/O requests submitted to a storage device concurrently.
- [[Blocking IO|Blocking I/O]]: Synchronous I/O model where the issuing thread halts until the storage operation completes.
- [[Batched Asynchronous IO|Batched Asynchronous I/O]]: Technique for submitting and completing batches of non-blocking I/O requests to saturate NVMe drive parallelism.
- [[io_uring]]: High-performance Linux asynchronous I/O framework utilizing lockless ring buffers shared between user space and kernel.
- [[Parquet Layout]]: Structural breakdown of Apache Parquet into row groups, column chunks, and independent data pages.
- [[Bloom Filters]]: Probabilistic membership data structures used for fast rejection of non-matching values at row-group or page granularity.
- [[Page Indexes]]: Column-chunk metadata tables detailing file offsets, byte sizes, and column statistics for individual data pages.
- [[Row-Range Translation]]: Overhead in traditional columnar formats of translating filtered row boundaries from one column into byte offsets in another.
- [[Sparse Metadata Loading]]: Selective reading of only those pruning metadata blocks relevant to candidate data regions.
- [[Coarse Zone Maps]]: First-tier metadata providing min/max statistics for groups of pages to quickly eliminate large irrelevant data regions.
- [[Fine Zone Maps]]: Second-tier metadata providing min/max statistics for individual pages within candidate page groups.
- [[Rows Per Page]]: Configurable limit capping the maximum number of logical rows contained within a single Mica page.
- [[Independent Addressability]]: Ability to directly compute the file location of any page or metadata record without sequentially scanning preceding blocks.
- [[Cross-Column Row-Range Invariant]]: Structural guarantee that a shared logical page ID spans identical row intervals across all columns in a table.
- [[Recursive Page Bisection]]: Write-time algorithm that recursively halves page row ranges across all columns whenever encoded data exceeds page size limits.
- [[Variable Physical Page Layout]]: Storage layout pairing fixed logical row boundaries with variable encoded byte lengths per column.
- [[Page-Level Membership Pruning]]: Per-page data structures, such as Bloom filters or presence bitmaps, used to determine if queried values exist on a page.
- [[Presence Bitmaps]]: Exact membership bit vectors mapped against a dictionary to prune pages without false positives in low-cardinality columns.
- [[Page-Local Decode Self-Containment]]: Guarantee that a page can be decoded using only its own bytes and static column-level dictionary state.
- [[Run-Length Encoding]]: Compression technique that stores sequences of identical consecutive values as single value-count pairs.
