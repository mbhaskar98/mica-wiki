---
tags: []
created: 2026-11-02
description: Hardware testbed specifications, execution environment configurations, and evaluated format baselines for Mica ATC'26 empirical evaluation.
aliases:
  - Hardware Testbed
  - Testbed and Baselines
---

# Testbed and Baselines

Parent Hub: [[Projects/mica/experiments/Experiments|Mica Experiments Hub]]

## Hardware testbed and execution environment (ATC'26 paper baseline)

* **Host & Kernel:** Single-socket server running Ubuntu 24.04 LTS (Linux kernel `6.8.0-106-generic`), swap disabled.
* **Processor & Affinity:** Intel® Xeon® Gold 6530 (32 physical cores / 64 threads @ 2.1 GHz base clock), sub-NUMA clustering (SNC) enabled exposing 2 NUMA nodes, 256 GiB total DDR5 memory. Every benchmark process is bound to the first NUMA node (`numactl --cpunodebind=0 --membind=0`) and pinned to a single physical core (`--pin-core 0`) to eliminate cross-node memory traffic and core migrations.
* **CPU Power & Governor:** CPU governor set to `performance`; Intel Turbo Boost explicitly **disabled** to enforce deterministic CPU execution across iterations.
* **Storage & I/O Subsystem:** Single Micron 7450 PRO 960 GB enterprise NVMe SSD hosting an ext4 volume without RAID. Multi-queue `none` block scheduler (`/sys/block/nvmeXn1/queue/scheduler`); kernel readahead set to `128 KiB` (`read_ahead_kb = 128`).
* **Cache Eviction & Cold-Run Protocol:** Linux page, dentry, and inode caches dropped before each measured cold run (`sync; echo 3 > /proc/sys/vm/drop_caches`). To eliminate NVMe internal hardware controller/cache side-effects, a 1 GiB dummy file is streamed sequentially between iterations.
* **Repetition & Output Standard:** 10 measured iterations per query with a 30-second cooldown period between iterations. All evaluated readers are required to output identical, materialized Apache Arrow `RecordBatch` representations.

## Evaluated format configurations & baselines (Mica, Parquet, Lance)

* **Parquet Best-Tuned (§3 & §7 Baseline):** Row Group (RG) = 1M rows, Data Page (DP) = 20K rows, column-chunk Bloom filters enabled, Page Indexes (min/max statistics) enabled. Identified in the §3 tuning sweep as the optimal latency setting.
* **Parquet Mica-Aligned:** RG = 1K rows, DP = 200 rows, Bloom filters + Page Indexes enabled. Mimics Mica's fine data granularity to isolate format-level and reader-level metadata inflation ("granularity wall").
* **Lance Default:** Canonical format configuration without secondary index metadata.
* **Lance Mica-Aligned:** Canonical format equipped with the identical set of secondary indexes as Mica.
* **Reader Implementations:** Custom optimized reader based on canonical `parquet-rs` (Arrow Rust) with exposed API optimizations (I/O coalescing, batching, page-index pushdown); Lance reader based on the official canonical library (`lance`); Mica asynchronous reader based on native layout and batched asynchronous I/O.
