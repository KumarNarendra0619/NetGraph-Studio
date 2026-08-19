"""Adapters for non-proximity City2Graph workflows.

No graph mathematics is implemented here. Every operation delegates directly
to a public City2Graph function so the upstream library remains the source of
scientific computation.
"""

from __future__ import annotations

from pathlib import Path
import inspect
import tempfile

import geopandas as gpd
import pandas as pd


def morphology_graph(buildings: gpd.GeoDataFrame, streets: gpd.GeoDataFrame, **kwargs):
    """Delegate urban morphology graph construction to City2Graph."""
    from city2graph.morphology import morphological_graph
    return morphological_graph(buildings, streets, **kwargs)


def od_graph(od_data: pd.DataFrame, zones: gpd.GeoDataFrame, **kwargs):
    """Delegate OD/mobility graph construction to City2Graph."""
    from city2graph.mobility import od_matrix_to_graph
    return od_matrix_to_graph(od_data, zones, **kwargs)


def gtfs_graph(gtfs_zip: bytes, **kwargs):
    """Delegate GTFS loading to City2Graph transportation APIs."""
    from city2graph.transportation import load_gtfs
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as handle:
        handle.write(gtfs_zip)
        path = Path(handle.name)
    try:
        return load_gtfs(path, **kwargs)
    finally:
        path.unlink(missing_ok=True)


def pyg_export(nodes, edges=None, **kwargs):
    """Delegate GeoDataFrame-to-PyG conversion to City2Graph."""
    from city2graph.graph import gdf_to_pyg
    return gdf_to_pyg(nodes, edges, **kwargs)


def available_city2graph_apis() -> dict[str, list[str]]:
    """Return discoverable public APIs without executing them."""
    import city2graph.mobility as mobility
    import city2graph.morphology as morphology
    import city2graph.transportation as transportation

    modules = {"morphology": morphology, "mobility": mobility, "transportation": transportation}
    result: dict[str, list[str]] = {}
    for name, module in modules.items():
        names = getattr(module, "__all__", [])
        result[name] = sorted(
            n for n in names
            if callable(getattr(module, n, None)) and not n.startswith("_")
        )
    return result


def signature(name: str):
    """Return a City2Graph public API signature for UI/documentation generation."""
    import city2graph
    fn = getattr(city2graph, name, None)
    if fn is None:
        raise ValueError(f"City2Graph public API not found: {name}")
    return inspect.signature(fn)
