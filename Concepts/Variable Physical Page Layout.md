---
tags: []
created: 2026-10-15
description: Storage layout pairing fixed logical row boundaries with variable encoded byte lengths per column.
---

# Variable Physical Page Layout

* A shared page ID fixes the logical row range across columns, while encoding, compression, and encoded byte size can differ.
* Mica stores each page's **file offset and byte size** in a per-column [[Page Indexes|page index]], allowing [[Independent Addressability]].
* Uniform physical pages would simplify offset arithmetic but waste space for narrow columns. The paper's example puts 200 Int8 values in an 8 KiB slot, leaving about 97.6% as padding.
* Adjusting [[Rows Per Page|RPP]] cannot eliminate the width mismatch: wide columns hit the size limit while narrow columns underfill uniform slots.
* Mica accepts page-index metadata to avoid that padding and the associated wasted reads. [[Recursive Page Bisection]] preserves row alignment without requiring equal byte sizes.

Paper context: [[4 Mica - File Format Design#4.2 Variable Physical Page Layout|§4.2 Variable physical page layout (editorial title)]].
