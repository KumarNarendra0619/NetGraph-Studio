"""Thin adapter over the original City2Graph public API.

The adapter contains UI validation and parameter translation only. Graph construction
is delegated directly to the original City2Graph functions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import geopandas as gpd
import city2graph.proximity as c2g


@dataclass(frozen=True)
class Operation:
    key: str
    label: str
    description: str
    function: Callable
    geometry: str
    parameter: str | None = None


OPERATIONS: dict[str, Operation] = {
    "knn": Operation("knn", "K-Nearest Neighbours (KNN)", "Connect each node to its k nearest neighbours.", c2g.knn_graph, "point", "k"),
    "delaunay": Operation("delaunay", "Delaunay", "Build a Delaunay triangulation graph.", c2g.delaunay_graph, "point"),
    "gabriel": Operation("gabriel", "Gabriel", "Build a Gabriel proximity graph.", c2g.gabriel_graph, "point"),
    "rng": Operation("rng", "Relative Neighbourhood", "Build a relative-neighbourhood graph.", c2g.relative_neighborhood_graph, "point"),
    "mst": Operation("mst", "Minimum Spanning Tree", "Build a minimum-weight spanning tree.", c2g.euclidean_minimum_spanning_tree, "point"),
    "radius": Operation("radius", "Fixed Radius", "Connect nodes within a specified distance.", c2g.fixed_radius_graph, "point", "radius"),
    "waxman": Operation("waxman", "Waxman", "Build a probabilistic Waxman graph.", c2g.waxman_graph, "point", "beta"),
    "contiguity": Operation("contiguity", "Polygon Contiguity", "Build Queen or Rook adjacency from polygons.", c2g.contiguity_graph, "polygon"),
}


def validate_input(gdf: gpd.GeoDataFrame, operation: Operation) -> None:
    """Perform UI-level validation only; City2Graph remains the computational authority."""
    if gdf.empty:
        raise ValueError("The uploaded layer contains no features.")
    if gdf.geometry.isna().any():
        raise ValueError("The uploaded layer contains missing geometries.")
    if gdf.crs is None:
        raise ValueError("The input layer has no CRS. Define a CRS before running the analysis.")
    if operation.geometry == "point":
        allowed = {"Point", "MultiPoint"}
        if not set(gdf.geometry.geom_type).issubset(allowed):
            raise ValueError("This operation requires point geometries.")
    if operation.geometry == "polygon":
        allowed = {"Polygon", "MultiPolygon"}
        if not set(gdf.geometry.geom_type).issubset(allowed):
            raise ValueError("Polygon Contiguity requires polygon geometries.")


def run_operation(
    gdf: gpd.GeoDataFrame,
    operation_key: str,
    *,
    k: int = 5,
    radius: float = 1000.0,
    beta: float = 0.2,
    r0: float = 1000.0,
    seed: int | None = 42,
    contiguity: str = "queen",
    distance_metric: str = "euclidean",
    network_gdf: gpd.GeoDataFrame | None = None,
    network_weight: str | None = None,
):
    """Call the selected original City2Graph public function without reimplementing it."""
    if operation_key not in OPERATIONS:
        raise ValueError(f"Unknown graph operation: {operation_key}")

    operation = OPERATIONS[operation_key]
    validate_input(gdf, operation)

    if distance_metric not in {"euclidean", "manhattan", "network"}:
        raise ValueError("Unsupported distance metric.")
    if distance_metric == "network":
        if network_gdf is None:
            raise ValueError("Network distance requires a network layer.")
        if network_gdf.empty or network_gdf.crs is None:
            raise ValueError("The network layer must contain features and have a CRS.")

    common = {
        "distance_metric": distance_metric,
        "network_gdf": network_gdf,
        "network_weight": network_weight,
        "as_nx": False,
    }

    if operation_key == "knn":
        return operation.function(gdf, k=k, **common)
    if operation_key == "radius":
        return operation.function(gdf, radius=radius, **common)
    if operation_key == "waxman":
        return operation.function(gdf, beta=beta, r0=r0, seed=seed, **common)
    if operation_key == "contiguity":
        return operation.function(gdf, contiguity=contiguity, **common)
    return operation.function(gdf, **common)
