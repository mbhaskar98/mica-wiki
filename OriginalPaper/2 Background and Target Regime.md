---
tags: []
created: 2026-10-15
description: Definition of the workload selectivity and NVMe storage regime required for Mica's fine-grained I/O advantages.
---

Mica's expected advantage depends on two conditions:

* **Workload condition (§2.1):** Queries must allow enough irrelevant data to be skipped that avoiding reads matters.
* **Storage condition (§2.2):** The storage tier must make independent small reads cheap enough to exploit that selectivity.

When either condition is absent, Mica's expected advantage diminishes or disappears. Section 2.3 explains the software support needed to exploit the storage condition.

## 2.1 Selectivity

### Two Aspects of Selectivity

* [[IO Selectivity|I/O selectivity]] describes the fraction of the dataset the reader actually touches through storage I/O.
* [[Data Selectivity|Data selectivity]] describes the fraction of rows that survive the query's filter and are passed to the upper layers.
* The paper uses **high selectivity** to mean that only a small fraction needs to be read or returned. Thus, a smaller fraction read means stronger I/O selectivity; a smaller fraction returned means stronger data selectivity.

### The Reading Funnel

The reader first decides which storage units to fetch, then filters the loaded rows in memory. [[Data Clustering|Data clustering]] and mechanisms such as [[Predicate Pushdown|predicate pushdown]] can help it avoid fetching irrelevant units.

For an illustrative query returning five rows:

| Stage | Reader with coarse reads | Ideal precise reader |
| --- | --- | --- |
| Rows represented by the data read | 50,000 | 5 |
| Rows surviving the filter | 5 | 5 |
| Irrelevant rows read | 49,995 | 0 |

Both cases have the same data selectivity, but the precise reader has stronger I/O selectivity. The ideal is a conceptual limit, not a guarantee that a page-based reader can fetch exactly five rows.

Expressed as fractions with the same row-based denominator:

`fraction read ≥ fraction surviving the filter`

Equality means the reader fetches only relevant rows. This compares numerical fractions, not the informal descriptions "high" and "low" selectivity. Pages containing both matching and nonmatching rows can keep the fraction read above the fraction returned.

### Terminology in the Paper

| Term used in these notes | Related terminology listed by the paper                               |
| ------------------------ | --------------------------------------------------------------------- |
| [[IO Selectivity]]       | Clustering factor, data skipping ratio, micro-partition pruning ratio |
| [[Data Selectivity]]     | Selectivity factor, predicate selectivity, data selectivity           |

These are related terms in the cited literature; a ratio measuring data skipped and one measuring data read have opposite directions. Check a source's definition before comparing numbers.

### Mica's Target Workload

* Mica targets **high I/O selectivity**: workloads where the reader can skip most of the stored data.
* Tiny, independently addressable pages let the reader avoid fetching large chunks merely because a few rows match. The [[Single Page Bitmap]] tracks surviving pages across columns, while [[Layered Zone Maps]] help prune irrelevant metadata and pages.
* Low I/O selectivity means reading a large fraction of the dataset—essentially a scan—so Mica's expected advantage decreases.
* High data selectivity alone is insufficient: returning very few rows does not guarantee that the reader can avoid most storage reads.
* Improving [[Data Clustering|data clustering]] through file organization is a separate, complementary problem. Mica's format exploits opportunities to skip data; it does not automatically make scattered matching rows cluster together.

## 2.2 NVMe-class Storage

### Why the Storage Tier Matters

Fine-grained reads help only when storage can serve them efficiently. The paper contrasts these storage tiers:

| Storage tier           | Main constraint described in the paper                                  | Consequence for reading                                                                                          |
| ---------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| HDD                    | Millisecond-scale mechanical seeks and rotational delays                | Random access is much more expensive than sequential reads.                                                      |
| SATA SSD               | No mechanical seeks, but limited command-queue parallelism through AHCI | Less capacity for concurrent small reads than NVMe-class storage.                                                |
| Cloud object storage   | High per-request latency and limited per-object bandwidth               | Favors large coalesced reads at high concurrency.                                                                |
| [[NVMe-class Storage]] | PCIe attachment and extensive hardware queue parallelism                | Can serve many small random reads at high aggregate throughput if software maintains sufficient [[Queue Depth]]. |

For cloud object storage, the paper cites tens of milliseconds of base request latency and roughly 50 MiB/s per-object bandwidth. These are the paper's cited characteristics, not universal limits for every service or configuration.

### Small Reads at High Concurrency

* The paper cites the Samsung PM1743 specification as an example: up to **2.5 million [[IOPS]] for random 4 KB reads**.
* This is a hardware capability example, not Mica's measured query throughput or a guarantee for every NVMe drive.
* Keeping many requests in flight lets the storage device overlap work. A reader that submits only a few requests at a time can leave this capacity unused.

### The Mismatch with Existing Readers

* [[Parquet]] and ORC originated in the Hadoop ecosystem and organize data into coarse units suited to large sequential reads. The paper cites 128 MiB Parquet row groups and approximately 64 MiB ORC stripes as examples.
* In the reader behavior described here, a selective query fetches a few large chunks and then filters rows in memory, leaving NVMe's capacity for many small independent reads underused.
* These coarse units are not a claim that every Parquet reader must always fetch an entire row group; the paper's concern is how formats and readers exploit fine-grained access together.
* Mica uses independently addressable pages to exploit [[IO Selectivity|high I/O selectivity]]. Its advantage depends on both avoiding irrelevant reads and issuing the remaining reads efficiently.

## 2.3 Software Stack for Batched Disk I/O

### The Blocking I/O Bottleneck

* Traditional POSIX `pread` and `pwrite` calls use [[Blocking IO|blocking I/O]]: the issuing thread waits for the operation to finish before continuing.
* In that synchronous pattern, each thread has at most one request in flight. Creating more concurrent requests requires more threads.
* The paper estimates that reaching roughly 1.5–2.5 million IOPS this way can require on the order of a thousand concurrent threads. The exact requirement depends on request latency and workload.
* Scheduling and context switching consume CPU cycles the query engine could use for useful work. This is a performance bottleneck, not a claim that the system necessarily crashes.

### Asynchronous Submission and Completion

* [[Batched Asynchronous IO|Batched asynchronous I/O]] separates submitting requests from collecting their completions.
* The paper lists Linux AIO (`libaio`), [[io_uring]], and SPDK as ways to support many outstanding requests without assigning a blocked thread to each one.
* A worker can submit a batch, keep many requests in flight, and collect completions as they become available.
* io_uring uses shared submission and completion rings. Batching amortizes system-call overhead across requests; the completed read data goes into the designated read buffers, while completion entries report the outcome.

### How This Enables Mica

1. Determine which pages survive pruning, using mechanisms such as the [[Single Page Bitmap]] and [[Layered Zone Maps]].
2. Plan reads for those pages, using [[Bounded IO Coalescing|bounded I/O coalescing]] where nearby reads can be combined within the extra-data limit.
3. Submit the reads in batches through an asynchronous I/O interface to maintain sufficient [[Queue Depth|queue depth]].
4. Collect completions and process the returned data without requiring a dedicated blocked thread for every request.

The combination of selective page reads, NVMe-class storage, and efficient asynchronous submission enables the operating regime Mica targets. This excerpt emphasizes io_uring but does not establish it as Mica's only possible I/O interface.

Previous: [[1 Introduction-The Hardware & Software Mismatch|1 Introduction: The Hardware & Software Mismatch]] · Next: [[3 Granularity Wall]] · Index: [[Mica]]
