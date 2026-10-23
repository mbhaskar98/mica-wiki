---
tags: []
created: 2026-10-15
description: Probabilistic membership data structures used for fast rejection of non-matching values at row-group or page granularity.
---

# Bloom Filters

* A membership-pruning structure used to answer whether a tested value may be present.
* In the [[Parquet Layout]], a Bloom filter is associated with a column chunk: one column within one row group.
* In Parquet, a **miss** rules out that row group for the tested value. A **hit** means the value may be present; it does not prove a match or identify which data page contains it.
* Making row groups smaller makes this pruning more fine-grained but creates more column chunks and associated metadata.
* Parquet Bloom filters are optional: the writer must include them, and the reader must use them for pruning.

## In Mica

* [[4 Mica - File Format Design|Section 4]] places Bloom filters in the Detail Block as metadata associated directly with individual pages per column.
* This changes the pruning scope from Parquet's column chunk to a Mica page. A hit still means only that the tested value may be present.
* At write time, high-cardinality columns receive per-page Bloom filters; low-cardinality columns use exact [[Presence Bitmaps]] instead. The threshold is configurable, and column metadata identifies the chosen structure.
* [[Page-Level Membership Pruning]] produces page candidates directly compatible with zone-map candidates under the shared page domain.

Related: [[Page Indexes]], [[Predicate Pushdown]], [[Granularity Wall]].

Paper context: [[3 Granularity Wall#Parquet's File Layout and Pruning Units|§3: File layout and pruning units]].
