---
tags: []
created: 2026-10-15
description: Master roadmap and synthesis of the SOSP/OSDI research plan, experiment matrix, and evidence for Mica fine-grained columnar pruning.
aliases:
  - Mica Plan
  - mica-plan
  - Mica SOSP Plan
---

# Mica SOSP/OSDI storyline and evidence plan

Updated 2026-10-14 to reconcile the completed predicate-first study, closed in `5fb5225` with experimental core frozen at `cbb11fc`. Original assessment prepared 2026-09-28 from implementation at `b00564d810596a8bd2361fcbacbf4a7abaa19ee4`, the supplied manuscript, existing experiment artifacts and primary-source related work. This package revises the September assessment and records adversarial review of the new argument. The original positioning assessment remains historical; the 2026-09-29 predicate-first update below reports a completed bounded execution study. It does not replace the separate format-necessity evaluation.

**Recommended direction.** Center the paper on making fine-grained columnar pruning economical through coordinated metadata organization, row partitioning and reader execution. Fine pruning saves data work only when metadata discovery, cross-column mapping and physical execution do not consume the savings. Metadata residency is an important evaluation axis; limited residency is not yet an established deployment premise.

**Current assessment.** Mica has a credible systems contribution in making fine-grained pruning practical. Current code, the granularity diagnosis, selective-metadata ablations and full-query measurements support that interpretation. The distinctiveness of the organization relative to the closest systems, the causal role of each design choice, and the breadth of its practical benefit remain incompletely demonstrated. Prior hierarchical summaries constrain claims about individual techniques; their existence does not establish that Mica lacks a systems contribution. Strong SOSP/OSDI readiness remains an evaluation question.

| Status | Current conclusion | Evidence or next step |
|---|---|---|
| Implemented | Shared row partitions, selectively addressable detail metadata and separate physical batching form a concrete design. | [[evidence|Code audit]]. |
| Supported in recorded settings | Fine Parquet pages can increase metadata cost; Mica selectively accesses fine metadata and benefits complete queries. | [[evidence#current-assessment|Evidence synthesis]]. Historical measurements, not new runs. |
| Completed execution study | Explicit predicate-first can omit projection I/O; physical placement controls savings, and selected real full queries do not establish a general staging speedup. Defaults remain combined, exact sink disabled. | [[evidence#predicate-first-results|Evidence and claim status]]; [[experiments#evaluation-status|evaluation status]]. |
| Still unresolved | How much the organization adds beyond strong native alternatives, equivalent indexing and legitimate metadata reuse. | [[experiments#e01|E01]], [[experiments#e02|E02]], [[experiments#e03|E03]], [[experiments#e05|E05]]. |
| Not required | A new Bloom-filter algorithm, proof that existing formats cannot implement the design, or superiority in every regime. | [[prior-art#contribution-standard|Contribution standard]]. |
| Still required | A distinct, consequential systems result with credible workload coverage and full cost accounting. | S1–S3 and gates G0–G3. |

| Document | What it contains |
|---|---|
| [[storyline|Storyline]] | Proposed introduction prose, motivation figures, design narrative, three claims, boundaries and paper-direction decisions. |
| [[experiments|Experiments]] | E00–E09, with setup/run/analysis, baselines, cache and resource controls, reuse decisions and falsifiers. |
| [[prior-art|Prior art and positioning]] | Primary-source comparison with SMA, Big Metadata, ORC, Parquet, Vortex, Lance, FastLanes, Nimble, Pixels and column-store predecessors. |
| [[evidence|Implementation and existing evidence]] | Code-backed capabilities and limits, historical results, artifact availability and what must be rerun. |
| [[design-extensions|Conditional design extensions]] | Required study infrastructure and measurement-triggered reader changes, with correctness and evaluation obligations. |
| [[stress-test|Stress-test record]] | Rejected stories, independent review findings, revisions, remaining empirical risks and stop/reframe criteria. |

Start with the storyline and its S1–S3 claim table. Then read E01–E05 and the prior-art verdict before scheduling the full evaluation campaign.

The predicate-first study is complete under its bounded single-query contract. Its final decision report retains explicit experimental staging and rejects default promotion: 3,750 accepted measurements show large clustered-control gains, but roughly 19–23% dense full-query losses versus combined-empty-skip. Strict production aggregate admission remains unsupported. This study does not establish format necessity or a general real-query staging speedup.

The next broader-format study should combine E00 provenance/correctness with an E01 granularity sweep of tuned native readers, Mica with eager fine metadata and full Mica. Keep the Mica pair's layout and pruning information identical. Include E02 matched-information and closest-native pilots, E03 reused-reader controls, and E04 loss cases. This directly tests whether the proposed organization makes useful finer pruning economical. Expand the full engine, cost, concurrency and hardware studies after this pilot identifies the cause and operating region.

The key addition is the [[storyline#format-rationale|format rationale]]. It separates S2a, the metadata/reader organization contribution, from S2b, the incremental value of the integrated layout. [[experiments#e02a|E02a]] compares unchanged-file reader improvements, equivalent sidecars, compatible layout rewrites and Mica. [[experiments#e02b|E02b]] traces and tests the residual dependencies. E07 then asks whether the advantage justifies conversion and adoption costs. A new format is an implementation choice today; its comparative advantage is a claim to establish.

**Continuity.** This package is the current paper-positioning plan. Reconciliation on 2026-10-14 changes documentation only; it does not rerun or reopen the completed September execution study. Follow the [[experiments#evaluation-status|status matrix]], rather than interpreting every setup/run paragraph as unexecuted work. The scoped predicate-first implementation and evaluation are complete; the broader E00–E09 studies remain proposed except for explicitly linked completed or historical evidence. Do not treat deferred allocator accounting, every metadata mode or every adapter improvement as prerequisites for the completed execution study. The repository's older root research plan retains its historical status and is not a current implementation inventory.

The user-requested deliverables are all represented: introduction/motivation/design in storyline.md; add/reuse experiment specifications in experiments.md; related-work positioning in prior-art.md; and extensions only where a measured failure warrants them in design-extensions.md. The evidence and stress-test documents make the reasoning reviewable.

The decision procedure evaluates a systems contribution, not the novelty of each ingredient. Proceed when an explainable organization or systems finding changes a consequential tradeoff. A portable implementation can strengthen that result. Reconsider the contribution if the closest established design already provides the same organization and outcome under comparable costs, with no remaining substantive insight. A familiar component, an additive ablation result, or a matching sidecar alone is not such a finding.

---

## Vault Navigation & MoC Context

- [[Mica]]: Parent Level 3 Project Hub for the Mica research project and file format notes.
- [[storyline|Mica Storyline]]: Proposed introduction prose, motivation figures, design narrative, three claims, boundaries, and paper-direction decisions.
- [[experiments|Mica Experiments]]: Comprehensive experimental campaign E00–E09 evaluating granularity sweeps, baseline comparisons, metadata lifecycle, and engine queries.
- [[prior-art|Mica Prior Art]]: Primary-source comparison with SMA, Big Metadata, ORC, Parquet, Vortex, Lance, FastLanes, Nimble, Pixels, and column-store predecessors.
- [[evidence|Mica Evidence]]: Implementation status audit, historical measurements, code-backed capabilities, and completed predicate-first bounded study results.
- [[design-extensions|Mica Design Extensions]]: Required study infrastructure and measurement-triggered reader changes, with correctness and evaluation obligations.
- [[stress-test|Mica Stress Test]]: Rejected narrative candidates, two rounds of adversarial review findings, revisions, empirical risks, and falsification criteria.
- [[Projects/mica/mica-plan/E00|E00 — Can we trust the comparison?]]: Plain-language checks for matched data, correct answers, recorded settings, and traceable results.
- [[Projects/mica/mica-plan/E01|E01 — Does smaller-page pruning pay off?]]: Self-contained tests stating the action, what it reveals, and existing versus required code.
- [[Projects/mica/mica-plan/E02|E02 — Which explanation accounts for the speed difference?]]: Concrete questions answered by each comparison, with implementation actions and existing versus required code.
- [[Projects/mica/mica-plan/E03|E03 — Does Mica still help when file maps are cached?]]: Short plan for testing metadata reuse across files under limited memory.
- [[Projects/mica/mica-plan/E04|E04 — When does Mica help, and when does it lose?]]: Six-case pilot testing match count and row placement, with required code and result-driven next steps.
- [[Projects/mica/mica-plan/E07|E07 — Is Mica's speed worth its cost?]]: Reuses E00–E04 results and specifies the added writing, storage, wide-column, and adoption-cost checks.
