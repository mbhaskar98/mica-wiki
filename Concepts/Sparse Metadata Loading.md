---
tags: []
created: 2026-10-15
description: Selective reading of only those pruning metadata blocks relevant to candidate data regions.
---

# Sparse Metadata Loading

* Reading only the pruning metadata relevant to a query, skipping metadata for regions that can already be ruled out.
* Pruning data and pruning metadata are different tasks. Tiny data pages can reduce unnecessary data reads while creating a large amount of page-level metadata to inspect.
* Section 3 identifies insufficient format support in Parquet for efficiently pruning the pruning metadata as one cause of the [[Granularity Wall]]. This does not mean every reader always reads every metadata byte.
* Mica's [[Layered Zone Maps]] use an in-memory coarse summary to reject blocks before fetching their finer page-level metadata.
* The goal is to keep metadata loading and planning from overwhelming the savings achieved by fine-grained data pruning.

Related: [[Page Indexes]], [[Bloom Filters]].

Paper context: [[3 Granularity Wall#Growing Metadata Without Efficient Sparse Loading|§3: Growing metadata without efficient sparse loading]].
