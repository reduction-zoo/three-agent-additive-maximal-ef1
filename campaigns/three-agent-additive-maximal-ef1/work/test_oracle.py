from check import legal_source, solve_source, valid_source, legal_target, solve_target, valid_target


def test_hand_cases():
    edge = {"vertices": 2, "edges": [[0,1]], "threshold": 2}
    assert solve_source(edge) == {"status":"NO-SOLUTION"}
    assert not valid_source(edge, {"set":[0,1]})
    assert valid_source({**edge,"threshold":1}, {"set":[0]})
    assert not legal_source({"vertices":1,"edges":[[0,0]],"threshold":0})
    one = {"goods":1,"edges":[],"values":[[1,1]]}
    assert valid_target(one,{"bundles":[[0],[],[]]})
    assert not valid_target(one,{"bundles":[[],[],[]]})
    assert "bundles" in solve_target(one)
    zero = {"goods":1,"edges":[],"values":[[0,1]]}
    assert not valid_target(zero,{"bundles":[[],[],[]]})
    four = {"goods":4,"edges":[],"values":[[1,1]]*4}
    assert not valid_target(four,{"bundles":[[0,1,2,3],[],[]]})
    conflict = {"goods":2,"edges":[[0,1]],"values":[[1,1],[1,1]]}
    assert not valid_target(conflict,{"bundles":[[0,1],[],[]]})
    assert not legal_target({"goods":1,"edges":[],"values":[[-1,1]]})


if __name__ == "__main__":
    test_hand_cases()
