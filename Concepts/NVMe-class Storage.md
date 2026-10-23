---
tags: []
created: 2026-10-15
description: Solid-state storage devices offering high queue depths, deep parallelism, and fast random read capabilities over PCIe.
---

# NVMe-class Storage

* NVMe stands for Non-Volatile Memory Express. In the paper's target regime, PCIe-connected storage supports many parallel hardware queues and small random reads at high aggregate throughput.
* HDDs pay mechanical seek and rotational costs. SATA SSDs avoid those mechanical costs but have more limited command-queue parallelism through AHCI.
* Software must maintain sufficient [[Queue Depth]] to exploit the device's parallelism; hardware capability alone does not ensure fast queries.
* The paper cites the Samsung PM1743's specification of up to 2.5 million [[IOPS]] for random 4 KB reads as an example, not a universal NVMe performance figure.
* [[Mica]] targets this storage regime because its small, independently addressable pages can avoid irrelevant reads when [[IO Selectivity|I/O selectivity]] is high.

Paper context: [[2 Background and Target Regime#2.2 NVMe-class Storage|§2.2 NVMe-class Storage]].
