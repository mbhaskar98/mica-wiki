---
tags: []
created: 2026-10-15
description: Summary of the Granularity Wall in legacy columnar formats and Mica's page-addressable hardware-software co-design.
---

# Mica: Page-Addressable Columnar Format

## The Problem: The Granularity Wall

* Standard formats like [[Parquet]] process data in massive chunks. Highly selective queries waste resources loading and decoding irrelevant rows.
* Modern NVMe drives support thousands of tiny random reads. However, shrinking Parquet's chunk size destroys software performance.
* This software bottleneck is the [[Granularity Wall]]. The CPU spends all its time mapping individual surviving row numbers to exact byte offsets in subsequent columns instead of processing data.

## The Solution: Page-Addressable Architecture

* [[Mica]] is a new columnar format built around strict, system-wide alignment.
* Data is stored in small units called Pages. A Page ID maps to the exact same rows across every single column in the table.
* If a filter drops Page 42 in the first column, the system clears bit 42 in the [[Single Page Bitmap]]. Subsequent columns use that shared map to skip Page 42.
* Supporting mechanisms include [[Layered Zone Maps]] for pruning metadata, [[Bounded IO Coalescing|Bounded I/O Coalescing]] for combining reads, and [[Cost-Gated Secondary Indexes]] for deciding when an index is worth loading.

## The Results

* Reads as little as 0.08% of total data on highly selective queries.
* Runs 2.2 to 22.6x faster than highly tuned versions of [[Parquet]] and [[Lance]].
