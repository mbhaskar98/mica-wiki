---
tags: []
created: 2026-10-15
description: Shared bit vector tracking surviving page candidates across all columns to eliminate row-translation overhead.
---

# The Single Page Bitmap

* Instead of building a complex list of surviving row numbers and calculating byte offsets for every column, the reader uses a simple array of bits (1s and 0s).
* Each bit represents one page. If the filter logic decides Page 42 has no matching data, it flips bit 42 to 0.
* In [[Mica]], a page ID refers to the same rows across every column: the [[Cross-Column Row-Range Invariant]]. The reader checks this shared bitmap when reading subsequent columns; if a bit is 0, it skips that page entirely.
* This reduces the repeated bookkeeping behind the [[Granularity Wall]].
* A survivor bit represents a page ID. This differs from [[Presence Bitmaps]], whose bits represent dictionary values present within one page.
* For an AND predicate, page-level candidate sets from different columns can be intersected directly. A surviving page may still need row-level filtering to establish that the predicates match the same row.

Related: [[Layered Zone Maps]], [[Bounded IO Coalescing|Bounded I/O Coalescing]], [[Cost-Gated Secondary Indexes]].
