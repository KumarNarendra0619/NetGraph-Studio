from netgraph.adapter import OPERATIONS


def test_expected_core_operations_are_mapped():
    expected = {"knn", "delaunay", "gabriel", "rng", "mst", "radius", "waxman", "contiguity"}
    assert expected.issubset(OPERATIONS)


def test_operations_use_public_city2graph_callables():
    for operation in OPERATIONS.values():
        assert callable(operation.function)
