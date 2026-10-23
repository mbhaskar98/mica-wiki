---
tags: []
created: 2026-10-15
description: Per-page data structures, such as Bloom filters or presence bitmaps, used to determine if queried values exist on a page.
---

# Page-Level Membership Pruning

* Checks whether a queried value can occur in a particular page, allowing the reader to skip pages that cannot match.
* Mica chooses the structure per column using a configurable write-time cardinality threshold. Cardinality is the number of distinct values.
* **High cardinality:** Per-page [[Bloom Filters]], with possible false positives on hits.
* **Low cardinality:** [[Presence Bitmaps]] backed by a column-wide sorted dictionary, giving exact page-level membership.
* A column uses one of these two membership structures; column metadata identifies the choice.
* With the [[Cross-Column Row-Range Invariant|shared page domain]], membership candidates can be combined directly with zone-map candidates using page IDs.
* Intersecting page candidates for an AND predicate does not establish a matching row: the two values could occur in different rows of the same page.

Related: [[Single Page Bitmap]], [[Cost-Gated Secondary Indexes]].

Paper context: [[4 Mica - File Format Design#4.4 Per-Column Detail Blocks|§4.4 Per-column detail blocks]].
