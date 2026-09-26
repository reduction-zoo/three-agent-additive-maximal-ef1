# Independent Set → Three-agent additive maximal EF1 allocation

Category: Complexity open

## Source

The source gives a simple graph and an integer threshold. Its outputs are independent sets of at least that size, or NO-SOLUTION.

## Target

The target gives goods with a conflict graph and identical nonnegative rational additive values for three agents. Find three disjoint independent bundles forming an EF1 partial allocation that is maximal under adding any single unallocated good to any bundle.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

This tests whether fairness remains algorithmically accessible when feasibility conflicts and maximality interact, even for three identical agents.

## Difficulty

Maximality is local while EF1 is global. A reduction must handle empty bundles and all ways to leave goods unallocated.

## Literature context

Existence of unconstrained EF1 allocations does not settle maximal partial allocation when every bundle must also satisfy a conflict graph.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Dividing Conflicting Items Fairly](https://arxiv.org/html/2506.14149v1): Igarashi, Manurangsi and Yoneda, Dividing Conflicting Items Fairly, arXiv:2506.14149v1 (2025), Section 4.1 after Theorem 11, explicitly asks about three agents with additive valuations. Proposition 12 handles at least four agents. Theorem 11 uses non-additive valuations. Neither settles this target. The final IJCAI paper, Section 6, retains the three-agent additive question.
- [final IJCAI paper](https://www.ijcai.org/proceedings/2025/0435.pdf): Igarashi, Manurangsi and Yoneda, Dividing Conflicting Items Fairly, arXiv:2506.14149v1 (2025), Section 4.1 after Theorem 11, explicitly asks about three agents with additive valuations. Proposition 12 handles at least four agents. Theorem 11 uses non-additive valuations. Neither settles this target. The final IJCAI paper, Section 6, retains the three-agent additive question.
- [Fair Allocation under Conflict Constraints](https://arxiv.org/html/2605.09930v1): Fair Allocation under Conflict Constraints (May 2026), Table 1, Proposition 2 and Theorem 5.2, still separate three-agent monotone hardness from nonnegative additive hardness for at least four agents. Its additive hardness with fewer agents permits negative weights. Its path-graph existence results do not settle arbitrary conflict graphs.

Fixed from board record `website/questions/three-agent-additive-maximal-ef1.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
