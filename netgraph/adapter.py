"""Thin adapter over the original City2Graph public API.

UI validation and parameter translation live here; graph construction remains
entirely delegated to City2Graph.
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


OPERATIONS: dict[str, Operation] = {
    "knn": Operation("knn", "K-Nearest Neighbours (KNN)", "Connect each node to its k nearest neighbours.", c2g.knn_graph, "point"),
    "delaunay": Operation("delaunay", "Delaunay", "Build a Delaunay triangulation graph.", c2g.delaunay_graph, "point"),
    "gabriel": Operation("gabriel", "Gabriel", "Build a Gabriel proximity graph.", c2g.gabriel_graph, "point"),
    "rng": Operation("rng", "Relative Neighbourhood", "Build a relative-neighbourhood graph.", c2g.relative_neighborhood_graph, "point"),
    "mst": Operation("mst", "Minimum Spanning Tree", "Build a minimum-weight spanning tree.", c2g.euclidean_minimum_spanning_tree, "point"),
    "radius": Operation("radius", "Fixed Radius", "Connect nodes within a specified distance.", c2g.fixed_radius_graph, "point"),
    "waxman": Operation("waxman", "Waxman", "Build a probabilistic Waxman graph.", c2g.waxman_graph, "point"),
    "contiguity": Operation("contiguity", "Polygon Contiguity", "Build Queen or Rook adjacency from polygons.", c2g.contiguity_graph, "polygon"),
}


def validate_input(gdf: gpd.GeoDataFrame, operation: Operation) -> None:
    if gdf.empty:
        raise ValueError("The uploaded layer contains no features.")
    if gdf.geometry.isna().any():
        raise ValueError("The uploaded layer contains missing geometries.")
    if gdf.crs is None:
        raise ValueError("The input layer has no CRS. Define a CRS before analysis.")
    if operation.geometry == "point" and not set(gdf.geometry.geom_type).issubset({"Point", "MultiPoint"}):
        raise ValueError("This operation requires point geometries.")
    if operation.geometry == "polygon" and not set(gdf.geometry.geom_type).issubset({"Polygon", "MultiPolygon"}):
        raise ValueError("Polygon Contiguity requires polygon geometries.")


def _distance_kwargs(distance_metric: str, network_gdf: gpd.GeoDataFrame | None, network_weight: str | None) -> dict:
    if distance_metric not in {"euclidean", "manhattan", "network"}:
        raise ValueError("Unsupported distance metric.")
    if distance_metric == "network":
        if network_gdf is None or network_gdf.empty or network_gdf.crs is None:
            raise ValueError("Network distance requires a non-empty network layer with a CRS.")
        return {"distance_metric": distance_metric, "network_gdf": network_gdf, "network_weight": network_weight}
    return {"distance_metric": distance_metric}


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
    if operation_key not in OPERATIONS:
        raise ValueError(f"Unknown graph operation: {operation_key}")

    operation = OPERATIONS[operation_key]
    validate_input(gdf, operation)

    if operation_key == "contiguity":
        if contiguity not in {"queen", "rook"}:
            raise ValueError("Contiguity must be queen or rook.")
        # City2Graph contiguity does not use proximity distance arguments.
        return operation.function(gdf, contiguity=contiguity, as_nx=False)

    distance_kwargs = _distance_kwargs(distance_metric, network_gdf, network_weight)

    if operation_key == "knn":
        if k < 1:
            raise ValueError("k must be at least 1.")
        return operation.function(gdf, k=k, **distance_kwargs, as_nx=False)
    if operation_key == "radius":
        if radius <= 0:
            raise ValueError("radius must be greater than 0.")
        return operation.function(gdf, radius=radius, **distance_kwargs, as_nx=False)
    if operation_key == "waxman":
        if not 0 < beta <= 1:
            raise ValueError("beta must be between 0 and 1.")
        if r0 <= 0:
            raise ValueError("r0 must be greater than 0.")
        return operation.function(gdf, beta=beta, r0=r0, seed=seed, **distance_kwargs, as_nx=False)
    return operation.function(gdf, **distance_kwargs, as_nx=False)
