---
tags: []
created: 2026-10-15
description: Query execution optimization that transfers filter predicates down to the storage layer to prune irrelevant data early.
---

# Predicate Pushdown

* Passing a query's filter condition down to the storage reader so it can apply the condition early.
* When metadata can rule out a storage unit, the reader can skip that unit before reading its data. For example, a date filter can exclude a page whose min/max dates fall entirely outside the requested range.
* If a storage unit cannot be ruled out, the reader may still need to fetch it and filter its rows in memory. Pushing down a predicate does not guarantee that every irrelevant row is avoided on disk.
* [[Data Clustering]] and metadata such as [[Layered Zone Maps]] help create opportunities to improve [[IO Selectivity|I/O selectivity]].

Paper context: [[2 Background and Target Regime#2.1 Selectivity|§2.1 Selectivity]].
