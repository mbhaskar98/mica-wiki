---
tags: []
created: 2026-10-15
description: First-tier metadata providing min/max statistics for groups of pages to quickly eliminate large irrelevant data regions.
aliases:
  - CZM
---

# Coarse Zone Maps

* The coarse level of Mica's [[Layered Zone Maps]]: one min/max entry for a group of consecutive pages in a particular column.
* The configurable page-group size `G` defaults to **1,024 pages per entry**. It counts pages, not rows.
* The lightweight coarse map is cheap enough to load even on each cold read, then use in memory to reject groups before loading their [[Fine Zone Maps|fine metadata]]. It need not be permanently resident across queries.
* A group whose min/max range overlaps the predicate remains a candidate; overlap does not guarantee a matching row.
* Although a coarse entry covers multiple pages, its result maps to page IDs, preserving Mica's common unit for pruning.
* The ClickBench example has about 51 thousand coarse entries; §4.3 reports roughly 0.8 MiB for CZM versus 800 MiB for FZM. The earlier table labels the approximate sizes MB.
* Reducing `G` increases coarse metadata entries but does not change page boundaries, column-data segmentation, or data byte sizes. Coarse pruning granularity is independent of [[Rows Per Page|data-page granularity]].

Related: [[Sparse Metadata Loading]], [[Single Page Bitmap]].

Paper context: [[4 Mica - File Format Design#4.3 Layered Pruning Metadata|§4.3 Layered pruning metadata]].
