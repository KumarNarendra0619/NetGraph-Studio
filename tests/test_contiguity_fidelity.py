"""Polygon contiguity fidelity tests against City2Graph."""

import geopandas as gpd
from shapely.geometry import Polygon

import city2graph.proximity as c2g
from netgraph.adapter import run_operation


def polygons():
    return gpd.GeoDataFrame(
        geometry=[
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(1, 0), (2, 0), (2, 1), (1, 1)]),
            Polygon([(3, 0), (4, 0), (4, 1), (3, 1)]),
        ],
        crs="EPSG:3857",
        index=[201, 202, 203],
    )


def test_queen_contiguity_fidelity():
    gdf = polygons()
    expected = c2g.contiguity_graph(gdf, contiguity="queen", as_nx=False)
    actual = run_operation(gdf, "contiguity", contiguity="queen")
    assert isinstance(actual, tuple) and len(actual) == 2
    gpd.testing.assert_geodataframe_equal(actual[0], expected[0], check_exact=True)
    gpd.testing.assert_geodataframe_equal(actual[1], expected[1], check_exact=True)


def test_rook_contiguity_fidelity():
    gdf = polygons()
    expected = c2g.contiguity_graph(gdf, contiguity="rook", as_nx=False)
    actual = run_operation(gdf, "contiguity", contiguity="rook")
    gpd.testing.assert_geodataframe_equal(actual[0], expected[0], check_exact=True)
    gpd.testing.assert_geodataframe_equal(actual[1], expected[1], check_exact=True)
