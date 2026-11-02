---
tags: []
created: 2026-10-15
description: Chapter and section breakdown of the original Mica ATC'26 research paper, file format designs, and empirical evaluation.
aliases:
  - Original Paper
  - OriginalPaper
---

# Original Paper

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
- [[7 Evaluation]]: Empirical evaluation setup, hardware testbed specifications, dataset query matrix, and baseline configurations for Mica, Parquet, and Lance.

- [[Mica]]: Parent Mica project hub.
