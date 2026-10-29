---
tags: []
created: 2026-10-27
description: Defensive dummy-file scaffolding workaround to bypass Cargo manifest parser failures for missing unused vendored binaries.
---

# Vendored Lance Build Fix

This note documents the dummy-file workaround used to resolve missing binary errors in vendored dependencies (specifically `lance`) during remote Cargo builds.

## Problem Diagnosis

When executing `cargo build` on the remote server for `native-format-bench`:

```text
error: failed to get `lance` as a dependency of package `native-format-bench v0.1.0`
Caused by:
  failed to parse manifest at `/mnt/home/bmahajan/mica/deps/lance/rust/lance/Cargo.toml`
Caused by:
  can't find `lq` bin at `src/bin/lq.rs` or `src/bin/lq/main.rs`. Please specify bin.path if you want to use a non-default path.
```

### Root Cause

The vendored manifest in `deps/lance/rust/lance/Cargo.toml` declares an executable target:

```toml
[[bin]]
name = "lq"
required-features = ["cli"]
```

However, the corresponding source file (`src/bin/lq.rs`) is not present in the vendored tree. Cargo validates the existence of all declared binary targets whenever it parses the manifest of a path dependency, causing the build to fail immediately.

## The Solution: Dummy File Scaffolding

Scaffold an empty placeholder binary locally before synchronizing to the remote node:

```bash
mkdir -p deps/lance/rust/lance/src/bin
echo 'fn main() {}' > deps/lance/rust/lance/src/bin/lq.rs
```

Then sync to the remote server using the two-step rsync workflow:

```bash
rsync -av --delete --exclude='.git/' ./deps/lance/ nsl-ruby2:~/mica/deps/lance/
```

## Why We Did It: Trade-Off Analysis

We require the `lance` library to compile and evaluate comparative benchmarks in `native-format-bench`, but we have zero operational need for Lance's bundled `lq` CLI utility.

Attempting to resolve this issue through conventional means introduces unnecessary technical debt:

| Alternative | Problem Introduced | Verdict |
|---|---|---|
| **Edit vendored `Cargo.toml`** (deleting `[[bin]]`) | Directly mutates third-party/forked code. Any subsequent upstream rebase, submodule update, or fork pull will hit immediate Git merge conflicts on the manifest file. | **Rejected** |
| **Download real `lq.rs` from upstream** | Ingests unneeded CLI dependencies, additional feature flags, and dead code that will never be executed by Mica's benchmarks. | **Rejected** |
| **Scaffold dummy `fn main() {}`** | Satisfies Cargo's strict file-existence validation check. Compiles instantaneously, adds zero dead code, and leaves the upstream manifest 100% untouched. | **Adopted (Zero Debt)** |

The dummy file is a defensive engineering pattern: it satisfies the compiler toolchain's structural requirements while preserving upstream manifest purity.

---

## Vault Navigation & MoC Context

- [[Projects/mica/OriginalPaper/Mica|Mica]]: Parent project hub.
- [[Remote Dev Setup and Resync]]: Two-step rsync procedure ensuring vendored source directories transfer cleanly.
