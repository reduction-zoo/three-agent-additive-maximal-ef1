# Preparation evidence

Prepared on 2026-09-26 before constructing a candidate. The fixed corpus has
120 distinct legal Independent Set instances: 20 hand-labelled edge cases
and 100 seeded random cases, with 86 YES and 34 NO decisions and zero to
seven vertices. `generate_cases.py` retains all seeds; `cases.json` stores
expected outputs. The source oracle enumerates all vertex subsets. Returned
sets are checked directly for size and independence; NO-SOLUTION follows
only after exhaustive enumeration.

The target oracle uses Z3 4.16.0 with one integer owner per good, taking an
agent index or unallocated. Edge constraints enforce independent bundles.
For an unallocated good, each agent must own a neighboring good. Exact
rational values are scaled by their common denominator, and EF1 is encoded
as a disjunction over each possible removed good. Every Z3 model is checked
again by direct conflict, maximality and `Fraction` value calculations.
UNSAT is conclusive; unknown is an error. Independent exhaustive enumeration
of all four ownership choices per good agreed with Z3 on 64 target instances
of zero to five goods. Hand fixtures reject a nonmaximal empty allocation,
including a zero-value good, an EF1 violation, a conflict, malformed source
edges and negative values.

[The source paper](https://arxiv.org/html/2506.14149v1) defines maximality
by feasible addition, and EF1 by removing one good from the envied bundle.
All 64 tested target instances have a maximal EF1 allocation. The existence
of a three-agent additive counterexample is the open question itself; this
finite test set does not claim one or exercise a genuine negative target.
The NO-SOLUTION validator rejects it on every positive target and accepts it
only after conclusive Z3 UNSAT.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/three-agent-additive-maximal-ef1/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates every random source,
rechecks labels and witnesses, and compares target decisions to exhaustive
enumeration. The candidate runner uses separate forward and recovery
subprocesses and up to three target allocations per source. An incorrect
injected candidate was rejected after solving its target and invalidating
recovery. No actual reduction candidate exists; finite tests do not prove
one or settle the existence question.
