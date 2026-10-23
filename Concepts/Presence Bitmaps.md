---
tags: []
created: 2026-10-15
description: Exact membership bit vectors mapped against a dictionary to prune pages without false positives in low-cardinality columns.
---

# Presence Bitmaps

* Mica's exact membership structure for low-cardinality columns combines a column-wide sorted dictionary with a presence bit vector for each page.
* A bit corresponds to a dictionary value and records whether that value occurs in the page. This avoids Bloom-filter false positives.
* It identifies value presence, not the row positions where the value occurs. Multiple conditions may still require row-level filtering.
* It differs from the [[Single Page Bitmap]]: **presence bits represent dictionary values within a page; query survivor bits represent page IDs**.
* The writer selects this structure or [[Bloom Filters]] per column using a configurable cardinality threshold.

Related: [[Page-Level Membership Pruning]].

Paper context: [[4 Mica - File Format Design#4.4 Per-Column Detail Blocks|§4.4 Per-column detail blocks]].
