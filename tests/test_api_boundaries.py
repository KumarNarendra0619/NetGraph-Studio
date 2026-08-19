"""Smoke tests for City2Graph integration boundaries.

The tests only inspect public APIs and adapter signatures; they do not
reimplement any City2Graph graph algorithm.
"""

import inspect

import city2graph as c2g

from netgraph.advanced import gtfs_graph, morphology_graph, od_graph, pyg_export


def test_public_city2graph_boundaries_exist():
    for name in (
        "morphological_graph",
        "od_matrix_to_graph",
        "load_gtfs",
        "travel_summary_graph",
        "gdf_to_pyg",
    ):
        assert callable(getattr(c2g, name, None)), name


def test_adapter_signatures_expose_required_inputs():
    assert "center_point" in inspect.signature(morphology_graph).parameters
    assert "od_data" in inspect.signature(od_graph).parameters
    assert "gtfs_zip" in inspect.signature(gtfs_graph).parameters
    assert "nodes" in inspect.signature(pyg_export).parameters


def test_od_api_supports_expected_controls():
    sig = inspect.signature(c2g.od_matrix_to_graph)
    for name in (
        "zone_id_col",
        "matrix_type",
        "source_col",
        "target_col",
        "weight_cols",
        "directed",
        "as_nx",
    ):
        assert name in sig.parameters


def test_pyg_api_supports_gdf_conversion():
    sig = inspect.signature(c2g.gdf_to_pyg)
    assert "nodes" in sig.parameters
    assert "edges" in sig.parameters
