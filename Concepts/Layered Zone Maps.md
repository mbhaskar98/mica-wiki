---
tags: []
created: 2026-10-15
description: Two-tier metadata architecture combining coarse and fine zone maps to prevent metadata reading bottlenecks.
---

# Layered Zone Maps (Pruning the Metadata)

* Tiny pages generate a large amount of metadata, such as min/max values for every page. Reading all of that metadata from disk would recreate the [[Granularity Wall]].
* [[Mica]] splits the metadata into [[Coarse Zone Maps]] (one min/max entry per page group per column) and [[Fine Zone Maps]] (one min/max entry per page per column). The coarse map is loaded first, including on cold reads, and used in memory to prune groups.
* If the coarse map rules out a block for the target data, the reader never loads the fine-grained metadata for the pages inside that block.
* This lets the reader prune the metadata itself before inspecting individual pages.
* This is an example of [[Sparse Metadata Loading]], addressing one of the costs identified in [[3 Granularity Wall]].
* The coarse grouping parameter `G` defaults to 1,024 pages. Changing it changes coarse metadata granularity without changing the data-page layout.
* Full FZM pre-warming is an optional upper-layer optimization with a memory cost, not a prerequisite for Mica's reader.

Related: [[Single Page Bitmap]], [[IO Selectivity|I/O Selectivity]], [[Data Clustering]], [[Predicate Pushdown]].

File layout and size example: [[4 Mica - File Format Design#Two-Level Zone Maps|§4: Two-level zone maps]].

Cold reads and granularity: [[4 Mica - File Format Design#4.3 Layered Pruning Metadata|§4.3 Layered pruning metadata]].
