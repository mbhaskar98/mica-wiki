---
tags: []
created: 2026-10-15
description: Optimization that merges nearby small reads into a single I/O request while strictly limiting wasted data transfer.
aliases:
  - Bounded I/O Coalescing
---

# Bounded I/O Coalescing

* [[NVMe-class Storage|NVMe drives]] handle parallel reads well, but issuing millions of tiny 4 KB read requests still consumes CPU time.
* Coalescing combines nearby reads. If the reader needs Page 1 and Page 3, it might issue one read covering Pages 1 through 3 to save a kernel call.
* "Bounded" means the reader enforces a strict limit on the extra, unneeded data included between useful pages.
* [[Mica]] only merges reads when the extra data stays within that limit, balancing request overhead and hardware queue utilization against wasted bandwidth.

* Unlike [[Batched Asynchronous IO|batching]], which submits multiple requests together, coalescing merges nearby reads into fewer requests. The reader can combine both techniques.

Related: [[Single Page Bitmap]], [[Granularity Wall]], [[Queue Depth]].
