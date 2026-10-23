---
tags: []
created: 2026-10-15
description: Physical sorting and co-location of related table rows to maximize the effectiveness of storage pruning.
---

* Organizing rows so that values relevant to common filters are stored near one another.
* For example, grouping taxi trips by date can let a reader skip blocks outside a requested date range.
* If matching rows are scattered across many pages, the reader may need many page reads even when very few rows survive. Clustering can improve [[IO Selectivity|I/O selectivity]] without changing the query's [[Data Selectivity|data selectivity]].
* Clustering can make metadata-based pruning, such as [[Layered Zone Maps]], more effective by giving storage units narrower value ranges.
* The Mica paper treats improving file organization as a separate, complementary problem to its format design.

Paper context: [[2 Background and Target Regime#2.1 Selectivity|§2.1 Selectivity]].
