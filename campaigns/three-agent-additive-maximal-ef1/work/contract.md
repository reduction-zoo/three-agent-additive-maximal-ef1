# Prepared input and output contract

The Independent Set source input is `{"vertices": n, "edges": [[u,v],
...], "threshold": k}` with a simple undirected graph on `0..n-1` and
nonnegative integer `k`. A source output is `{"set": [distinct_vertices]}`
forming an independent set of size at least `k`, or
`{"status": "NO-SOLUTION"}` exactly when none exists.

The target input is `{"goods": m, "edges": [[u,v], ...], "values":
[[numerator, denominator], ...]}` with a simple conflict graph and one
nonnegative rational value per good, shared by three agents. A target output
is `{"bundles": [agent_0_goods, agent_1_goods, agent_2_goods]}`: disjoint
independent bundles. It is EF1 if each agent's total value is at least the
other bundle's value after removing some good from that other bundle (empty
other bundles pass). It is maximal if every unallocated good conflicts with
at least one good in each agent's bundle. Maximality refers to feasibility of
adding a good, regardless of whether the enlarged allocation would retain
EF1. `{"status": "NO-SOLUTION"}` is valid only if no maximal EF1
allocation exists.

A candidate `algorithm.py` reads one source JSON object from stdin and writes
one legal target JSON object to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. The commands share no memory, exit nonzero on errors and send
diagnostics to stderr. They must be deterministic and polynomial time, and
recovery must work for every valid target output.

`check.py --candidate PATH` independently solves each target produced from
the fixed source corpus and directly validates recovered source outputs.
