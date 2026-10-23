---
tags: []
created: 2026-10-15
description: Number of pending, in-flight I/O requests submitted to a storage device concurrently.
---

# Queue Depth

* The number of outstanding I/O requests submitted but not yet completed, measured at a particular queue, device, or layer of the storage stack.
* Enough outstanding requests let [[NVMe-class Storage|NVMe storage]] overlap work and use its parallelism. Too few requests can leave the device underutilized.
* Queue depth is different from the number of hardware queues: one queue can contain multiple outstanding requests.
* [[Batched Asynchronous IO]] lets a worker maintain many outstanding requests without needing one blocked thread per request.
* [[Mica]] needs both selective page reads and efficient request submission to keep the hardware busy.

Related: [[IOPS]], [[Blocking IO|Blocking I/O]], [[io_uring]].

Paper context: [[2 Background and Target Regime#2.3 Software Stack for Batched Disk I/O|§2.3 Software Stack for Batched Disk I/O]].
