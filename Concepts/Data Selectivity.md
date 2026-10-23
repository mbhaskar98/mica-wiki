---
tags: []
created: 2026-10-15
description: Fraction of dataset rows that satisfy a query's filter predicates and survive to downstream execution.
---

* The fraction of dataset rows that satisfy a query's filter and are passed to the upper layers.
* Also called predicate selectivity or selectivity factor in the terminology listed by the Mica paper.
* In the paper's wording, **high data selectivity** means very few rows survive the filter.
* If a query needs five rows, those five survivors define its data selectivity regardless of whether the reader fetches data covering five rows or 50,000 rows.
* This measures filtering of input rows, not the number of rows produced by a later aggregation.
* High data selectivity does not guarantee high [[IO Selectivity|I/O selectivity]]: the reader must also be able to locate and skip irrelevant storage units.

Paper context: [[2 Background and Target Regime#2.1 Selectivity|§2.1 Selectivity]].
