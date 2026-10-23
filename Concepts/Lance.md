---
tags: []
created: 2026-10-15
description: Modern columnar data format optimized for random access, vector search, and selective machine learning workloads.
---

# Lance

* A columnar storage format, like [[Parquet]], designed to support fast random access: fetching selected rows without scanning large amounts of surrounding data.
* Its layout and encodings support selective queries, vector-search follow-up reads, and machine-learning workloads that sample rows non-sequentially.
* For example, if a query needs only 2,000 scattered rows from a table with 100 million rows, Lance aims to make retrieving those selected rows efficient.

## Why Mica Compares Against It

* Lance is a benchmark competitor in the [[1 Introduction-The Hardware & Software Mismatch#Evaluation Highlights|Mica introduction's evaluation highlights]]. Comparing against it tests [[Mica]] against a format already designed for efficient random reads, alongside Parquet.
* Lance lets each column have its own page layout and number of pages. Mica, as described in these notes, aligns page IDs across columns to support a [[Single Page Bitmap]].
* The reported Mica speedup applies to the tested queries and configurations; it does not establish that Mica is faster for every workload.

Source: [Lance file format documentation](https://lance.org/format/file/).
