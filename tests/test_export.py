"""Export regression and round-trip tests for NetGraph Studio."""

import io

import networkx as nx

from netgraph.export import edge_list_bytes, gml_bytes, graphml_bytes


def sample_graph():
    graph = nx.Graph()
    graph.add_node(0, name="A")
    graph.add_node(1, name="B")
    graph.add_edge(0, 1, weight=2.5, relation="nearest")
    graph.add_edge(1, 2, weight=1.0, relation="nearest")
    return graph


def sample_directed_graph():
    graph = nx.DiGraph()
    graph.add_edge("A", "B", weight=3.0)
    graph.add_edge("B", "A", weight=1.0)
    return graph


def test_graphml_export_is_nonempty_and_round_trippable():
    data = graphml_bytes(sample_graph())
    assert data
    assert b"graphml" in data.lower()

    restored = nx.read_graphml(io.BytesIO(data))
    assert restored.number_of_nodes() == 3
    assert restored.number_of_edges() == 2
    assert float(restored["0"]["1"]["weight"]) == 2.5
    assert restored["0"]["1"]["relation"] == "nearest"


def test_gml_export_is_nonempty_and_round_trippable():
    data = gml_bytes(sample_graph())
    assert data
    assert b"graph" in data.lower()

    restored = nx.parse_gml(data.decode("latin-1"))
    assert restored.number_of_nodes() == 3
    assert restored.number_of_edges() == 2


def test_edge_list_export_is_stable():
    data = edge_list_bytes(sample_graph()).decode("utf-8")
    assert data.splitlines() == ["0 1", "1 2"]


def test_directed_graphml_preserves_direction():
    data = graphml_bytes(sample_directed_graph())
    restored = nx.read_graphml(io.BytesIO(data))
    assert restored.is_directed()
    assert restored.number_of_edges() == 2
    assert float(restored["A"]["B"]["weight"]) == 3.0
    assert float(restored["B"]["A"]["weight"]) == 1.0
