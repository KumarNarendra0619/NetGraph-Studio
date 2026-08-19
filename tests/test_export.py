"""Export regression tests for NetGraph Studio."""

import networkx as nx

from netgraph.export import edge_list_bytes, gml_bytes, graphml_bytes


def sample_graph():
    graph = nx.Graph()
    graph.add_edge(0, 1, weight=2.5)
    graph.add_edge(1, 2, weight=1.0)
    return graph


def test_graphml_export_is_nonempty():
    data = graphml_bytes(sample_graph())
    assert data
    assert b"graphml" in data.lower()


def test_gml_export_is_nonempty():
    data = gml_bytes(sample_graph())
    assert data
    assert b"graph" in data.lower()


def test_edge_list_export_is_stable():
    data = edge_list_bytes(sample_graph()).decode("utf-8")
    assert data.splitlines() == ["0 1", "1 2"]
