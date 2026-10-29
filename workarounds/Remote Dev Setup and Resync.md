---
tags: []
created: 2026-10-27
description: Two-step rsync workflow to synchronize local codebase and vendored dependencies to remote nodes without .gitignore filtering bugs.
---

# Remote Dev Setup and Resync

This guide documents the operational rsync strategy for synchronizing the local Mica codebase to remote compute environments (such as `nsl-ruby2`).

## The Two-Step Rsync Strategy

To synchronize a local repository to a remote compute node without losing vendored dependency source files or uploading project junk:

```bash
# Step 1: Sync main project tree respecting .gitignore
rsync -av --delete --filter=':- .gitignore' --exclude='.git/' mica/ remote:~/mica/

# Step 2: Sync vendored dependencies ignoring root .gitignore filters
rsync -av --delete --exclude='.git/' mica/deps/ remote:~/mica/deps/
```

### Technical Justification

1. **Global `.gitignore` Filtering Hazards:** 
   Standard project `.gitignore` files frequently contain rules such as `bin/`, `*.so`, or `build/`. When executing a naive recursive `rsync` with `--filter=':- .gitignore'`, `rsync` applies these patterns globally. This inadvertently strips legitimate nested source files inside vendored third-party repositories—such as `deps/lance/rust/lance/src/bin/` or embedded C/C++ source trees in `deps/fsst`.
2. **Explicit Dependency Transfer:** 
   The second command explicitly syncs `mica/deps/` without the `.gitignore` filter. This guarantees that all required vendored code transfers intact to the remote target while preventing large project artifacts (such as `target/`, `.venv/`, or `.git/`) from polluting the remote workspace.

## Dry-Run Verification

Before applying deletions on a new remote node, verify the transfer list with `-n` (dry-run):

```bash
rsync -avn --delete --filter=':- .gitignore' --exclude='.git/' mica/ remote:~/mica/
rsync -avn --delete --exclude='.git/' mica/deps/ remote:~/mica/deps/
```

---

## Vault Navigation & MoC Context

- [[Projects/mica/OriginalPaper/Mica|Mica]]: Parent project hub.
- [[Vendored Lance Build Fix]]: Companion workaround for scaffolding dummy binaries in vendored dependencies.
- [[runbooks/Runbooks|Runbooks]]: Central index of operational guides and procedures.
