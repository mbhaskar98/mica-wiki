---
tags: []
created: 2026-10-15
description: Guarantee that a page can be decoded using only its own bytes and static column-level dictionary state.
---

# Page-Local Decode Self-Containment

* A Mica page is decoded from its own bytes plus, at most, shared state loaded once for its column.
* Dictionaries and symbol tables may be embedded in the page or stored once per column in the Detail Block. They are not necessarily duplicated in every page.
* Once the needed column state is available, selected pages can be fetched in any order and decoded independently and in parallel without loading neighboring data pages.
* The tradeoff is repeated page state such as encoding tags, raw sizes, and checksums, plus less effective compression at finer granularity.
* For example, [[Run-Length Encoding|run-length encoding (RLE)]] stores consecutive repeats as a value and count. Splitting 1,000 identical values into five independent 200-row pages replaces one `(value, 1000)` run with five `(value, 200)` runs, plus per-page state. This can cost more space but lets the reader decode any selected page independently.
* These overheads are separate from the fixed-size padding avoided by [[Variable Physical Page Layout]].

Related: [[Independent Addressability]], [[Rows Per Page]].

Paper context: [[4 Mica - File Format Design#4.5 Page-Local Decode Self-Containment|§4.5 Page-local decode self-containment]].
