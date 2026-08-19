import geopandas as gpd
from geopandas.testing import assert_geodataframe_equal
from shapely.geometry import LineString, Point, Polygon

import city2graph.proximity as c2g
from netgraph.adapter import run_operation


def _polygons() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {"name": ["A", "B", "C", "D"]},
        geometry=[
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(1, 0), (2, 0), (2, 1), (1, 1)]),
            Polygon([(0, 1), (1, 1), (1, 2), (0, 2)]),
            Polygon([(1, 1), (2, 1), (2, 2), (1, 2)]),
        ],
        crs="EPSG:3857",
        index=[10, 20, 30, 40],
    )


def _network() -> gpd.GeoDataFrame:
    index = [(0, 1), (1, 2)]
    return gpd.GeoDataFrame(
        {"source_id": [0, 1], "target_id": [1, 2]},
        geometry=[LineString([(0, 0), (10, 0)]), LineString([(10, 0), (20, 0)])],
        crs="EPSG:3857",
        index=index,
    )


def _points() -> gpd.GeoDataFrame:
    return gpd.GeoDataFrame(
        {"name": ["A", "B", "C"]},
        geometry=[Point(0, 0), Point(10, 0), Point(20, 0)],
        crs="EPSG:3857",
        index=[0, 1, 2],
    )


def _assert_graph_equal(actual, expected) -> None:
    assert isinstance(actual, tuple) and len(actual) == 2
    assert isinstance(expected, tuple) and len(expected) == 2
    assert_geodataframe_equal(actual[0], expected[0], check_like=False)
    assert_geodataframe_equal(actual[1], expected[1], check_like=False)


def test_polygon_contiguity_queen_fidelity():
    gdf = _polygons()
    direct = c2g.contiguity_graph(gdf, contiguity="queen", distance_metric="euclidean", as_nx=False)
    wrapped = run_operation(gdf, "contiguity", contiguity="queen", distance_metric="euclidean")
    _assert_graph_equal(wrapped, direct)


def test_polygon_contiguity_rook_fidelity():
    gdf = _polygons()
    direct = c2g.contiguity_graph(gdf, contiguity="rook", distance_metric="euclidean", as_nx=False)
    wrapped = run_operation(gdf, "contiguity", contiguity="rook", distance_metric="euclidean")
    _assert_graph_equal(wrapped, direct)


def test_polygon_contiguity_preserves_node_ids():
    nodes, _ = run_operation(_polygons(), "contiguity", contiguity="queen")
    assert list(nodes.index) == [10, 20, 30, 40]


def test_network_distance_knn_fidelity():
    points = _points()
    network = _network()
    direct = c2g.knn_graph(
        points,
        k=1,
        distance_metric="network",
        network_gdf=network,
        network_weight=None,
        as_nx=False,
    )
    wrapped = run_operation(
        points,
        "knn",
        k=1,
        distance_metric="network",
        network_gdf=network,
    )
    _assert_graph_equal(wrapped, direct)


def test_network_distance_requires_nonempty_crs_network():
    points = _points()
    empty_network = gpd.GeoDataFrame(geometry=[], crs="EPSG:3857")
    try:
        run_operation(points, "knn", k=1, distance_metric="network", network_gdf=empty_network)
    except ValueError as exc:
        assert "network layer" in str(exc).lower()
    else:
        raise AssertionError("Expected network-layer validation error")
