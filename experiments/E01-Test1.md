---
tags: []
created: 2026-10-27
description: E01-Test1 completed data preparation, original and new dataset locations, blocked configurations, paper scope, and batch commands.
---

# E01-Test1 — Data preparation

All paths are on **`nsl-ruby2`**. **Status verified: 2026-10-28 09:11 UTC.** Of the original 22 targets: **19 complete, 3 blocked, none pending**. The 19 include three full-year Mica configs already created outside the current comparison scope. Complete means files are prepared; query correctness and benchmark timings are separate checks.

## Commands

Preparation is complete for every feasible target; no rerun is needed. The commands below are retained for reference. Run from `~/mica`; the binaries are already built. The batch command attempts all 22 configs with up to two independent conversions at a time, without grouping.

| Task | Command |
|---|---|
| Preview all 22 configurations without creating files | `python3 scripts/prepare_e01_batch.py --jobs 2 --parquet-jobs 2` |
| Run the complete 22-configuration list | See the command below. |
| Watch active conversions in another terminal | `python3 scripts/prepare_e01_status.py --watch 30` |
| Verify original `/data` files against the saved hashes | `python3 scripts/hash_prepared_dataset.py -c` |

```bash
cd ~/mica
python3 scripts/prepare_e01_batch.py --execute --jobs 2 --parquet-jobs 2
```

| What to expect | Meaning |
|---|---|
| Configuration list | `scripts/e01_configs.json`; every listed entry is attempted. No automatic skipping. |
| Existing destination | Reports `FAIL` / `Output already exists`; refuses to overwrite it and continues. |
| ClickBench 1K configurations | Included in the original list but blocked by the writer limit described below. The complete-list command does not make them feasible. |
| Parallelism | Two independent conversions overall, including up to two ClickBench Parquet converters. `--parquet-jobs` defaults to 1; the command above explicitly sets it to 2. Each converter loads its own decoded input (roughly 75 GiB each in recent runs, plus variable writer memory). |
| Grouping | The command above omits `--group-parquet`: each configuration encodes independently and publishes when it finishes. Adding grouping shares decoding but writes each group sequentially. |
| No output growth initially | Input loading and Bloom-filter preparation happen before writing. This stage has no progress counter. Restarting repeats it. |
| Publication and interruption | Each independent configuration is published after validation. Ctrl+C stops active/queued work; completed configurations remain, while unfinished ones restart from the beginning. |
| Logs | `~/mica/logs/e01-preparation/<run-time>/<run-number>.log`. Without grouping, each configuration has its own numbered log. |

The final batch `20261028T065739.239688Z` completed the four remaining ClickBench Parquet configs (logs `19.log`–`22.log`). No preparation processes were running at the verification. Existing-output failures in the other logs are overwrite refusals; the three 1K ClickBench cases failed preflight. The old `scripts/e01_remaining.json` is outdated; the command above uses `scripts/e01_configs.json`.

- [[Projects/mica/experiments/commands|Commands]]: Remote prerequisites, binary build commands, and binary locations.

## Locations

The tables below use two roots. Append a listed relative path to the corresponding root to obtain its full location.

| Root | Exact location | Contents |
|---|---|---|
| **Original** | `/data/mica-dataset/prepared/native-format-bench/` | Existing prepared files; unchanged by home preparation. |
| **New** | `/mnt/home/bmahajan/data/mica-dataset/prepared/native-format-bench/` | New configurations and the two home dataset manifests. |

| Home input / manifest | Exact location |
|---|---|
| NYC inputs: all 12 months | `/mnt/home/bmahajan/data/mica-dataset/raw/nyc-fhv-2021/parquet/` |
| ClickBench input | `/mnt/home/bmahajan/data/mica-dataset/raw/clickbench/hits.parquet` |
| NYC dataset manifest | `/mnt/home/bmahajan/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/manifest.json` |
| ClickBench dataset manifest | `/mnt/home/bmahajan/data/mica-dataset/prepared/native-format-bench/clickbench/manifest.json` |

## What existed before this preparation

### Mica — Original root

All three original layouts use **200 rows/page**.

| Dataset / scope | Relative folder | Files / rows |
|---|---|---|
| NYC January | `nyc-fhv-guardrail/mica/v3_single/` | `part_0000.mica`; 11,908,468 rows |
| NYC full year | `nyc-fhv-guardrail/mica/v3_multi_mirrored/` | 12 monthly Mica files; 174,596,652 rows |
| ClickBench full dataset | `clickbench/mica/v3_single/` | `hits_0000.mica` through `hits_0003.mica`; 99,997,497 rows |

`v3_single` uses one source dataset; ClickBench is split into four Mica files by its file-row limit. NYC `v3_multi_mirrored` keeps the 12 monthly source boundaries.

### Parquet — Original root

**RG** means rows per row group; **page target** means the requested maximum page rows, not a guarantee of equal page boundaries across columns. Here `1k = 1,024`, `16k = 16,384`, `256k = 262,144`, and `1m = 1,048,576`.

| Dataset / scope | Compression | Existing RG → page targets | Best baseline |
|---|---|---|---|
| NYC January | None | 1k → 200; 4k → 200/2000; 16k → 200/2000; 64k → 200/2000/20000; 256k → 200/2000/20000; 1m → 200/2000/20000/200000 | **1m / 20000** |
| NYC January | Each of lz4, snappy, zstd | Each of 4k/16k/64k/256k/1m → 20000 | Additional compressed variants |
| ClickBench full dataset | None | 256k → 20000; 1m → 20000 | **1m / 20000** |
| NYC full year | — | No tuned full-year prepared Parquet found | Outside the checked paper scope |

| Dataset | Relative file pattern under Original root |
|---|---|
| NYC | `nyc-fhv-guardrail/parquet/original_order/<codec>/rg_<RG>/page_rows_<target>/single/fhvhv_tripdata_2021-01.parquet` |
| ClickBench | `clickbench/parquet/original_order/none/rg_<RG>/page_rows_<target>/single/hits.parquet` |

For example, the NYC best baseline is `/data/mica-dataset/prepared/native-format-bench/nyc-fhv-guardrail/parquet/original_order/none/rg_1m/page_rows_20000/single/fhvhv_tripdata_2021-01.parquet`.

## New configurations — status and destinations

### Mica — New root

All nine are **complete**. They retain Mica v3, 8 KiB pages, no compression, and the existing file-row limits. Each folder contains its Mica files and a local manifest.

| Dataset / scope | Rows/page | Status | Relative folder |
|---|---:|---|---|
| NYC January | 50 | Complete | `nyc-fhv-guardrail/mica/v3_single_rpp_50/` |
| NYC January | 800 | Complete | `nyc-fhv-guardrail/mica/v3_single_rpp_800/` |
| NYC January | 3200 | Complete | `nyc-fhv-guardrail/mica/v3_single_rpp_3200/` |
| NYC full year | 50 | Already created; outside current scope | `nyc-fhv-guardrail/mica/v3_multi_mirrored_rpp_50/` |
| NYC full year | 800 | Already created; outside current scope | `nyc-fhv-guardrail/mica/v3_multi_mirrored_rpp_800/` |
| NYC full year | 3200 | Already created; outside current scope | `nyc-fhv-guardrail/mica/v3_multi_mirrored_rpp_3200/` |
| ClickBench | 50 | Complete | `clickbench/mica/v3_single_rpp_50/` |
| ClickBench | 800 | Complete | `clickbench/mica/v3_single_rpp_800/` |
| ClickBench | 3200 | Complete | `clickbench/mica/v3_single_rpp_3200/` |

Each NYC January config has 11,908,468 rows in one file; each full-year config has 174,596,652 rows across 12 files; each ClickBench config has 99,997,497 rows across four files. Headers, row counts and manifest sizes were checked.

### Parquet — New root

All use **no compression** and **original row order**. Paths below are relative to the dataset's Parquet base:

| Dataset | Parquet base under New root | Filename inside each `single/` folder |
|---|---|---|
| NYC January | `nyc-fhv-guardrail/parquet/original_order/none/` | `fhvhv_tripdata_2021-01.parquet` |
| ClickBench | `clickbench/parquet/original_order/none/` | `hits.parquet` |

| Dataset | RG | Page target | Status | Folder under its Parquet base |
|---|---|---:|---|---|
| NYC January | 1k | 2000 | Complete, registered | `rg_1k/page_rows_2000/single/` |
| NYC January | 1k | 20000 | Complete, registered | `rg_1k/page_rows_20000/single/` |
| NYC January | 16k | 20000 | Complete, registered | `rg_16k/page_rows_20000/single/` |
| ClickBench | 1k | 200 | Blocked; no valid final output | `rg_1k/page_rows_200/single/` |
| ClickBench | 1k | 2000 | Blocked; no valid final output | `rg_1k/page_rows_2000/single/` |
| ClickBench | 1k | 20000 | Blocked; no valid final output | `rg_1k/page_rows_20000/single/` |
| ClickBench | 16k | 200 | Complete, recovered and registered | `rg_16k/page_rows_200/single/` |
| ClickBench | 16k | 2000 | Complete, recovered and registered | `rg_16k/page_rows_2000/single/` |
| ClickBench | 16k | 20000 | Complete, recovered and registered | `rg_16k/page_rows_20000/single/` |
| ClickBench | 256k | 200 | Complete, registered | `rg_256k/page_rows_200/single/` |
| ClickBench | 256k | 2000 | Complete, registered | `rg_256k/page_rows_2000/single/` |
| ClickBench | 1m | 200 | Complete, registered | `rg_1m/page_rows_200/single/` |
| ClickBench | 1m | 2000 | Complete, registered | `rg_1m/page_rows_2000/single/` |

All seven completed ClickBench Parquet files contain **99,997,497 rows**. The 16K configs have 6,104 row groups each; 256K configs have 382; 1M configs have 96. Footer row counts and row-group sizes match the requested settings, and each home manifest entry points to the final folder with the correct RG/page settings. Mica headers confirm the requested caps, including **50 rows/page**; file sizes and local manifest row totals also match. The original best-tuned Parquet baselines remain available. No regeneration is needed.

## Failures and manifest behavior

| Question / message | Explanation |
|---|---|
| Why does ClickBench 1K fail? | Full ClickBench needs about 97,654 groups at 1,024 rows/group. The installed parquet-rs 58.2.0 writer rejects group ordinals beyond its roughly 32K-group limit (`i16` conversion). Page-target changes cannot fix this. This is a limit of this writer, not a universal Parquet claim. |
| Why did NYC 1K work? | January has 11,908,468 rows: about 11,630 groups, which fits. |
| Why did the earlier group report failure after 16K finished? | Its 1K members failed. Recovery saved and registered all three valid 16K outputs before cleanup; the final `Expected exactly one Parquet file` error rejected a failed 1K output. |
| What was wrong with the plan? | It lacked a full-size row-group-limit check. The 20,000-row grouping sample could verify equivalence but could not expose this scale limit. Splitting ClickBench would change the file-layout experiment. |
| What changes after successful preparation? | New files and the home dataset manifest. Existing original references to `/data` are retained. Original files and manifests remain unchanged. |
| How does Parquet registration work? | Adds configurations, final paths and writer settings to `parquet_tuned.variants`; existing entries remain. Failed 1K outputs were not registered. |
| How does Mica selection work? | Updates `v3_single_dir` or `v3_multi_mirrored_dir` to the latest successful folder. Only one folder per layout is selected at a time; select the intended config before benchmarking. Other prepared folders remain available. |
| Are concurrent manifest writes safe? | The helper uses a lock and atomic replacement. A failed publication rolls back only that attempt's new output. |
| Does grouping change encoding? | No requested encoding, compression or index settings change. All ten grouped sample files were byte-identical to standalone files. Grouped preparation time includes shared work and must not be reported as independent per-config build time. |
| Why can home preparation be slow? | Home is NFS-backed. Preparation there is not a local-NVMe performance measurement. |

## Scope and evidence

| Measurement / extension | Data scope / decision | Evidence |
|---|---|---|
| Figures 4–5: Parquet tuning/decomposition | NYC January | Manuscript §3 explicitly selects January for single-file measurements. |
| Main NYC cold-read comparison | January for Mica, Parquet and Lance | Archived results use `single_file`; Mica and Parquet scans return 11,908,468 rows. |
| Best-tuned Parquet | 1m / 20000 | Figure 10 caption; already existed before this preparation. |
| NYC Mica-aligned Parquet | 1k / 200 | Figure 10 caption and archived NYC results. |
| Main ClickBench comparison | Full dataset; best Parquet 1m / 20000 | Figure 10 and archived results; displayed comparison omits Mica-aligned Parquet. |
| Full-year NYC | Mica prepared as extra work; matching new Parquet is paused pending scope choice | Full-year data existing does not establish its use in the checked paper results. Missing full-year tuned Parquet is not a January reproduction gap. |

The reader name `mica_v3_native_mirrored_adaptive_sparse_hybrid` does not determine data scope: workload scope selects single-file versus mirrored data.

| Source / audit | Location |
|---|---|
| Manuscript and PDF | Local `papers/mica_atc26_manuscript.md` and `.pdf`; checked §3, Figure 10, Table 3 and §7.1 |
| Figure's NYC archive selection | `paper_package/v3/scripts/plotting/plot_cold_read_combined.py` |
| NYC result archive | `exp/cold-read/results/nyc/cold_read_20260518T084357Z/merged_iterations.csv` |
| ClickBench result archive | `exp/cold-read/results/clickbench/cold_read_clickbench_20260518T231854Z/merged_iterations.csv` |
| Reader scope selection | `eval/native-format-bench/src/run.rs` |
| Recovered 16K outputs | `~/mica/logs/e01-16k-recovery-20261028T041354Z/results.json` |
| Grouped/standalone sample equivalence | `~/mica/logs/e01-group-equivalence-20261028T020137Z/` |
| Home migration and original-data verification | `~/mica/logs/e01-home-migration/20261028T000708Z/`; all 2,304 original prepared files matched saved hashes; all 13 copied raw files were SHA-256 verified |

- [[Projects/mica/OriginalPaper/Mica|Mica]]: Parent project hub.
