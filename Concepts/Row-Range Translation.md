---
tags: []
created: 2026-10-15
description: Overhead in traditional columnar formats of translating filtered row boundaries from one column into byte offsets in another.
---

# Row-Range Translation

* Converting a selection in one column into row ranges, then using those ranges to locate the corresponding pages and read locations in another column.
* [[Parquet Layout|Parquet pages]] need not align across columns. For example, a date page covering rows 1–500 could overlap several price pages covering smaller row ranges.
* A page-index hit identifies a candidate region, not necessarily exact matching row numbers. The reader may still need to evaluate the predicate on the candidate rows.
* Translation does not inherently require enumerating every surviving row individually; ranges can represent groups of rows. The paper's concern is the growing cost of managing and mapping many small selections.
* Mica's aligned pages let a [[Single Page Bitmap]] carry page selections across columns, avoiding this particular cross-column page-mapping mismatch.

Related: [[Page Indexes]], [[Granularity Wall]].

Paper context: [[3 Granularity Wall#Why Page Hits Need Row-Range Translation|§3: Why page hits need row-range translation]].
