"""Fix seeded Independent Set cases before constructing a reduction."""

import json
import random
from pathlib import Path


EDGE_CASES = [
    (0, [], 0, True), (0, [], 1, False),
    (1, [], 0, True), (1, [], 1, True), (1, [], 2, False),
    (2, [], 2, True), (2, [[0,1]], 2, False), (2, [[0,1]], 1, True),
    (3, [[0,1],[1,2],[0,2]], 2, False),
    (3, [[0,1],[1,2]], 2, True), (3, [[0,1],[1,2]], 3, False),
    (3, [], 3, True),
    (4, [[0,1],[1,2],[2,3],[0,3]], 2, True),
    (4, [[0,1],[1,2],[2,3],[0,3]], 3, False),
    (4, [[u,v] for u in range(4) for v in range(u+1,4)], 1, True),
    (4, [[u,v] for u in range(4) for v in range(u+1,4)], 2, False),
    (4, [[0,1],[0,2],[0,3]], 3, True),
    (4, [[0,1],[0,2],[0,3]], 4, False),
    (4, [[0,1],[2,3]], 2, True), (4, [[0,1],[2,3]], 3, False),
]


def random_source(seed):
    rng = random.Random(seed)
    n = rng.randint(1, 7)
    edges = [[u,v] for u in range(n) for v in range(u+1,n) if rng.random() < 0.38]
    if seed % 2 == 0:
        order = list(range(n))
        rng.shuffle(order)
        chosen = []
        for vertex in order:
            if not any({vertex, prior} == set(edge) for prior in chosen for edge in edges):
                chosen.append(vertex)
        threshold = len(chosen)
    else:
        threshold = rng.randint(1, n+1)
    return {"vertices":n,"edges":edges,"threshold":threshold}


def build_cases():
    from check import solve_source
    cases, seen = [], set()

    def add(source, kind, seed=None, hand_answer=None):
        key = json.dumps(source, sort_keys=True, separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_source(source)
        if hand_answer is not None and ("set" in answer) != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        case = {"source":source,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for n,edges,k,expected in EDGE_CASES:
        add({"vertices":n,"edges":edges,"threshold":k},"edge",hand_answer=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")
