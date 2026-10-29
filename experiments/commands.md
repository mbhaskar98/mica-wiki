---
tags: []
created: 2026-10-27
description: Remote prerequisites, release build commands, and output paths for the Mica and Parquet preparation binaries.
---

# Commands

## Build the preparation binaries on remote

Run on **`nsl-ruby2`**, from the repository root containing `mica/`, `eval/`, and `deps/`. Rust **1.94.0** must be installed; the remote already has the compiler tools, CMake, `pkg-config`, and `protoc`. Keep the complete checkout, including `deps/lance`; Cargo needs network access or cached dependencies.

```bash
# Mica file converter
cargo +1.94.0 build --release --locked \
  --manifest-path mica/Cargo.toml --bin mica-convert

# Parquet preparation tool
cargo +1.94.0 build --release --locked \
  --manifest-path eval/native-format-bench/Cargo.toml \
  --bin native-format-bench
```

| Binary | Output path relative to repository root |
|---|---|
| Mica converter | `mica/target/release/mica-convert` |
| Parquet preparation tool | `eval/native-format-bench/target/release/native-format-bench` |

These commands build the tools only; they do not prepare or change dataset files. Build commands have not been executed or verified by a build in this session.

