---
tags: []
created: 2026-11-02
description: Empirical evaluation setup, hardware testbed specifications, dataset query matrix, and baseline configurations for Mica, Parquet, and Lance.
---

# 7 Evaluation

This section documents the experimental methodology, hardware environment, query workload matrix, and baseline configurations evaluated in the [[Mica]] ATC'26 paper to assess fine-grained pruning efficiency against [[Parquet]] and [[Lance]].

## Evaluation Goals

The evaluation tests four core research questions:

1. **Selective Query Latency:** How does Mica perform on selective queries compared to existing formats on cold page cache, and how does a warm page cache affect relative performance?
2. **Storage Overhead:** How much storage overhead does the Mica format incur compared to other formats across different data granularities?
3. **In-Memory Footprint:** How much intermediate in-memory data representation (Arrow `RecordBatch`) can Mica reduce via fine-grained I/O pruning compared to existing formats?
4. **Full-Scan Performance:** How does Mica perform on un-pruned full-scan queries where fine-grained metadata cannot skip data pages?

---

## Experimental Setup & Hardware Testbed

All evaluations were executed on a dedicated single-socket bare-metal server configured for deterministic hardware and kernel performance:

* **Host Processor:** Single **Intel® Xeon® Gold 6530** (32 physical cores / 64 threads @ 2.1 GHz base clock). Sub-NUMA Clustering (**SNC**) is enabled, exposing the socket as 2 distinct NUMA nodes.
* **Memory Subsystem:** **256 GiB** total DDR5 memory.
* **Operating System & Kernel:** **Ubuntu 24.04 LTS** running Linux kernel **`6.8.0-106-generic`**, swap disabled.
* **Storage Device:** Single **Micron 7450 PRO 960 GB** enterprise NVMe SSD hosting an **ext4** dataset volume without RAID.
* **Block I/O Scheduler & Readahead:** Multi-queue **`none`** block scheduler (`/sys/block/nvmeXn1/queue/scheduler`); kernel block readahead configured to **128 KiB** (`read_ahead_kb = 128`).
* **CPU Power & Governor:** CPU frequency governor configured strictly to **`performance`**; Intel Turbo Boost explicitly **disabled** to eliminate dynamic thermal clock skew; system swap disabled.
* **Affinity & NUMA Isolation:** Every benchmark process is explicitly bound to NUMA node 0 via `numactl --cpunodebind=0 --membind=0` and pinned to a single physical core (`--pin-core 0`) to eliminate cross-node memory bus traffic and OS scheduler migrations.
* **Cold-Run Cache Protocol:** Linux page cache, dentries, and inodes are evicted before each measured run (`sync; echo 3 > /proc/sys/vm/drop_caches`). To counter NVMe internal controller/DRAM cache side-effects, a 1 GiB dummy file is streamed sequentially between iterations.
* **Repetition Cadence:** 10 measured iterations per query with an enforced 30-second cooldown period between iterations.
* **Materialization Contract:** All competing reader implementations are required to materialize identical, contiguous Apache Arrow `RecordBatch` representations to ensure downstream consumer equality.

---

## Evaluated Baselines & Configurations

To isolate whether performance gains originate from layout organization, index availability, or reader implementations, the paper establishes four key baseline configurations across three formats:

| Format / Configuration | Row Group (RG) Size | Data Page (DP) Size | Pruning Metadata & Indexes | Description / Purpose |
|---|---|---|---|---|
| **Mica** | 1,000–3,200 rows | 200 rows (cap) | Coarse Zone Maps, Fine Zone Maps, Detail Blocks (Bloom + Bitmaps) | Native page-addressable columnar format with unified row intervals and single-page bitmap pruning. |
| **Parquet Best-Tuned** | 1,000,000 rows | 20,000 rows | Column-chunk Bloom filters + Page Indexes (min/max) | Lowest-latency baseline identified during the §3 tuning sweep, representing realistic tuned production deployment. |
| **Parquet Mica-Aligned** | 1,000 rows | 200 rows | Column-chunk Bloom filters + Page Indexes (min/max) | Parquet tuned to mimic Mica's data granularity, isolating software stack planning and metadata inflation overheads ([[Granularity Wall]]). |
| **Lance Default** | Canonical defaults | Canonical defaults | Default manifest statistics (no secondary indexes) | Canonical modern columnar format optimized for random access without added indexes. |
| **Lance Mica-Aligned** | Canonical defaults | Canonical defaults | Secondary inverted/scalar index equivalents | Canonical Lance equipped with the equivalent secondary index coverage as Mica. |

### Reader Implementations

* **Parquet Reader:** Custom high-performance reader based on the official Rust **`parquet-rs`** library (Arrow ecosystem). Optimized via exposed reader APIs for I/O coalescing, page-index pruning, and batch decoding.
* **Lance Reader:** Custom benchmark reader built upon the official **`lance`** Rust library, utilizing native scan adapters.
* **Mica Reader:** Native asynchronous engine utilizing direct asynchronous I/O batching, single-page bitmap candidate filtering, and role-based per-column decode scheduling.

---

## Workload Matrix: Evaluated Datasets & Queries

The evaluation spans real-world NYC Taxi trips (single-file 12M row January 2021 partition and full 175M row dataset) and ClickBench web analytics (single 14.8 GB table):

| Dataset | Label | Predicate Expression | Projected Columns | Workload Archetype |
|---|---|---|---|---|
| **NYC Taxi** | `point` | `pickup_datetime = 12:34:56 on 2021-01-15` | `pickup_datetime+` | Extreme point lookup on high-cardinality timestamp. |
| **NYC Taxi** | `time-1h` | `pickup_datetime ∈ [12:00, 13:00) on 2021-01-15 ∧ trip_miles > 5` | `trip_miles+` | Clustered 1-hour time window with range filter. |
| **NYC Taxi** | `equality` | `dispatching_base = "B03136"` | `base_passenger_fare+` | Rare string equality on low-cardinality dimension. |
| **NYC Taxi** | `compound` | `pickup_datetime ∈ [12:00, 13:00) ∧ trip_miles > 5 ∧ dispatching_base = "B02764"` | `dispatching_base` | Multi-column conjunction (time range + numeric range + string equality). |
| **ClickBench** | `Q19` | `UserID = "435090932899640449"` | `UserID` | Rare equality point query on 64-bit integer ID. |
| **ClickBench** | `Q36` | `CounterID = 62 ∧ EventDate ∈ [15887, 15918) ∧ isRefresh = 0 ∧ DontCountHits = 0 ∧ URL ≠ ""` | `URL` | Complex conjunction on high-cardinality string projection. |
| **ClickBench** | `Q40` | `CounterID = 62 ∧ EventDate ∈ [15887, 15918) ∧ isRefresh = 0 ∧ TrafficSourceID ∈ {-1, 6} ∧ RefererHash = 3594120000172545465` | `URLHash`, `EventDate` | Multi-predicate selective conjunction projecting fixed-width columns. |

---

## Selective Query Latency & Pruning Effectiveness (§7.1)

* **End-to-End Speedup:** Mica consistently outperforms Parquet and Lance across all selective queries, delivering speedups ranging from **2.23×** (ClickBench Q40) to **22.56×** (ClickBench Q19) over Parquet Best-Tuned.
* **Granularity Wall Confirmation:** Parquet Mica-Aligned consistently demonstrates higher latency than Parquet Best-Tuned (often >10× slower) despite reading fewer physical data bytes, confirming that Parquet's metadata representation, row-range mapping, and reader pipeline cannot translate fine data granularity into lower end-to-end latency.
* **I/O Selectivity Metric:** Calculated as the ratio of kernel-reported physical read bytes to the actual on-disk data bytes of projected columns. In Mica, I/O selectivity approaches true data selectivity, whereas Parquet incurs extreme read amplification due to coarse row group / page bounds and un-pruned metadata reads.
