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

## Generate Mica report

- [x] Generate the NYC-only report for all four page sizes.
- [x] Generate the ClickBench-only report for all four page sizes.
- [x] Generate the combined NYC + ClickBench report for all eight configurations.
- [x] Include questions, setup, value labels, CSV tables, and both linear/log versions of cold and warm latency.
- [x] Verify exported table counts, charts, and ZIP integrity; generate reports locally and on `nsl-ruby2`.

**Report locations on remote** (relative to `~/mica`):

- NYC: `exp/results/batch-20261029T033433Z-cm9bd50y/report/`.
- ClickBench: `exp/results/batch-20261029T060341Z-95dn98gp/report/`.
- Combined: `exp/results/combined-report/`.

On `nsl-ruby2`, run:

```bash
cd ~/mica
source .venv/bin/activate
python3 exp/report_mica_experiments.py exp/results/BATCH_FOLDER
```

Inside that batch, open `report/index.html` to browse or `report/report.pdf` to share. Individual charts are in `report/plots/`, CSV tables in `report/tables/`, and the complete package is `report.zip`.

For multiple result folders, list them after the script name, separated by spaces:

```bash
python3 exp/report_mica_experiments.py \
  exp/results/NYC_BATCH_FOLDER \
  exp/results/CLICKBENCH_BATCH_FOLDER \
  --out-dir exp/results/combined-report
```

Replace the uppercase folder names with your actual batch folders. You can list more than two folders; each dataset/page-size combination must appear only once. With `--out-dir`, exports go into that folder and the ZIP is written beside it.

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
