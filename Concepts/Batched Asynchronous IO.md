---
tags: []
created: 2026-10-15
description: Technique for submitting and completing batches of non-blocking I/O requests to saturate NVMe drive parallelism.
aliases:
  - Batched Asynchronous I/O
---

# Batched Asynchronous I/O

* **Asynchronous:** Submit a request without waiting for its completion before submitting another. Collect completion results separately.
* **Batched:** Submit or collect multiple requests together, spreading coordination overhead across the batch.
* A worker can keep many reads outstanding, providing the [[Queue Depth]] needed to exploit [[NVMe-class Storage]].
* The paper names Linux AIO (`libaio`), [[io_uring]], and SPDK as relevant approaches. Their interfaces and implementation details differ.
* Batching is different from [[Bounded IO Coalescing|I/O coalescing]]: batching submits multiple requests together; coalescing merges nearby byte ranges into fewer requests. A reader can use both.

Related: [[Blocking IO|Blocking I/O]], [[Single Page Bitmap]].

Paper context: [[2 Background and Target Regime#2.3 Software Stack for Batched Disk I/O|§2.3 Software Stack for Batched Disk I/O]].
