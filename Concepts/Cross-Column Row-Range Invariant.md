---
tags: []
created: 2026-10-15
description: Structural guarantee that a shared logical page ID spans identical row intervals across all columns in a table.
aliases:
  - Shared Page Domain
---

# Cross-Column Row-Range Invariant

* In Mica, the same page ID covers exactly the same contiguous row range across all columns.
* Page 42 in Date and Page 42 in Price contain values for the same rows. Their values and encoded byte lengths need not be identical.
* [[Rows Per Page]] is a cap; different page IDs can cover different numbers of rows while alignment across columns remains intact.
* This lets a [[Single Page Bitmap]] carry a page selection across columns without the per-column remapping required by [[Parquet Layout|Parquet's unaligned pages]].
* The invariant removes that [[Row-Range Translation|row-range translation]] mismatch, not all address calculations or filtering within candidate pages.
* The paper calls this a **shared page domain**. If any column exceeds the page-size limit, [[Recursive Page Bisection]] splits the logical row range for every column together.
* [[Variable Physical Page Layout]] preserves that row alignment while allowing different encoded byte sizes. Each column's page index supplies physical offsets and lengths.

Related: [[Independent Addressability]], [[Granularity Wall]].

Paper context: [[4 Mica - File Format Design#4.1 Shared Page Domain Across Columns|§4.1 Shared page domain]].
