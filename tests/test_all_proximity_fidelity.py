"""Fidelity smoke/regression tests for all point-based proximity operations.

These tests intentionally compare the adapter output with the original public
City2Graph functions. NetGraph Studio must not reimplement graph construction.
"""

import geopandas as gpd
import pytest
from geopandas.testing import assert_geodataframe_equal
from shapely.geometry import Point

import city2graph.proximity as c2g
from netgraph.adapter import run_operation


def sample_points():
    return gpd.GeoDataFrame(
        {"name": list("ABCDE")},
        geometry=[Point(0, 0), Point(10, 0), Point(0, 10), Point(10, 10), Point(5, 5)],
        crs="EPSG:3857",
        index=[101, 102, 103, 104, 105],
    )


def assert_equal(actual, expected):
    assert isinstance(actual, tuple) and len(actual) == 2
    assert isinstance(expected, tuple) and len(expected) == 2
    assert_geodataframe_equal(actual[0], expected[0], check_exact=True)
    assert_geodataframe_equal(actual[1], expected[1], check_exact=True)


def test_delaunay_fidelity():
    gdf = sample_points()
    expected = c2g.delaunay_graph(gdf, distance_metric="euclidean", as_nx=False)
    actual = run_operation(gdf, "delaunay")
    assert_equal(actual, expected)


def test_gabriel_fidelity():
    gdf = sample_points()
    expected = c2g.gabriel_graph(gdf, distance_metric="euclidean", as_nx=False)
    actual = run_operation(gdf, "gabriel")
    assert_equal(actual, expected)


def test_rng_fidelity():
    gdf = sample_points()
    expected = c2g.relative_neighborhood_graph(gdf, distance_metric="euclidean", as_nx=False)
    actual = run_operation(gdf, "rng")
    assert_equal(actual, expected)


def test_mst_fidelity():
    gdf = sample_points()
    expected = c2g.euclidean_minimum_spanning_tree(gdf, distance_metric="euclidean", as_nx=False)
    actual = run_operation(gdf, "mst")
    assert_equal(actual, expected)


def test_radius_fidelity():
    gdf = sample_points()
    expected = c2g.fixed_radius_graph(gdf, radius=8, distance_metric="euclidean", as_nx=False)
    actual = run_operation(gdf, "radius", radius=8)
    assert_equal(actual, expected)


def test_waxman_fidelity():
    gdf = sample_points()
    expected = c2g.waxman_graph(gdf, beta=0.2, r0=1000, seed=42, distance_metric="euclidean", as_nx=False)
    actual = run_operation(gdf, "waxman", beta=0.2, r0=1000, seed=42)
    assert_equal(actual, expected)


@pytest.mark.parametrize("operation", ["delaunay", "gabriel", "rng", "mst", "radius", "waxman"])
def test_point_operations_preserve_node_ids(operation):
    nodes, _ = run_operation(sample_points(), operation, radius=8)
    assert list(nodes.index) == [101, 102, 103, 104, 105]
