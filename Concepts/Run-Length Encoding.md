---
tags: []
created: 2026-10-15
description: Compression technique that stores sequences of identical consecutive values as single value-count pairs.
aliases:
  - RLE
---

# Run-Length Encoding

Run-length encoding (RLE) represents a consecutive run of equal values as a value and its repetition count, instead of storing every occurrence separately.

## Example

```text
Original values: A A A B B A
Encoded runs:    (A, 3) (B, 2) (A, 1)
```

Decoding expands each pair in sequence to reconstruct the original values. The final A remains a separate run: RLE records consecutive repetitions, not the total frequency of a value across the column.

* Long runs of repeated values can compress well.
* Alternating values such as `A B A B A B` produce runs of length one, so storing counts may add overhead instead of saving space.
* Low cardinality alone does not guarantee effective RLE; the order of the values matters too. [[Presence Bitmaps]] answer which values occur in a page, while RLE encodes their ordered sequence for reconstruction.

## Why Small Pages Can Reduce Compression

Consider 1,000 consecutive occurrences of A:

```text
One independently encoded 1,000-row page:
    (A, 1000)

Five independently encoded 200-row pages:
    Page 1: (A, 200)
    Page 2: (A, 200)
    Page 3: (A, 200)
    Page 4: (A, 200)
    Page 5: (A, 200)
```

The smaller pages repeat the run description and carry their own page state, such as encoding tags, sizes, and checksums. In exchange, the reader can fetch and decode Page 4 without reading the other four pages.

These pairs are a teaching notation, not Mica's specified byte encoding. They illustrate repeated state, not an exact compression ratio; actual byte savings depend on the encoding and data.

## Mica's Tradeoff

Section 4.5 uses RLE as an example of how fine page granularity reduces opportunities for compression. [[Page-Local Decode Self-Containment]] allows independent sparse reads but restricts how much data an encoder can exploit within a page. Mica accepts the resulting space overhead to avoid fetching unnecessary neighboring pages.

The excerpt does not say every Mica page uses RLE. Different pages and columns can use different encodings.

Related: [[Rows Per Page]], [[Variable Physical Page Layout]].

Paper context: [[4 Mica - File Format Design#4.5 Page-Local Decode Self-Containment|§4.5 Page-local decode self-containment]].
