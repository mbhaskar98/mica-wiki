---
tags: []
created: 2026-10-29
description: Completed NYC and ClickBench Parquet baselines across 18 configurations, result locations, report commands, and pending fine instrumentation.
---

# E01-Test4 — Parquet baseline and drill-down

**Question:** Where does Parquet spend time, and how much overhead do extra measurements add?

**Data:** NYC January and full ClickBench, using uncompressed Parquet. Checked boxes mean complete; unchecked boxes mean pending.

**Baseline status:** Both datasets × nine configurations × seven tests = **126/126 completed test groups**. Fine instrumentation and its overhead comparison remain pending below.

## Row groups and page sizes

| Row-group sizes | Page-row targets |
|---|---|
| **16K, 256K, 1M** | **200, 2000, 20000** |

These nine uncompressed combinations are already prepared for both datasets. A page-row target is an upper limit; actual pages may contain fewer rows and always stay within a row group.

## Setup

- [x] Check the selected uncompressed NYC variants against the remote manifest/files.
- [x] Automatically build the existing profiler in release mode before staging data. Build logs are under the batch’s `builds/` folder. Other binaries retain their existing driver build steps.
- [x] Build the release profiler on remote; initial build completed successfully.

## Tests for every configuration

Use the existing query lists: **nine NYC queries** and **five ClickBench queries**. For both datasets, run cold read, warm read, Arrow memory, disk space, coalescing, metadata cold, and metadata cached for each file. Stage the file once, finish all seven tests, restore the manifest and clean up, then move to the next file.

| Test | What is captured | Paper coverage |
|---|---|---|
| `cold-read` | Latency, kernel I/O, selected/read rows and pages; exact/coarse results | Figures 4, 10, 13, 16, 17 |
| `warm-read` | Latency with file bytes cached | Figure 11 |
| `in-memory-size` | Intermediate coarse Arrow data size | Figure 12 |
| `disk-space` | Total, data, metadata, and padding bytes | Table 3 |
| `parquet-coalescing` | Coalesced reader, exact results; compare with normal cold baseline | Figure 14 |
| `parquet-metadata-cold` | Rebuilt metadata/Bloom filters; existing stage timings and I/O counters | Figures 5, 15; Table 4 byte accounting |
| `parquet-metadata-cached` | Retained metadata/Bloom filters with cold data reads | Figure 15 |

The paper’s focused point, time-1h, and compound queries are included in the nine-query controls. Controls are extended to every available configuration. The cache-byte counter follows the paper’s serialized-metadata read accounting; it is **not measured peak RAM or parsed-object heap usage**. Existing coarse profiling is distinct from the later fine-instrumentation overhead experiment.

## NYC

**Complete:** 9 configurations, all seven tests per configuration (**63/63 groups**). Results: `exp/results/batch-20261029T091931Z-43t02s4b/`.

- [x] `nyc-parquet-none-rg-16k-page-200` — `/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_16k/page_rows_200/single`.
- [x] `nyc-parquet-none-rg-16k-page-2000` — `/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_16k/page_rows_2000/single`.
- [x] `nyc-parquet-none-rg-16k-page-20000` — `~/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_16k/page_rows_20000/single`.
- [x] `nyc-parquet-none-rg-256k-page-200` — `/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_256k/page_rows_200/single`.
- [x] `nyc-parquet-none-rg-256k-page-2000` — `/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_256k/page_rows_2000/single`.
- [x] `nyc-parquet-none-rg-256k-page-20000` — `/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_256k/page_rows_20000/single`.
- [x] `nyc-parquet-none-rg-1m-page-200` — `/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_1m/page_rows_200/single`.
- [x] `nyc-parquet-none-rg-1m-page-2000` — `/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_1m/page_rows_2000/single`.
- [x] `nyc-parquet-none-rg-1m-page-20000` — `/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_1m/page_rows_20000/single`.

## ClickBench

**Complete:** 9 configurations, all seven tests per configuration (**63/63 groups**). Results: `exp/results/batch-20261029T143404Z-oz1huksy/`.

- [x] `clickbench-parquet-none-rg-16k-page-200` — `~/data/mica-dataset/prepared/native-format-bench/clickbench/parquet/original_order/none/rg_16k/page_rows_200/single/`.
- [x] `clickbench-parquet-none-rg-16k-page-2000` — `~/data/mica-dataset/prepared/native-format-bench/clickbench/parquet/original_order/none/rg_16k/page_rows_2000/single/`.
- [x] `clickbench-parquet-none-rg-16k-page-20000` — `~/data/mica-dataset/prepared/native-format-bench/clickbench/parquet/original_order/none/rg_16k/page_rows_20000/single/`.
- [x] `clickbench-parquet-none-rg-256k-page-200` — `~/data/mica-dataset/prepared/native-format-bench/clickbench/parquet/original_order/none/rg_256k/page_rows_200/single/`.
- [x] `clickbench-parquet-none-rg-256k-page-2000` — `~/data/mica-dataset/prepared/native-format-bench/clickbench/parquet/original_order/none/rg_256k/page_rows_2000/single/`.
- [x] `clickbench-parquet-none-rg-256k-page-20000` — `/data/mica-dataset/prepared/native-format-bench/clickbench/parquet/original_order/none/rg_256k/page_rows_20000/single/`.
- [x] `clickbench-parquet-none-rg-1m-page-200` — `~/data/mica-dataset/prepared/native-format-bench/clickbench/parquet/original_order/none/rg_1m/page_rows_200/single/`.
- [x] `clickbench-parquet-none-rg-1m-page-2000` — `~/data/mica-dataset/prepared/native-format-bench/clickbench/parquet/original_order/none/rg_1m/page_rows_2000/single/`.
- [x] `clickbench-parquet-none-rg-1m-page-20000` — `/data/mica-dataset/prepared/native-format-bench/clickbench/parquet/original_order/none/rg_1m/page_rows_20000/single/`.

## Run either Mica or Parquet

The same runner handles both. Each JSON entry’s `format` is `"mica"` or `"parquet"`; `dataset` is `"nyc"` or `"clickbench"`. The `tests` list selects the applicable experiments. Mica reader-ablation is Mica-only; all seven Parquet tests support both NYC and ClickBench.

```bash
cd ~/mica
source .venv/bin/activate
python3 exp/run_experiments.py             # validate and preview
python3 exp/run_experiments.py --execute   # build and run selected config
```

For a different JSON list or an interrupted batch:

```bash
python3 exp/run_experiments.py --config PATH_TO_CONFIG.json --execute
python3 exp/run_experiments.py --resume exp/results/BATCH_FOLDER --execute
```

Put the desired dataset entries in your config file and select it with `--config`. See E01-Test2 for a complete Mica example.

## Example Parquet entry

The config file is an array:

```json
[
  {
    "name": "nyc-parquet-none-rg-16k-page-200",
    "dataset": "nyc",
    "format": "parquet",
    "data_dir": "/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_16k/page_rows_200/single",
    "manifest": "~/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/manifest.json",
    "tests": [
      "cold-read",
      "warm-read",
      "in-memory-size",
      "disk-space",
      "parquet-coalescing",
      "parquet-metadata-cold",
      "parquet-metadata-cached"
    ]
  }
]
```

`name` labels outputs; `data_dir` selects prepared files; `manifest` is the home dataset-level manifest; `tests` selects work. The wrapper finds the Parquet selector from that manifest. It reads `/data` files in place, stages home files temporarily, and restores the original `/data` manifest after use or during interruption recovery.

## Scripts and outputs

| Purpose | Script / binary |
|---|---|
| Dispatch, builds, copying, checkpoints, recovery, cache summaries | `exp/run_experiments.py` |
| Cold baseline and coalescing | `exp/cold-read/run_cold_read_bench.sh` |
| Warm baseline | `exp/warm-page-cache-size/run_warm_page_cache_size_bench.sh` |
| Arrow objects | `exp/in-memory-size/run_in_memory_size_bench.sh` |
| Storage components | `exp/disk-space/run_disk_space_analysis.sh` |
| Existing stage timings and metadata-cache modes | `eval/native-format-bench/target/release/profile_parquet_sync_lazy` |

Standard/coalescing results use their existing `run/summary.csv` layout. Metadata controls save `profile.json`, `summary.csv`, `command.json`, and `runner.log` under each test. Cold-profile summaries include `serialized_cacheable_metadata_bytes`. Outputs stay inside the new result batch; old paper artifacts are not overwritten.

## Generate Parquet reports

Run from the repository root with its Python environment activated. Reports cover **all seven tests** for each of the nine configurations per dataset.

```bash
source .venv/bin/activate
NYC_BATCH=exp/results/batch-20261029T091931Z-43t02s4b
CLICKBENCH_BATCH=exp/results/batch-20261029T143404Z-oz1huksy

python3 exp/report_parquet_experiments.py "$NYC_BATCH" --out-dir "$NYC_BATCH/nyc-parquet"
python3 exp/report_parquet_experiments.py "$CLICKBENCH_BATCH" --out-dir "$CLICKBENCH_BATCH/clickbench-parquet"
python3 exp/report_parquet_experiments.py "$NYC_BATCH" "$CLICKBENCH_BATCH" --out-dir exp/results/combined-parquet
```

| Report | Output folder |
|---|---|
| NYC | `exp/results/batch-20261029T091931Z-43t02s4b/nyc-parquet/` |
| ClickBench | `exp/results/batch-20261029T143404Z-oz1huksy/clickbench-parquet/` |
| Combined | `exp/results/combined-parquet/` |

Each folder contains `index.html`, `report.pdf`, `plots/`, `tables/`, and `provenance.json`; a ZIP is written beside the folder. Reports read saved results only and do not rerun benchmarks or change datasets. Cold, warm, and coalescing latency include linear and log charts. Arrow memory is logical buffer size; cacheable metadata is serialized read bytes, neither is peak process RAM.

For other batches, replace the variable values. Multiple batch paths can be listed before `--out-dir`; include each dataset/configuration combination only once.

## Later work

- [ ] Audit missing generic Parquet costs beyond the existing counters.
- [ ] Add only necessary fine instrumentation to the shared reader path, with an on/off switch.
- [ ] Repeat matching benchmarks and quantify instrumentation overhead.

- [[Projects/mica/experiments/E01-Test1|E01-Test1]]: Prepared input inventory.
- [[Projects/mica/experiments/E01-Test2|E01-Test2]]: Completed Mica runs, config example, and reporting.
