"""Input/output helpers for NetGraph Studio."""

from __future__ import annotations

import tempfile
from pathlib import Path

import geopandas as gpd

SUPPORTED_VECTOR_SUFFIXES = {".geojson", ".json", ".gpkg", ".parquet", ".feather", ".shp"}


def save_uploaded_file(uploaded_file) -> Path:
    """Persist a Streamlit UploadedFile to a temporary path."""
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix not in SUPPORTED_VECTOR_SUFFIXES:
        raise ValueError(
            "Unsupported file type. Use GeoJSON, GeoPackage, GeoParquet, Feather, or Shapefile."
        )
    handle = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    handle.write(uploaded_file.getbuffer())
    handle.close()
    return Path(handle.name)


def read_vector(path: Path) -> gpd.GeoDataFrame:
    """Read a supported vector dataset without changing its CRS or geometry."""
    suffix = path.suffix.lower()
    if suffix in {".parquet", ".feather"}:
        return gpd.read_parquet(path) if suffix == ".parquet" else gpd.read_feather(path)
    return gpd.read_file(path)


def gdf_to_geojson_bytes(gdf: gpd.GeoDataFrame) -> bytes:
    """Serialize a GeoDataFrame to UTF-8 GeoJSON."""
    return gdf.to_json().encode("utf-8")


def gdf_to_csv_bytes(gdf: gpd.GeoDataFrame) -> bytes:
    """Serialize non-geometry attributes to CSV."""
    return gdf.drop(columns="geometry", errors="ignore").to_csv(index=True).encode("utf-8")
