---
tags: []
created: 2026-10-15
description: Configurable limit capping the maximum number of logical rows contained within a single Mica page.
aliases:
  - RPP
---

# Rows Per Page

* Mica's rows-per-page (RPP) setting controls page granularity. The paper gives a default of **200 rows**.
* RPP is an upper bound, not a guarantee that every page contains exactly that many rows.
* If any column exceeds the default **16 MiB page-size limit**, [[Recursive Page Bisection]] halves the logical row range across all columns and repeats as needed, reducing the actual row count.
* Pages must preserve the [[Cross-Column Row-Range Invariant]]: the same page ID covers the same rows in every column despite possible variation between pages.
* Do not infer a page's row range simply by multiplying its ID by 200 when pages can have fewer rows.
* Smaller pages can improve pruning precision but increase the number of metadata entries and reads to manage, the tradeoff behind the [[Granularity Wall]].
* RPP affects data-page granularity. The coarse zone-map group size `G` affects only metadata granularity; changing `G` does not split data pages.

Paper context: [[4 Mica - File Format Design#The Page as the Basic I/O Unit|§4: The page as the basic I/O unit]].
