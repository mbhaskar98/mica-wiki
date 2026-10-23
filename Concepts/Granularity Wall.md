---
tags: []
created: 2026-10-15
description: Performance tipping point where reducing chunk size to save I/O is overwhelmed by metadata parsing and scheduling overheads.
---

# The Granularity Wall

* The performance barrier you hit when you shrink data chunks to minimize wasted disk reads.
* In the paper's smaller-page experiment, rows selected for reading decrease while latency rises by over an order of magnitude. Finer pruning does not necessarily mean faster execution.
* The bottleneck shifts directly from disk I/O into the software system.
* The CPU gets crushed by per-unit bookkeeping. The overhead of managing and pruning metadata for thousands of tiny chunks grows faster than the irrelevant data those chunks remove.

## Evidence and Causes

* [[3 Granularity Wall#Smaller Units: Fewer Reads, Higher Latency|Section 3's measurements]] reduce actual data reads from 1.44 MiB to 0.14 MiB across three configurations, while metadata loading and planning rises from 5 ms to 392 ms.
* [[Sparse Metadata Loading]] addresses the cost of fetching and inspecting increasingly large pruning metadata.
* [[Row-Range Translation]] adds work because Parquet's page selections are local to individual column chunks.

## How Mica Addresses It

* [[Single Page Bitmap]] reduces repeated tracking of surviving pages across columns.
* [[Layered Zone Maps]] avoid loading fine-grained metadata for irrelevant blocks.
* [[Bounded IO Coalescing|Bounded I/O Coalescing]] reduces read-request overhead while limiting extra bytes read.
* [[Cost-Gated Secondary Indexes]] avoid index reads when a direct scan is estimated to be cheaper.

Paper context: [[3 Granularity Wall]].
