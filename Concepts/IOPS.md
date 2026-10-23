---
tags: []
created: 2026-10-15
description: Measure of storage performance indicating the number of discrete read or write operations completed per second.
---

# IOPS

* I/O operations per second: the rate at which a storage device or system completes read and/or write operations.
* IOPS counts operations, while bandwidth measures bytes transferred per second. Request size matters when comparing the two.
* The paper cites up to 2.5 million IOPS for random 4 KB reads on a Samsung PM1743 as an example of [[NVMe-class Storage|NVMe hardware]] capability.
* Actual application performance depends on the request pattern, [[Queue Depth]], software overhead, and processing beyond storage I/O. A device specification is not a query-throughput measurement.

Paper context: [[2 Background and Target Regime#2.2 NVMe-class Storage|§2.2 NVMe-class Storage]].
