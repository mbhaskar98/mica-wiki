---
tags: []
created: 2026-11-12
description: Formal workload and pruning-sensitivity definitions anchored to Mica measurements, explaining one fixed layout and the limits of clustering and scan-frequency extrapolation.
---

# Clustering and MICA: one layout, many queries

## 1. System Constraint: The Workload Objective

$$
L^* = \operatorname*{arg\,min}_{L}\sum_q p_q\,T(q\mid L)
$$

A database file is written once. The storage engine cannot dynamically rebuild the physical layout (row order, page granularity, encodings) for each incoming query. Therefore, the optimal layout ($L^*$) is the one that minimizes frequency-weighted average latency across the entire expected workload, weighting high-frequency queries ($p_q$) more heavily.

## 2. Diagnostic Metric: Pruning Sensitivity

$$
\eta = \frac{\ln\left(S(r_c)/S(r_f)\right)}{\ln\left(r_c/r_f\right)}
$$

Pruning sensitivity ($\eta$) measures the efficiency of shrinking page sizes.
*   **The Denominator:** Represents the scaling of metadata overhead. Shrinking pages creates more page headers and metadata entries that the CPU must load, parse, and cache.
*   **The Numerator:** Represents the reduction in I/O payload (how many fewer rows the engine is forced to fetch).

## 3. Empirical Trade-offs: Metadata Overhead vs. I/O Savings

**High Sensitivity (NYC Equality)**
Shrinking pages from 20,000 to 200 rows slashed candidates from 9.56 million to 221,600 ($\eta \approx 0.82$). This massive I/O reduction offset the increased metadata overhead, dropping latency to 43.09 ms.

**Low Sensitivity (ClickBench Q42)**
Shrinking pages only reduced candidates from 780,000 to 738,600 ($\eta \approx 0.012$). The CPU incurred heavy metadata discovery costs without a meaningful I/O reduction, increasing latency to 78.96 ms.

## 4. The 20.7% Workload Tipping Point

**Global Configuration:** 200 rows/page.

Mica’s fine-grained layout excels on selective workloads, averaging 151.72 ms on the NYC dataset and beating Parquet's 1-million-row group layout (183.91 ms). 

However, this layout hits a hard compute bottleneck if the workload shifts toward full-table scans. If dense projection scans exceed **20.7%** of the workload frequency, the metadata overhead of Mica's tiny pages causes it to lose to Parquet's larger blocks.