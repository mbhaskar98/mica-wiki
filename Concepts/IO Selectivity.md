---
tags: []
created: 2026-10-15
description: Fraction of total physical dataset bytes that storage readers actually read from disk to evaluate a query.
aliases:
  - I/O Selectivity
---

# I/O Selectivity

* Describes how much of a dataset the reader must physically touch through storage I/O to answer a query.
* In the Mica paper's wording, **high I/O selectivity** means reading a small fraction and skipping most of the data. Low I/O selectivity means reading a large fraction, approaching a scan.
* A query can return only five rows yet require reads covering 50,000 rows. Its [[Data Selectivity|data selectivity]] is strong, but its storage reads may still waste substantial work.
* Using comparable row-based fractions, the fraction read is at least the fraction surviving the filter. The two become equal only when no irrelevant rows are fetched.
* [[Data Clustering]], [[Predicate Pushdown]], and the size of independently readable units affect how much data can be skipped. [[Layered Zone Maps]] support pruning in Mica.
* The paper lists clustering factor, data skipping ratio, and micro-partition pruning ratio as related terminology. Their numerical definitions can differ; a fraction skipped is not the same as a fraction read.

Paper context: [[2 Background and Target Regime#2.1 Selectivity|§2.1 Selectivity]].
