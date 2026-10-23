---
tags: []
created: 2026-10-15
description: Standard open-source columnar storage format designed for large-scale sequential batch analytics.
---

# Parquet Files

* A standard columnar storage format organized into row groups, column chunks, and data pages; see [[Parquet Layout]].
* Optional [[Bloom Filters]] and [[Page Indexes]] let readers prune row groups and individual pages for selective queries.
* Data pages need not align across columns, so carrying a page selection into other columns requires [[Row-Range Translation]].
* In the paper's selective-query experiment, shrinking pruning units reduces data reads but increases metadata loading and planning costs, producing the [[Granularity Wall]].

Paper context and measurements: [[3 Granularity Wall]].
