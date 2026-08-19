"""Guard against accidentally moving graph construction into the adapter."""

from pathlib import Path


def test_adapter_delegates_to_city2graph():
    text = Path("netgraph/adapter.py").read_text(encoding="utf-8")
    for symbol in [
        "c2g.knn_graph",
        "c2g.delaunay_graph",
        "c2g.gabriel_graph",
        "c2g.relative_neighborhood_graph",
        "c2g.euclidean_minimum_spanning_tree",
        "c2g.fixed_radius_graph",
        "c2g.waxman_graph",
        "c2g.contiguity_graph",
    ]:
        assert symbol in text
