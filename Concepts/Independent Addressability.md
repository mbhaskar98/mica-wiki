---
tags: []
created: 2026-10-15
description: Ability to directly compute the file location of any page or metadata record without sequentially scanning preceding blocks.
---

# Independent Addressability

* The ability to locate and read a particular block or metadata entry without scanning preceding blocks first.
* The Section 4 excerpt describes known fixed-length metadata entries. Once a table's base location and indexing layout are known, a reader can address the needed entry directly.
* For example, locating Page 42's metadata should not require reading the entries for Pages 1 through 41 in sequence.
* Fixed-length metadata entries do not imply fixed byte lengths for all data pages. Mica's per-column [[Page Indexes|page index]] records each data page's file offset and byte size, supporting a [[Variable Physical Page Layout]].
* This complements [[Sparse Metadata Loading]]: pruning decides which metadata is relevant, and addressability lets the reader reach it directly.
* Addressability and the [[Cross-Column Row-Range Invariant]] solve different problems: locating a block versus giving a page ID the same row meaning across columns.
* [[Page-Local Decode Self-Containment]] is another requirement: after fetching a page, the reader can decode it using its own bytes and any one-time column state, without fetching neighboring data pages.

Paper context: [[4 Mica - File Format Design#Independent Addressability and Cross-Column Alignment|§4: Independent addressability and alignment]].
