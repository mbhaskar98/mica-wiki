---
tags: []
created: 2026-10-15
description: Write-time algorithm that recursively halves page row ranges across all columns whenever encoded data exceeds page size limits.
---

# Recursive Page Bisection

* Mica's writer starts with a common row range within the [[Rows Per Page|RPP]] cap. If any column exceeds the default **16 MiB page-size limit**, it bisects that range for every column.
* The writer repeats this process for resulting ranges that remain too large, preserving the [[Cross-Column Row-Range Invariant|shared page domain]].
* For example, a 200-row range becomes two 100-row ranges across both a wide string column and a narrow numeric column, even if only the string column exceeded the limit.
* Splitting the logical range does not force equal encoded byte lengths or fixed-size padding. Mica uses a [[Variable Physical Page Layout]].
* This adds write-time coordination and potentially more per-page overhead to avoid cross-column row-range translation during reads.

Paper context: [[4 Mica - File Format Design#4.1 Shared Page Domain Across Columns|§4.1 Shared page domain]].
