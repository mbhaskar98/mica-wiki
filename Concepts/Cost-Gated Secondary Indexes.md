---
tags: []
created: 2026-10-15
description: Adaptive decision mechanism that loads secondary indexes only when estimated lookup cost is lower than scanning data pages.
---

# Cost-Gated Secondary Indexes

* Reading a secondary index costs I/O and memory, so using one is not automatically cheaper than scanning data pages.
* [[Mica]] performs a cost-benefit calculation before loading an index.
* If accessing the index is estimated to be slower than directly scanning the targeted data pages, the reader skips the index and scans those pages instead.

Related: [[Single Page Bitmap]], [[Layered Zone Maps]].
