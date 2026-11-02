---
tags: []
created: 2026-11-02
description: Master glossary and Map of Content for core Mica columnar storage concepts, NVMe I/O mechanics, and pruning algorithms.
aliases:
  - Mica Concepts
  - Concepts
---

# Concepts

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

- [[Mica]]: Parent Mica project hub.
