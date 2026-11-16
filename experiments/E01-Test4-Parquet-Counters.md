---
tags: []
created: 2026-11-05
description: Inventory of measurements already saved by the lazy Parquet diagnostic binary and what remains combined within each measurement.
---

# E01-Test4: Existing Parquet measurements

Related: [[E01-Test4]].

These measurements are already saved in each configuration’s `parquet-metadata-cold/profile.json` and `parquet-metadata-cached/profile.json`, per query and iteration. They come from `profile_parquet_sync_lazy`; they are separate executions from the ordinary cold-read and warm-read tests.

| Step | Time already recorded | Other counters already recorded | What is still combined or missing |
|---|---|---|---|
| Open metadata | `open_builder_ms` | File-read time, bytes and calls | Footer versus page-index loading; parsing, schema setup and allocation |
| Compile predicates | `compile_predicates_ms` | — | Finer work within compilation |
| Check row-group statistics | `zone_map_ms` | Surviving row groups | Entries checked per column |
| Check Bloom filters | `lazy_bloom_ms` | File-read time, bytes and calls; surviving row groups | Loading/parsing versus membership checks; cache hits and missing filters |
| Apply page indexes | `page_index_ms` | Candidate predicate segments and selected/skipped rows | Per-column checks, row-range conversion/intersection and final selection construction |
| Prepare predicate and projection | `row_filter_build_ms`, `projection_build_ms` | Projected/materialized columns and hidden predicate columns | Predicate preparation does not measure its execution |
| Build reader and apply predicates | `reader_build_ms` | File-read time, bytes and calls | Reader setup, predicate-column decoding and predicate evaluation |
| Read output batches | `read_filter_ms` for reader advancement; `read_filter_eval_ms` for the enclosing loop | File-read time, bytes and calls; returned rows and batches | Page parsing, value/dictionary decoding and Arrow-array construction |
| Whole query and validation | `total_ms`, `validation_ms`, `wall_ms` | Total wrapper-read bytes/calls/time; process OS-read bytes; result-validation fields | Explicit residual time and measured instrumentation overhead |

## How to interpret these values

- **Reader build includes filtering:** `reader_row_filter_ms` labels the whole build span when filtering is enabled; it is not a separate predicate-only timer.
- **File reads are not necessarily disk reads:** wrapper counters include reads served by the OS cache. Process OS-read bytes cover a broader scope, including validation.
- **Page counts are candidate predicate segments:** they do not count every page decoded across output columns.
- **Timers can overlap:** I/O times are inside stage times; the enclosing output-loop timer contains reader advancement. Do not add them together.
- **Keep executions separate:** these fields can explain metadata-cold/cached latency, not directly decompose the ordinary cold/warm bars. Calculate any breakdown per iteration before summarizing.

Source: `eval/native-format-bench/src/bin/profile_parquet_sync_lazy.rs`.
Saved results: `exp/results/batch-20261103T100910Z-2r2sbqiy/`.

## Preview timing breakdown

```bash
python3 exp/reporting/report_parquet_drilldown.py <batch-folder> --preview
```

Review `<batch-folder>/parquet-drilldown/parquet-drilldown.pdf` before generating further reports. Only the selected batch is read. Every query uses the actual iteration producing its median metadata-test reader latency; its stage values add to that median total. This is not a breakdown of ordinary cold/warm executions. Numerical stage values are shown alongside the stacked bars. Existing reports remain unchanged.
