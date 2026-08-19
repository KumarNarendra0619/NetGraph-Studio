"""Input validation and output-fidelity comparison utilities."""

from __future__ import annotations

import geopandas as gpd
import pandas as pd


def validate_layer(gdf: gpd.GeoDataFrame, *, allowed_geometry: set[str] | None = None) -> None:
    """Validate a layer before the City2Graph call; never modify the layer."""
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("Input must be a GeoDataFrame.")
    if gdf.empty:
        raise ValueError("The input layer contains no features.")
    if gdf.geometry.isna().any():
        raise ValueError("The input layer contains missing geometries.")
    if gdf.crs is None:
        raise ValueError("The input layer has no CRS.")
    if allowed_geometry and not set(gdf.geometry.geom_type).issubset(allowed_geometry):
        raise ValueError(f"Expected geometry types: {sorted(allowed_geometry)}")


def compare_geodataframes(actual: gpd.GeoDataFrame, expected: gpd.GeoDataFrame) -> dict:
    """Compare structural, CRS, attribute and geometry equality."""
    result = {
        "same_row_count": len(actual) == len(expected),
        "same_columns": list(actual.columns) == list(expected.columns),
        "same_crs": actual.crs == expected.crs,
        "same_index": actual.index.equals(expected.index),
        "same_geometry": False,
        "same_attributes": False,
    }
    try:
        gpd.testing.assert_geodataframe_equal(actual, expected, check_exact=True, check_like=False)
    except AssertionError:
        return result
    result["same_geometry"] = True
    result["same_attributes"] = True
    return result


def compare_result(actual, expected) -> dict:
    """Compare City2Graph-style (nodes, edges) results without recomputation."""
    if not (isinstance(actual, tuple) and isinstance(expected, tuple) and len(actual) == len(expected) == 2):
        return {"pass": actual == expected, "reason": "Non-tuple result comparison."}
    nodes = compare_geodataframes(actual[0], expected[0])
    edges = compare_geodataframes(actual[1], expected[1])
    return {"pass": all(nodes.values()) and all(edges.values()), "nodes": nodes, "edges": edges}
