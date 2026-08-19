import geopandas as gpd
from geopandas.testing import assert_geodataframe_equal
from shapely.geometry import Point

import city2graph.proximity as c2g
from netgraph.adapter import run_operation


def _sample_points() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {"name": ["A", "B", "C", "D"]},
        geometry=[Point(0, 0), Point(10, 0), Point(0, 10), Point(10, 10)],
        crs="EPSG:3857",
        index=[101, 102, 103, 104],
    )


def _assert_graph_outputs_equal(actual, expected) -> None:
    assert isinstance(actual, tuple) and len(actual) == 2
    assert isinstance(expected, tuple) and len(expected) == 2

    actual_nodes, actual_edges = actual
    expected_nodes, expected_edges = expected

    assert_geodataframe_equal(
        actual_nodes,
        expected_nodes,
        check_like=False,
        check_exact=True,
    )
    assert_geodataframe_equal(
        actual_edges,
        expected_edges,
        check_like=False,
        check_exact=True,
    )


def test_knn_netgraph_matches_direct_city2graph():
    gdf = _sample_points()
    kwargs = {
        "k": 2,
        "distance_metric": "euclidean",
        "network_gdf": None,
        "network_weight": None,
        "as_nx": False,
    }

    direct = c2g.knn_graph(gdf, **kwargs)
    through_netgraph = run_operation(
        gdf,
        "knn",
        k=2,
        distance_metric="euclidean",
    )

    _assert_graph_outputs_equal(through_netgraph, direct)


def test_knn_preserves_input_node_ids():
    nodes, _ = run_operation(_sample_points(), "knn", k=2)
    assert list(nodes.index) == [101, 102, 103, 104]


def test_invalid_network_metric_is_rejected_before_engine_call():
    gdf = _sample_points()
    try:
        run_operation(gdf, "knn", k=2, distance_metric="network")
    except ValueError as exc:
        assert "Network distance requires a network layer" in str(exc)
    else:
        raise AssertionError("Expected network-distance validation error")
