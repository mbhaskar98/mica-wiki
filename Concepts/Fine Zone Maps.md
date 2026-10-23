---
tags: []
created: 2026-10-15
description: Second-tier metadata providing min/max statistics for individual pages within candidate page groups.
aliases:
  - FZM
---

# Fine Zone Maps

* The fine level of Mica's [[Layered Zone Maps]]: one min/max entry for each page in each column.
* Relevant fine metadata is loaded after [[Coarse Zone Maps]] rule out irrelevant groups, rather than loading the entire fine map for every query.
* Fine entries let the reader reject individual pages whose value ranges cannot satisfy a predicate. Pages that remain candidates can still contain nonmatching rows.
* The reported ClickBench example has about 52.5 million fine entries. Section 4.3 describes the size as roughly 800 MiB, while the earlier table labels its approximate size MB. This motivates [[Sparse Metadata Loading]].
* Fine metadata and the actual data pages are separate parts of the file; ruling out a page can avoid reading its data.
* An upper layer may optionally pre-warm FZM, accepting the memory cost. Mica also targets cold reads without loading the entire fine map unconditionally.

Related: [[Single Page Bitmap]], [[Rows Per Page]].

Paper context: [[4 Mica - File Format Design#4.3 Layered Pruning Metadata|§4.3 Layered pruning metadata]].
