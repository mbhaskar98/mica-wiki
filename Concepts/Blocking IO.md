---
tags: []
created: 2026-10-15
description: Synchronous I/O model where the issuing thread halts until the storage operation completes.
aliases:
  - Blocking I/O
---

# Blocking I/O

* In the synchronous POSIX `pread`/`pwrite` pattern described by the paper, the issuing thread waits until its operation finishes.
* That thread cannot submit another operation while it is blocked, so increasing the number of outstanding requests requires more threads.
* At high concurrency, scheduling and switching between threads consumes CPU time that a query engine could otherwise use to process data.
* The paper describes a performance and scalability problem, not an inevitable system crash.
* [[Batched Asynchronous IO|Batched asynchronous I/O]] separates submission from completion so many requests can remain in flight with fewer worker threads.

Related: [[Queue Depth]], [[io_uring]].

Paper context: [[2 Background and Target Regime#2.3 Software Stack for Batched Disk I/O|§2.3 Software Stack for Batched Disk I/O]].
