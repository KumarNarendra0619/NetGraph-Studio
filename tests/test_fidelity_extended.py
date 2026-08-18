import geopandas as gpd
import pytest
from shapely.geometry import Point

import city2graph.proximity as c2g
from netgraph.adapter import run_operation


def _sample_points() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {"name": ["A", "B", "C", "D", "E"]},
        geometry=[Point(0, 0), Point(10, 0), Point(0, 10), Point(10, 10), Point(5, 5)],
        crs="EPSG:3857",
        index=[101, 102, 103, 104, 105],
    )


def _assert_graph_outputs_equal(actual, expected) -> None:
    assert isinstance(actual, tuple) and len(actual) == 2
    assert isinstance(expected, tuple) and len(expected) == 2
    actual_nodes, actual_edges = actual
    expected_nodes, expected_edges = expected
    gpd.testing.assert_geodataframe_equal(actual_nodes, expected_nodes, check_like=False, check_exact=True)
    gpd.testing.assert_geodataframe_equal(actual_edges, expected_edges, check_like=False, check_exact=True)


@pytest.mark.parametrize(
    "operation_key, function_name, kwargs",
    [
        ("delaunay", "delaunay_graph", {}),
        ("gabriel", "gabriel_graph", {}),
        ("rng", "relative_neighborhood_graph", {}),
        ("mst", "euclidean_minimum_spanning_tree", {}),
        ("radius", "fixed_radius_graph", {"radius": 8.0}),
        ("waxman", "waxman_graph", {"beta": 0.2, "r0": 20.0, "seed": 42}),
    ],
)
def test_point_operations_match_direct_city2graph(operation_key, function_name, kwargs):
    gdf = _sample_points()
    common = {
        "distance_metric": "euclidean",
        "network_gdf": None,
        "network_weight": None,
        "as_nx": False,
    }
    direct = getattr(c2g, function_name)(gdf, **common, **kwargs)
    through_netgraph = run_operation(gdf, operation_key, distance_metric="euclidean", **kwargs)
    _assert_graph_outputs_equal(through_netgraph, direct)


def test_knn_manhattan_matches_direct_city2graph():
    gdf = _sample_points()
    direct = c2g.knn_graph(
        gdf, k=2, distance_metric="manhattan", network_gdf=None, network_weight=None, as_nx=False
    )
    through_netgraph = run_operation(gdf, "knn", k=2, distance_metric="manhattan")
    _assert_graph_outputs_equal(through_netgraph, direct)


def test_network_distance_requires_network_layer():
    with pytest.raises(ValueError, match="Network distance requires a network layer"):
        run_operation(_sample_points(), "knn", k=2, distance_metric="network")
