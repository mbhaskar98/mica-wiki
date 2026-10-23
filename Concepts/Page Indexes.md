---
tags: []
created: 2026-10-15
description: Column-chunk metadata tables detailing file offsets, byte sizes, and column statistics for individual data pages.
---

# Page Indexes

* Optional Parquet metadata describing data pages within a column chunk, including page-level min/max statistics used for pruning.
* A range predicate can reject pages whose min/max values fall outside the requested range. A timestamp point predicate can similarly reject pages whose intervals exclude that timestamp.
* Pages that cannot be rejected remain candidates; their rows may still need filtering after reading.
* A selected page is local to its column chunk, not a shared page ID across columns. [[Row-Range Translation]] is needed to carry its row selection into other columns.
* Smaller pages can improve pruning precision while increasing the amount of metadata and planning work, as shown in the [[Granularity Wall]] experiment.

Related: [[Parquet Layout]], [[Bloom Filters]], [[Layered Zone Maps]].

## In Mica

* Mica's per-column page index stores each page's **file offset and byte size**, supporting a [[Variable Physical Page Layout]] without uniform-page padding.
* The index resides in the column's Detail Block. A shared page ID selects the logical page; the index supplies the physical location and length for that column.
* Mica's per-page min/max summaries reside separately in [[Fine Zone Maps]]. Physical addressing and min/max pruning serve different purposes.

Mica context: [[4 Mica - File Format Design#4.4 Per-Column Detail Blocks|§4.4 Per-column detail blocks]].

Paper context: [[3 Granularity Wall#Parquet's File Layout and Pruning Units|§3: File layout and pruning units]].
