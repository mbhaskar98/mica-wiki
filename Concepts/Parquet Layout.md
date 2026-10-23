---
tags: []
created: 2026-10-15
description: Structural breakdown of Apache Parquet into row groups, column chunks, and independent data pages.
---

# Parquet Layout

* **Row group:** A contiguous row range shared across columns.
* **Column chunk:** The data for one column within a row group.
* **Data page:** A subdivision of a column chunk. Pages are local to that chunk, and their row boundaries need not align with pages in other columns.
* Optional [[Bloom Filters]] support membership pruning at the column-chunk/row-group level. Optional [[Page Indexes]] support pruning individual pages.
* A page selected in one column must be mapped through row ranges to identify the corresponding reads in other columns: [[Row-Range Translation]].
* Smaller units can improve pruning precision while increasing metadata and planning work, producing the [[Granularity Wall]] observed in the paper's experiment.

Related: [[Parquet]], [[Single Page Bitmap]].

Paper context: [[3 Granularity Wall#Parquet's File Layout and Pruning Units|§3: File layout and pruning units]].
