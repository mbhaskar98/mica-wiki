---
tags: []
created: 2026-10-15
description: Analysis of the architectural mismatch between scan-oriented columnar formats and selective queries on modern NVMe drives.
---

# 1 Introduction: The Hardware & Software Mismatch

## Legacy Design Flaw

* Analytical formats like [[Parquet]] are optimized for large sequential scans.
* Real-world queries are highly selective. Most filters drop 80 to 100 percent of rows.
* Standard readers fetch, decode, and track massive data blocks just to extract a handful of surviving rows.

## The Hardware Shift

* Modern NVMe storage is no longer the bottleneck.
* Using deep hardware queues and kernel async I/O (like `io_uring`), NVMe drives process thousands of small random reads in parallel cheaply.

## The [[Granularity Wall]] in Practice

* Shrinking legacy data chunks to leverage NVMe capabilities creates a severe systems problem.
* Physical bytes read drop, but end-to-end latency spikes by over an order of magnitude.
* The bottleneck moves to the CPU. Software gets crushed by the metadata loading, memory allocations, and I/O planning required for thousands of tiny reads.

## The Solution: Co-Design

* [[Mica]] is a coupled format and reader runtime. Neither works alone.
* **The Format:** Natively supports fine-grained, independently addressable pages.
* **The Runtime:** Uses a [[Single Page Bitmap|single page bitmap]] for universal I/O planning. One bit decides a page's fate across every column at once.
* **Metadata and I/O:** [[Layered Zone Maps]] avoid loading irrelevant page metadata, while [[Bounded IO Coalescing|Bounded I/O Coalescing]] reduces the number of small read requests.
* **Index Selection:** [[Cost-Gated Secondary Indexes]] let the reader skip an index when scanning the targeted pages is estimated to be cheaper.
* **The Impact:** Software overhead scales only with the data that survives the filter, not the total number of pages in the file.

## Evaluation Highlights

* **Performance Speedup:** The paper reports that [[Mica]] achieves a 2.2× to 22.6× speedup over the best-tuned versions of [[Parquet]] and [[Lance]] across seven selective queries on the NYC Taxi and ClickBench datasets.
* **Memory Footprint Reduction:** By pruning data before it is read from NVMe storage and materialized in memory, Mica reduces the intermediate Arrow representation by up to four orders of magnitude, according to the paper.
* **Example:** Mica materializes only 2,000 rows compared with Parquet's 50,000—a 96% reduction in materialized rows. This row-count comparison does not by itself establish a 96% reduction in total RAM usage, and is separate from the reported maximum reduction above.

Next: [[2 Background and Target Regime]] · Index: [[Mica]]
