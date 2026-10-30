---
tags: []
created: 2026-10-28
description: Completed NYC and ClickBench Mica runs at four page sizes, validated outputs, report locations, and generation commands.
---

# E01-Test2 — Mica metadata loading

**Question:** How do page size and eager/lazy metadata and full/sparse secondary-index loading affect query time and work?

**Status: Complete for the agreed Mica scope.** Both datasets × four page sizes × five test groups = **40/40 completed test groups**, including all four reader-ablation settings. This records execution, output checks, and reporting; it does not certify exact agreement with every paper value.

## NYC January — completed runs

Results on `nsl-ruby2`: `/mnt/home/bmahajan/mica/exp/results/batch-20261029T033433Z-cm9bd50y/` (**20/20 test groups complete**).

- [x] **50 rows/page** — `nyc-mica-50`; home input `nyc-fhv-guardrail/mica/v3_single_rpp_50/`.
  - [x] Cold read.
  - [x] Warm read.
  - [x] Reader ablation: all four settings below, including stage timings.
  - [x] Intermediate Arrow memory size.
  - [x] Disk space and metadata breakdown.
- [x] **200 rows/page** — `nyc-mica-200`; original input `nyc-fhv-guardrail/mica/v3_single/`.
  - [x] Cold read.
  - [x] Warm read.
  - [x] Reader ablation: all four settings below, including stage timings.
  - [x] Intermediate Arrow memory size.
  - [x] Disk space and metadata breakdown.
- [x] **800 rows/page** — `nyc-mica-800`; home input `nyc-fhv-guardrail/mica/v3_single_rpp_800/`.
  - [x] Cold read.
  - [x] Warm read.
  - [x] Reader ablation: all four settings below, including stage timings.
  - [x] Intermediate Arrow memory size.
  - [x] Disk space and metadata breakdown.
- [x] **3200 rows/page** — `nyc-mica-3200`; home input `nyc-fhv-guardrail/mica/v3_single_rpp_3200/`.
  - [x] Cold read.
  - [x] Warm read.
  - [x] Reader ablation: all four settings below, including stage timings.
  - [x] Intermediate Arrow memory size.
  - [x] Disk space and metadata breakdown.

## Reader-ablation settings — completed for every NYC and ClickBench page size

- [x] Lazy metadata + sparse indexes — `current_default`.
- [x] Eager metadata + sparse indexes — `metadata_eager`.
- [x] Eager metadata + full indexes, original static/generic execution — `eager_full_materialize_generic`.
- [x] Eager metadata + full indexes, execution settings matched to eager+sparse — `metadata_eager_full_index`.

## Validation and reporting

- [x] Check NYC-50 result coverage, matched-row counts, stage counters, and storage totals.
- [x] Check NYC-200 result coverage, stage counters, and storage accounting.
- [x] Check output coverage, iteration counts, matched-row consistency, and storage totals for all four NYC configurations.
- [x] Check the same outputs for all four ClickBench configurations, including all four ablation settings.
- [x] Download the complete ClickBench result batch locally.

## Generate Mica reports

Run from the repository root with its Python environment activated. These commands use the updated batches, including **20,000 rows/page**.

```bash
source .venv/bin/activate
NYC_BATCH=exp/results/batch-20261029T033433Z-cm9bd50y
CLICKBENCH_BATCH=exp/results/batch-20261029T060341Z-95dn98gp

python3 exp/report_mica_experiments.py "$NYC_BATCH" --out-dir "$NYC_BATCH/nyc-mica"
python3 exp/report_mica_experiments.py "$CLICKBENCH_BATCH" --out-dir "$CLICKBENCH_BATCH/clickbench-mica"
python3 exp/report_mica_experiments.py "$NYC_BATCH" "$CLICKBENCH_BATCH" --out-dir exp/results/combined-mica
```

| Report | Output folder |
|---|---|
| NYC | `exp/results/batch-20261029T033433Z-cm9bd50y/nyc-mica/` |
| ClickBench | `exp/results/batch-20261029T060341Z-95dn98gp/clickbench-mica/` |
| Combined | `exp/results/combined-mica/` |

Each folder contains `index.html`, `report.pdf`, `plots/`, `tables/`, and `provenance.json`; a ZIP is written beside the folder. Reports read saved results only and do not rerun benchmarks or change datasets. Cold and warm latency include both linear and log charts.

For other batches, replace the variable values. Multiple batch paths can be listed before `--out-dir`; include each dataset/page-size combination only once.

## ClickBench — completed runs

Results on `nsl-ruby2`: `/mnt/home/bmahajan/mica/exp/results/batch-20261029T060341Z-95dn98gp/` (**20/20 test groups complete**).

- [x] **50 rows/page** — `clickbench-mica-50`; home input `clickbench/mica/v3_single_rpp_50/`.
- [x] **200 rows/page** — `clickbench-mica-200`; original input `clickbench/mica/v3_single/`.
- [x] **800 rows/page** — `clickbench-mica-800`; home input `clickbench/mica/v3_single_rpp_800/`.
- [x] **3200 rows/page** — `clickbench-mica-3200`; home input `clickbench/mica/v3_single_rpp_3200/`.
- [x] Run cold read, warm read, all four reader-ablation settings, intermediate Arrow memory size, and disk-space breakdown for every ClickBench page size.

  To start another batch, select its configurations in `exp/experiment_configs.json`. From `~/mica` on `nsl-ruby2`, with `.venv` activated:

  ```bash
  python3 exp/run_experiments.py             # validate and preview
  python3 exp/run_experiments.py --execute   # start a new selected batch
  ```

**Input prefixes:** Home = `~/data/mica-dataset/prepared/native-format-bench/`; original = `/data/mica-dataset/prepared/native-format-bench/`. Use the home dataset-level manifest, including for the original 200-row files.

- [[Projects/mica/experiments/E01-Test1|E01-Test1]]: Prepared file inventory and locations.
- [[Projects/mica/experiments/commands|Commands]]: Remote build commands and prerequisites.

## Example Mica config

The JSON file contains an array of entries. Each entry names one prepared input and the tests to run.

```json
[
  {
    "name": "nyc-mica-50",
    "dataset": "nyc",
    "format": "mica",
    "data_dir": "~/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/mica/v3_single_rpp_50",
    "manifest": "~/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/manifest.json",
    "tests": [
      "cold-read",
      "warm-read",
      "mica-reader-ablation",
      "in-memory-size",
      "disk-space"
    ]
  }
]
```

`name` labels results; `dataset` selects the workload family; `format` selects the reader family; `data_dir` selects the prepared files; `manifest` selects the dataset manifest; `tests` lists the existing test groups. Repeat entries for other page sizes and datasets. Select the file with `python3 exp/run_experiments.py --config PATH_TO_CONFIG.json --execute`.

**Shared runner:** Each entry’s `format` selects `"mica"` or `"parquet"`; `dataset` selects NYC or ClickBench. Use `python3 exp/run_experiments.py --config PATH_TO_CONFIG.json --execute` for your chosen Mica list. The default config now selects NYC Parquet; see [[Projects/mica/experiments/E01-Test4|E01-Test4]] for that checklist and automatic builds.
