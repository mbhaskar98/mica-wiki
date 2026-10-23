---
tags: []
created: 2026-10-15
description: High-performance Linux asynchronous I/O framework utilizing lockless ring buffers shared between user space and kernel.
---

# io_uring

* A Linux asynchronous I/O interface using shared submission and completion rings to communicate requests and results between an application and the kernel.
* The application places read requests in the submission ring; completion entries report when operations finish and their results. The actual bytes read are placed in the buffers designated by the requests.
* [[Batched Asynchronous IO|Batching]] spreads submission overhead across multiple operations, reducing per-request system-call overhead.
* A worker can keep many operations in flight without blocking a separate thread on every read, helping sustain [[Queue Depth]] on [[NVMe-class Storage|NVMe storage]].
* Section 2.3 highlights io_uring alongside `libaio` and SPDK. It supports the case for asynchronous I/O but does not establish an exclusive io_uring dependency for Mica.

Paper context: [[2 Background and Target Regime#2.3 Software Stack for Batched Disk I/O|§2.3 Software Stack for Batched Disk I/O]].
