"""Independent exact oracles for Independent Set and three-agent maximal EF1."""

import argparse
import json
import random
import subprocess
import sys
from fractions import Fraction
from itertools import product
from math import lcm
from pathlib import Path

import z3


def legal_graph(n, edges):
    if type(n) is not int or n < 0 or not isinstance(edges, list):
        return False
    seen = set()
    for edge in edges:
        if (not isinstance(edge, list) or len(edge) != 2
                or any(type(v) is not int or not 0 <= v < n for v in edge)
                or edge[0] == edge[1]):
            return False
        key = tuple(sorted(edge))
        if key in seen:
            return False
        seen.add(key)
    return True


def legal_source(source):
    return (isinstance(source, dict) and legal_graph(source.get("vertices"), source.get("edges"))
            and type(source.get("threshold")) is int and source["threshold"] >= 0)


def direct_independent(source, vertices):
    if not legal_source(source) or not isinstance(vertices, list):
        return False
    n = source["vertices"]
    return (len(vertices) >= source["threshold"]
            and all(type(v) is int and 0 <= v < n for v in vertices)
            and len(set(vertices)) == len(vertices)
            and all(not (u in vertices and v in vertices) for u, v in source["edges"]))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal Independent Set instance")
    n = source["vertices"]
    for bits in product((False,True), repeat=n):
        vertices = [v for v in range(n) if bits[v]]
        if direct_independent(source, vertices):
            return {"set": vertices}
    return {"status":"NO-SOLUTION"}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_source(source) == output
    return set(output) == {"set"} and direct_independent(source, output["set"])


def legal_target(target):
    if not isinstance(target, dict):
        return False
    n = target.get("goods")
    values = target.get("values")
    return (legal_graph(n, target.get("edges"))
            and isinstance(values, list) and len(values) == n
            and all(isinstance(pair, list) and len(pair) == 2
                    and all(type(x) is int for x in pair)
                    and pair[0] >= 0 and pair[1] > 0 for pair in values))


def direct_allocation(target, bundles):
    if not legal_target(target) or not isinstance(bundles, list) or len(bundles) != 3:
        return False
    n = target["goods"]
    if not all(isinstance(bundle,list) and all(type(g) is int and 0 <= g < n for g in bundle)
               for bundle in bundles):
        return False
    assigned = [g for bundle in bundles for g in bundle]
    if len(set(assigned)) != len(assigned):
        return False
    edges = [set(edge) for edge in target["edges"]]
    if any(edge <= set(bundle) for edge in edges for bundle in bundles):
        return False
    for g in set(range(n)) - set(assigned):
        if any(not any(g in edge and edge & set(bundle) for edge in edges)
               for bundle in bundles):
            return False
    values = [Fraction(*pair) for pair in target["values"]]
    totals = [sum((values[g] for g in bundle), Fraction(0)) for bundle in bundles]
    return all(not bundles[j] or totals[i] >= totals[j] - max(values[g] for g in bundles[j])
               for i in range(3) for j in range(3) if i != j)


def target_solutions(target, limit=3):
    if not legal_target(target):
        raise ValueError("Illegal three-agent allocation instance")
    n = target["goods"]
    assignment = [z3.Int(f"agent_{g}") for g in range(n)]
    solver = z3.Solver()
    for owner in assignment:
        solver.add(owner >= -1, owner <= 2)
    for u,v in target["edges"]:
        solver.add(z3.Or(assignment[u] == -1, assignment[v] == -1, assignment[u] != assignment[v]))
    neighbors = [set() for _ in range(n)]
    for u,v in target["edges"]:
        neighbors[u].add(v)
        neighbors[v].add(u)
    for g in range(n):
        for agent in range(3):
            solver.add(z3.Implies(assignment[g] == -1,
                                  z3.Or(*[assignment[h] == agent for h in neighbors[g]])))
    denominator = lcm(*(pair[1] for pair in target["values"]))
    weights = [pair[0]*(denominator//pair[1]) for pair in target["values"]]
    totals = [z3.Sum(*[z3.If(assignment[g] == agent, weights[g], 0)
                        for g in range(n)]) for agent in range(3)]
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            solver.add(z3.Or(z3.And(*[assignment[g] != j for g in range(n)]),
                             *[z3.And(assignment[g] == j, totals[i] >= totals[j]-weights[g])
                               for g in range(n)]))
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive target solver: {result}")
        model = solver.model()
        owners = [model.eval(owner).as_long() for owner in assignment]
        bundles = [[g for g, owner in enumerate(owners) if owner == agent]
                   for agent in range(3)]
        if not direct_allocation(target, bundles):
            raise AssertionError("Z3 allocation violates direct predicate")
        outputs.append({"bundles": bundles})
        solver.add(z3.Or(*[owner != value for owner, value in zip(assignment, owners)]))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target, 1)[0]


def valid_target(target, output):
    if not legal_target(target) or not isinstance(output, dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"bundles"} and direct_allocation(target, output["bundles"])


def exhaustive_target(target):
    for owners in product((-1,0,1,2), repeat=target["goods"]):
        bundles = [[g for g, owner in enumerate(owners) if owner == agent]
                   for agent in range(3)]
        if direct_allocation(target, bundles):
            return {"bundles": bundles}
    return {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES, random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable, str(root / "research/validate_preparation.py"), str(path)], check=True, cwd=root)
    cases = json.loads(path.read_text())
    for n, edges, k, expected in EDGE_CASES:
        assert ("set" in solve_source({"vertices":n,"edges":edges,"threshold":k})) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        assert ("set" in current) == ("set" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    checked = 0
    for seed in range(64):
        rng = random.Random(seed)
        n = rng.randrange(6)
        edges = [[u,v] for u in range(n) for v in range(u+1,n) if rng.randrange(2)]
        values = [[rng.randrange(4), rng.choice((1,2,3))] for _ in range(n)]
        target = {"goods":n,"edges":edges,"values":values}
        assert ("bundles" in solve_target(target)) == ("bundles" in exhaustive_target(target))
        checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive allocation instances")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)], input=json.dumps(source), text=True, capture_output=True, check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal target: {target}")
        for output in target_solutions(target):
            if not valid_target(target, output):
                raise AssertionError(f"Invalid target oracle output: {output}")
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"], input=json.dumps(payload), text=True, capture_output=True, check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
