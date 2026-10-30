---
tags: []
created: 2026-10-27
description: Dataset preparation checklists for NYC and ClickBench, with completed/missing Mica and Parquet configurations, locations, and preparation tools.
---

# E01-Test1 — Data preparation

**Goal:** Prepare the same source rows in each format/configuration. Checked = files prepared; unchecked = files still to create. **\*** marks newly created files; unmarked completed entries were already present. Query benchmarks are tracked in E01-Test2/E01-Test4.

## Locations

All paths are on `nsl-ruby2`.

| Root | Location |
|---|---|
| **Original** | `/data/mica-dataset/prepared/native-format-bench/` |
| **Home** | `~/data/mica-dataset/prepared/native-format-bench/` |

Append the paths below to the named root. Home dataset manifests are `<dataset-folder>/manifest.json`; they retain references to original files in `/data` and register new home files. Existing original files stay intact.

## Mica

### NYC January

Dataset folder: `nyc-fhv-guardrail`. Source: `~/data/mica-dataset/raw/nyc-fhv-2021/parquet/fhvhv_tripdata_2021-01.parquet`. Each configuration contains **11,908,468 rows**.


- [x] **200 rows/page** — Original: `nyc-fhv-guardrail/mica/v3_single/`.
- [x] \* **50 rows/page** — Home: `nyc-fhv-guardrail/mica/v3_single_rpp_50/`.
- [x] \* **800 rows/page** — Home: `nyc-fhv-guardrail/mica/v3_single_rpp_800/`.
- [x] \* **3200 rows/page** — Home: `nyc-fhv-guardrail/mica/v3_single_rpp_3200/`.
- [ ] **20,000 rows/page** — Home destination: `nyc-fhv-guardrail/mica/v3_single_rpp_20000/`.

One Mica file per January configuration, plus its local manifest. The row cap is an upper limit: the byte-size limit can split pages into smaller row ranges.

#### Full-year NYC

- [x] Full-year Mica, **200 rows/page** — Original: `nyc-fhv-guardrail/mica/v3_multi_mirrored/`.
- [x] \* Full-year Mica, **50/800/3200 rows/page** — Home: `nyc-fhv-guardrail/mica/v3_multi_mirrored_rpp_<RPP>/`.

Full-year Mica has 12 monthly files and 174,596,652 rows. It is separate from the January comparison; no full-year Parquet preparation is requested here.

### ClickBench

Dataset folder: `clickbench`. Source: `~/data/mica-dataset/raw/clickbench/hits.parquet`. Each configuration contains **99,997,497 rows**.


- [x] **200 rows/page** — Original: `clickbench/mica/v3_single/`.
- [x] \* **50 rows/page** — Home: `clickbench/mica/v3_single_rpp_50/`.
- [x] \* **800 rows/page** — Home: `clickbench/mica/v3_single_rpp_800/`.
- [x] \* **3200 rows/page** — Home: `clickbench/mica/v3_single_rpp_3200/`.
- [ ] **20,000 rows/page** — Home destination: `clickbench/mica/v3_single_rpp_20000/`.

Each Mica configuration has four files (`hits_0000.mica` through `hits_0003.mica`) and a local manifest.

## Parquet

### NYC January

Dataset folder: `nyc-fhv-guardrail`. Source: `~/data/mica-dataset/raw/nyc-fhv-2021/parquet/fhvhv_tripdata_2021-01.parquet`. Each configuration contains **11,908,468 rows**.


All checklist entries use **no compression and original row order**. The paper’s best-tuned reference is **1M row groups / 20000 page target**.

The file is `fhvhv_tripdata_2021-01.parquet` inside each listed folder. RG labels are row counts in binary multiples: 1K = 1024, 4K = 4096, 64K = 65536, 1M = 1048576. Page labels are requested maximum rows per page.

- [x] **RG 1K / page 200** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_1k/page_rows_200/single/`.
- [x] \* **RG 1K / page 2000** — Home: `nyc-fhv-guardrail/parquet/original_order/none/rg_1k/page_rows_2000/single/`.
- [x] \* **RG 1K / page 20000** — Home: `nyc-fhv-guardrail/parquet/original_order/none/rg_1k/page_rows_20000/single/`.
- [x] **RG 4K / page 200** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_4k/page_rows_200/single/`.
- [x] **RG 4K / page 2000** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_4k/page_rows_2000/single/`.
- [x] **RG 16K / page 200** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_16k/page_rows_200/single/`.
- [x] **RG 16K / page 2000** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_16k/page_rows_2000/single/`.
- [x] \* **RG 16K / page 20000** — Home: `nyc-fhv-guardrail/parquet/original_order/none/rg_16k/page_rows_20000/single/`.
- [x] **RG 64K / page 200** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_64k/page_rows_200/single/`.
- [x] **RG 64K / page 2000** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_64k/page_rows_2000/single/`.
- [x] **RG 64K / page 20000** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_64k/page_rows_20000/single/`.
- [x] **RG 256K / page 200** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_256k/page_rows_200/single/`.
- [x] **RG 256K / page 2000** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_256k/page_rows_2000/single/`.
- [x] **RG 256K / page 20000** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_256k/page_rows_20000/single/`.
- [x] **RG 1M / page 200** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_1m/page_rows_200/single/`.
- [x] **RG 1M / page 2000** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_1m/page_rows_2000/single/`.
- [x] **RG 1M / page 20000** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_1m/page_rows_20000/single/`.
- [x] **RG 1M / page 200000** — Original: `nyc-fhv-guardrail/parquet/original_order/none/rg_1m/page_rows_200000/single/`.

Additional compressed NYC Parquet files exist; the comparison uses the uncompressed files listed here.

### ClickBench

Dataset folder: `clickbench`. Source: `~/data/mica-dataset/raw/clickbench/hits.parquet`. Each configuration contains **99,997,497 rows**.


All entries use **no compression and original row order**. Each folder contains `hits.parquet`.

- [x] \* **RG 16K / page 200** — Home: `clickbench/parquet/original_order/none/rg_16k/page_rows_200/single/`.
- [x] \* **RG 16K / page 2000** — Home: `clickbench/parquet/original_order/none/rg_16k/page_rows_2000/single/`.
- [x] \* **RG 16K / page 20000** — Home: `clickbench/parquet/original_order/none/rg_16k/page_rows_20000/single/`.
- [x] \* **RG 256K / page 200** — Home: `clickbench/parquet/original_order/none/rg_256k/page_rows_200/single/`.
- [x] \* **RG 256K / page 2000** — Home: `clickbench/parquet/original_order/none/rg_256k/page_rows_2000/single/`.
- [x] **RG 256K / page 20000** — Original: `clickbench/parquet/original_order/none/rg_256k/page_rows_20000/single/`.
- [x] \* **RG 1M / page 200** — Home: `clickbench/parquet/original_order/none/rg_1m/page_rows_200/single/`.
- [x] \* **RG 1M / page 2000** — Home: `clickbench/parquet/original_order/none/rg_1m/page_rows_2000/single/`.
- [x] **RG 1M / page 20000** — Original: `clickbench/parquet/original_order/none/rg_1m/page_rows_20000/single/`.

ClickBench **1K row groups** are blocked by the existing writer’s 32,767-row-group limit: the full dataset would need about 97,654 groups. Changing the page target does not solve this. The completed 16K files remain available alongside 256K and 1M.

## Preparation config and commands

Preparation tools and basic usage are documented in the repository’s `data-prep/README.md`.

**Config file:** `data-prep/configs.json`. Each entry selects the dataset, format, and requested settings. Examples for both formats:

```json
[
  {"dataset": "nyc", "format": "mica", "layout": "v3_single", "rows_per_page": 20000},
  {"dataset": "clickbench", "format": "parquet", "row_group": "16k", "page_rows": 2000}
]
```

These entries illustrate the schema. Add only configurations that need creating; existing destinations are refused.

| Setting | Value / meaning |
|---|---|
| `--work-root` | `/data/mica-preparation` by default; conversion writes its temporary files here. |
| `--data-root` | `~/data/mica-dataset/prepared/native-format-bench` by default; completed files and dataset manifests live here. |
| `--min-free-gb` | `30` by default, in decimal GB. Reserve this space per output before starting; wait in the queue if unavailable. |
| `--jobs` | Maximum simultaneous preparation helpers. Waiting helpers do not run converters. |
| `--parquet-jobs` | Maximum large Parquet conversions; also bounded by `--jobs`. |

From `~/mica`, with `.venv` activated:

```bash
# Preview the configured targets; no conversion starts.
python3 data-prep/prepare_batch.py --jobs 2 --parquet-jobs 2

# Convert on /data, transfer to home, then release the /data work space.
python3 data-prep/prepare_batch.py --execute --jobs 2 --parquet-jobs 2 \
  --work-root /data/mica-preparation --min-free-gb 30

# Monitor running converters.
python3 data-prep/status.py --watch 30
```

Parallel helpers share disk reservations, including separately started helpers. A normal one-output job reserves 30 GB until its conversion and home transfer finish. Grouped conversions reserve 30 GB per requested output. This is an admission minimum, not an output-size cap: a job may need more disk. Space used by unrelated processes is not reserved by this script.

Completed output is checked on the fast disk, copied into temporary home staging, checked again, and then published to its final folder. Only the home dataset manifest is updated. Existing destinations are refused rather than overwritten. A failed transfer leaves the existing manifest/files intact; completed outputs remain on rerun. After a killed helper, the next preparation attempt reclaims recorded scratch space only when no converter still uses it.

Run preparation separately from benchmarks to avoid disk contention.

| Purpose | Tool |
|---|---|
| Prepare one config; preview by default | `data-prep/prepare.py` |
| Run the JSON list with parallelism and queue messages | `data-prep/prepare_batch.py` |
| Inspect active converter progress | `data-prep/status.py` |
| Verify original dataset hashes | `python3 scripts/hash_prepared_dataset.py -c` |

- [[Projects/mica/experiments/commands|Commands]]: Release build commands and binary locations.
- [[Projects/mica/experiments/E01-Test2|E01-Test2]]: Mica query runs and reports.
- [[Projects/mica/experiments/E01-Test4|E01-Test4]]: Parquet query runs and configuration checklist.
