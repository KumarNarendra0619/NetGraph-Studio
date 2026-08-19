"""Input/parameter validation regression tests."""

import geopandas as gpd
import pytest
from shapely.geometry import Point, Polygon

from netgraph.adapter import run_operation


def points():
    return gpd.GeoDataFrame(geometry=[Point(0, 0), Point(1, 1)], crs="EPSG:3857")


def polygons():
    return gpd.GeoDataFrame(
        geometry=[Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])],
        crs="EPSG:3857",
    )


def test_unknown_operation_rejected():
    with pytest.raises(ValueError, match="Unknown graph operation"):
        run_operation(points(), "unknown")


def test_knn_rejects_zero_k():
    with pytest.raises(ValueError, match="k must be at least 1"):
        run_operation(points(), "knn", k=0)


def test_radius_rejects_nonpositive_value():
    with pytest.raises(ValueError, match="radius must be greater than 0"):
        run_operation(points(), "radius", radius=0)


def test_waxman_rejects_invalid_beta():
    with pytest.raises(ValueError, match="beta must be between 0 and 1"):
        run_operation(points(), "waxman", beta=0)


def test_contiguity_rejects_point_layer():
    with pytest.raises(ValueError, match="Polygon Contiguity requires polygon geometries"):
        run_operation(points(), "contiguity")


def test_proximity_rejects_polygon_layer():
    with pytest.raises(ValueError, match="requires point geometries"):
        run_operation(polygons(), "knn")


def test_contiguity_rejects_invalid_rule():
    with pytest.raises(ValueError, match="Contiguity must be queen or rook"):
        run_operation(polygons(), "contiguity", contiguity="invalid")
