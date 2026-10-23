---
tags: []
created: 2026-10-15
description: Stress-test ledger documenting rejected narrative candidates, two rounds of adversarial review, and falsification criteria.
aliases:
  - Mica Stress Test
  - stress-test
---

# Stress-test and revision record

**Updated:** 2026-10-14. Sections 1–8 preserve the September 28 analytical reviews and planning history. Section 9 reconciles the completed September 29 execution study. Historical statements about pending staging work or no new measurements describe their original checkpoint; the current status is in [[experiments#evaluation-status|experiments.md]]. No new benchmark or literature review was run for this reconciliation, and it does not certify venue readiness.

1. **Candidate stories that did not survive**

| Candidate | Strongest objection | Evidence or counterexample | Revision |
|---|---|---|---|
| “Small pages plus io_uring unlock NVMe.” | Both are established, and the original hardware comparison confounds request overlap, granularity and I/O interface. | Lance and NVMe literature; local large-strided-read source. | Remove this as the principal novelty. E09 becomes a controlled hardware boundary study. |
| “The new insight is pruning metadata with metadata.” | This is directly described in prior work. | SMA section 4 and Big Metadata section 5.8, cited in [[prior-art|prior-art.md]]. | Attribute the idea; investigate a specific representation/execution dependency instead. |
| “Shared page identity makes software cost depend only on survivors.” | Shared row grouping has predecessors; current code has dense bitmaps, coarse summaries and per-page plans. | ORC and current Mica source in [[evidence|evidence.md]]. | Keep alignment as a tested design choice; account for total pages, intermediate candidates and columns. |
| “Cold-cache wins prove the design matters.” | A service can reuse parsed readers. Metadata pressure depends on files admitted by outer pruning, not total dataset size. | Reader ownership paths and the distinction between OS bytes and parsed objects. | Add persistent readers, relevant working-set measurement and independent admission/reuse axes in E03. |
| “An improved latency/memory frontier is automatically novel.” | Any indexing implementation can change that frontier; prior designs may already implement the same mechanism. | Current Vortex, Nimble, ORC and Pixels overlap. | Require source-level distinction and a consequential mechanism or interaction, as well as performance evidence. |

The retained contribution is making fine-grained pruning economical through metadata organization and reader execution. Current implementation and historical measurements support it as a credible systems contribution. Its distinctiveness and practical breadth remain to be demonstrated. The later reassessment in section 7 corrects the earlier tendency to infer too much from component-level precedents; it does not certify venue readiness.

2. **First independent adversarial review and changes made**

The first review evaluated a concrete candidate argument before the final experiment document was written. It found the scope defensible but warned that a memory-budget study could become a cache benchmark without a distinct systems insight.

| Objection | Change in final package | Remaining empirical obligation |
|---|---|---|
| Warm metadata bytes are not reused parsed metadata. | E03 distinguishes absent bytes, resident bytes with reconstruction, persistent objects and bounded reuse. | Verify actual object ownership and charge preparation/reconstruction. |
| Table-level pruning may make the reachable working set small. | E03 varies admitted files, hot-set/reuse distance and predicate/projection width; includes effective external pruning. | Demonstrate a credible access distribution instead of constructing only random-file pressure. |
| A sidecar matching Mica is not a single outcome. | Storyline and E02 distinguish a portable substantive organization, a simpler established index, and an equivalent existing native layout. | Measure and describe which mechanism the sidecar actually needs. |
| Remove-one-component ablations do not show co-design. | E05 includes membership × metadata access × alignment interventions and interaction analysis. | Construct comparable variants; don't confound alignment with extra index precision or encoding. |
| Known-row retrieval has its own mapping and decode costs. | E01 charges per-format row mapping and codec dependencies; forbids subtraction of independent medians as discovery time. | Implement the diagnostic adapter and handle variable row counts after bisection. |
| Native exact indexes are stronger than page membership for tiny results. | E02/E07 include native index portfolios and a mature engine alternative with separate system boundary. | Let native indexes use exact row locations and account for build/space costs. |
| Defining the useful region after seeing results is unfalsifiable. | E04 freezes intended queries/distributions and reports coverage of the benefit region. | Keep losses in the workload rather than changing scope to remove them. |
| One unused wide column can harm every queried column. | E07 adds a heavy-tailed unqueried column while keeping queries and numeric values unchanged. | Measure shared bisection, metadata and compression costs. |

3. **Second review and source corrections**

The second round reviewed the actual storyline and experiment files against both code and prior art. It found several remaining control gaps.

- E03 now defines a common byte-accounted LRU diagnostic and a separate best-native policy lane. Evicted-but-live objects and shared ownership stay charged. Oversized entries are transient, and fixed residency above budget is reported as infeasible. The total-memory lane requires verified accounting of process-group memory and filesystem cache; an unenforced observed curve cannot establish a hard budget.
- The cost model now distinguishes total schema columns from queried columns. Prepared-file initialization loads all-column coarse summaries; request-aware adaptive opening can select relevant columns. E05 grows total schema width with queried width fixed.
- Nimble gets a focused metadata test because its verified partial overlap targets the central cost. Whole-contract equivalence is not required before taking a competitor seriously.
- The introduction says the reader exposes work through adapters with execution limits. It no longer asserts an unverified aggregate engine resource bound.
- The third corpus is concretely specified as GH Archive events with a fixed date range, flat schema, query families and held-out dates. It is real event data with synthetic queries, not a production trace.
- The S2 failure wording now agrees with the portability branch. A sidecar implementing the proposed organization is not automatically a novelty failure; simpler known machinery reproducing it is a different outcome.

The source audit also corrected fully self-contained decode language, the assumption that every page is a fixed number of bytes, the default-v2 versus evaluated-v3 distinction, and the meaning of current predicate sinks. These corrections prevent the new story from silently claiming capabilities the code does not provide.

4. **Questions the final package must answer for a skeptical reviewer**

| Reviewer question | Current answer | Experiment that can overturn it |
|---|---|---|
| Why is this more than SMA or BigQuery metadata pruning? | Mica connects fine metadata access to shared row partitions and physical execution. Code and measurements support that systems argument; the prior papers establish overlap, not complete equivalence. The distinct cost advantage remains to be tested. | E01/E02/E05 plus primary-source mechanism comparison. |
| Why not ORC, Vortex or Nimble? | They are serious alternatives with overlapping capabilities, not dismissed categories. | E02 native/focused comparisons and E03 reuse states. |
| Why not a normal secondary index? | The broad predicate-portfolio case is a hypothesis; rare lookups alone may favor exact indexes. | E02/E07 index coverage, build and storage tradeoff. |
| Why a new format? | Format replacement is not a premise. A portable version may be the stronger outcome. | E02 sidecar and aligned-writer interventions. |
| Are cold-cache assumptions artificial? | Cold is one diagnostic endpoint; the intended deployment must survive parsed-reader reuse and admission-aware budgets. | E03. |
| Does this really scale with survivors? | Total cost does not. The model includes file/schema-sized and intermediate-candidate work. | E05 fixed-survivor and schema-width sweeps. |
| Does logical selectivity guarantee saved I/O? | No. Page occupancy, index discrimination and predicate correlation intervene. | E04. |
| Do the speedups survive full SQL and concurrency? | Historical engine evidence is promising but incomplete for the revised claim. | E06/E08. |
| Is the storage/write cost acceptable? | This is unresolved under native compression/index portfolios. | E07. |
| Are the policies adaptive or optimal? | Current thresholds are heuristics. No optimality claim is made. | E05 and conditional policy study in [[design-extensions|design-extensions.md]]. |

5. **What survived, and what has not been established**

The revised argument survives the identified logical counterexamples by stating what the code does, crediting prior mechanisms, and making the strongest alternatives capable of falsifying it. The plan now separates metadata bytes from reconstruction, logical rows from physical pages, native competition from mechanism controls, and empirical efficacy from originality.

It has not established novel mechanism superiority, a representative constrained-residency workload, baseline dominance, peak-memory savings, or concurrent robustness. Those are the experiments to perform, not achievements of this planning session.

Interpret each failed hypothesis at its actual scope. Portability can strengthen the contribution; an unimportant alignment effect can narrow it; an unrepresentative memory-pressure case can change the deployment claim. Reconsider the overall contribution when strong alternatives explain the result at comparable costs with no substantive systems insight remaining. Neither familiar components nor a single negative ablation warrants that conclusion.

6. **Final targeted verification and deliverable audit**

Before the section 7 reassessment, a final independent read confirmed the second-round corrections in the then-current files and checked the path-specific coarse-metadata statement against code. It found no further materially misleading statements within that targeted scope. This is not a claim that external reviewers will accept the paper or that the proposed experiments will succeed.

| Requested outcome | Current document evidence | Completion boundary |
|---|---|---|
| Storyline covering introduction, motivation and design | storyline.md contains proposed introductory prose, motivation figures and code-qualified design explanation. | Proposed argument, not fabricated empirical findings. |
| All added/reused experiments in a separate document | experiments.md specifies E00–E09, shared controls, explicit reuse choices, analysis and failure rules; storyline links to their entries. | Experimental specification complete; future implementations/runs not claimed complete. |
| Prior art and positioning | prior-art.md cites primary sources and separates verified overlap from unresolved equivalence; evidence.md checks current implementation. | A credible systems contribution is supported; comparative originality remains unresolved. |
| Extensions only if necessary | design-extensions.md separates required study support from measurement-triggered architecture changes. | No speculative extension is represented as implemented or automatically novel. |
| Stress-test and refinement | This document records rejected candidates, two adversarial rounds and final targeted verification. | Logical/source review completed; empirical gates remain open. |
| Organized folder | README.md indexes every document under docs/sosp-osdi-storyline. | Historical plans remain historical; no benchmark statuses changed. |

Local document links and experiment anchors were checked after the final edits. The implementation revision, old measurement settings and new study status are stated explicitly throughout the package.


7. **Contribution-level reassessment after the novelty clarification**

The follow-up review rechecked the distinction between inventing pruning techniques and making fine-grained pruning economical through a system design. The earlier headline verdict gave component-level precedents too much weight. SMA and Big Metadata establish that metadata hierarchies and metadata pruning are familiar. They do not establish that Mica's complete representation and execution organization has already been provided at the same cost. Conversely, the broad goal of efficient metadata is not itself a novelty claim.

**Revised assessment.** Mica has a credible systems contribution, supported by current code and historical granularity, metadata-ablation and full-query evidence. The remaining obligation is to explain and establish its difference from the closest complete designs, causal benefit and useful workload region. This revision introduces no new performance result and does not mark G1–G3 passed.

The package now leads with making fine-grained pruning economical. Limited metadata residency is an evaluation axis rather than an established premise. E01 explicitly compares tuned native readers, eager-metadata Mica and full Mica across granularity, with identical files and index information for the Mica pair. E02 distinguishes information advantage, portable organization and equivalent established design. E05 tests claimed interactions without requiring superadditivity. The design-extension guidance prioritizes measured limitations over adding mechanisms to make familiar techniques appear novel.

The remaining concerns are preserved: parsed-reader reuse, native and matched-information alternatives, alignment costs, occupancy/correlation, storage and build cost, shared codec dependencies, exact semantics and aggregate resource behavior. No universal survivor-only complexity, full deferred-projection-I/O capability or format-necessity claim was introduced.


8. **Close the motivation-to-format reasoning gap**

The user identified that the revised motivation still resembled the original small-page story and did not answer why a new format was warranted. The missing inference was from observed reader overhead to a benefit from changing the stored representation. Neither the historical Parquet granularity result nor the within-Mica eager-loading ablation establishes that inference.

The storyline now separates S2a, economical fine-metadata organization, from S2b, the additional advantage of an integrated layout. E02a tests unchanged-file reader improvements, equivalent sidecar metadata, a compatible rewritten layout when residual costs warrant it, and Mica. E02b supplies dependency traces and identical-candidate retrieval controls. E05 performs the causal substitutions; E06 promotes the strongest compatible baseline; E07 measures adoption against that baseline. Figure M4 makes this argument visible next to the design.

The decision branches now distinguish reader-only improvements, portable metadata, compatible layout policy, an integrated-layout advantage and an unexplained gap. Passing S2a does not pass S2b. A single-query speedup or the absence of a convenient writer API cannot establish a format requirement. Practical equivalence requires enough precision and comparable costs. All new lanes remain proposed, and no format-necessity claim or benchmark result was added.


9. **Reconciliation with completed predicate-first evidence, 2026-10-14**

The closing commit `5fb5225` and final report establish that staging was implemented and its bounded study completed. A later conversational recap incorrectly described it as unimplemented. Some package paragraphs already recorded completion, but the experiment preamble, extension trigger and status mapping remained inconsistent. Those descriptions are now reconciled.

The completed result supports physical projection-page skipping and the dependence on survivor placement. It also provides counterevidence to an unconditional staging-speedup claim: the real compound case saves bytes while increasing requests, and both dense engine queries regress. The selected cross-format benefit already exists in combined mode. These results support S1's execution argument and restrict S3; they do not pass S2a or S2b.

The package now distinguishes completed scoped correctness and execution tests from open E01/E02/E03/E07/E08 requirements, uses a mode-specific design diagram, and retains both performance losses and the small observed default-path cost. Strict aggregate admission, automatic selection and pipelining remain deferred. This update does not reopen the implementation study or rewrite its benchmark artifacts.

---

## Vault Navigation & MoC Context

- [[Mica]]: Central Level 3 Project Hub for Mica paper notes and core concepts.
- [[README|Mica Plan Overview]]: Master roadmap and synthesis of the SOSP/OSDI research plan.
- [[storyline|Mica Storyline]]: Proposed SOSP/OSDI research storyline and core claims S1–S3.
- [[prior-art|Mica Prior Art]]: Primary-source positioning and novelty analysis.
- [[experiments|Mica Experiments]]: Comprehensive experimental campaign E00–E09.
- [[evidence|Mica Evidence]]: Implementation status audit and empirical evidence synthesis.
- [[design-extensions|Mica Design Extensions]]: Infrastructure requirements and conditional architecture extensions.

