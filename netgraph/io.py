"""Input/output helpers for NetGraph Studio."""
from __future__ import annotations
import tempfile
from pathlib import Path
import zipfile
import geopandas as gpd

SUPPORTED_VECTOR_SUFFIXES = {".geojson", ".json", ".gpkg", ".parquet", ".feather", ".shp", ".zip"}


def save_uploaded_file(uploaded_file) -> Path:
    """Persist an uploaded vector file; ZIP may contain a complete Shapefile."""
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix not in SUPPORTED_VECTOR_SUFFIXES:
        raise ValueError("Unsupported file type. Use GeoJSON, GeoPackage, GeoParquet, Feather, Shapefile, or a zipped Shapefile.")
    if suffix == ".zip":
        root = Path(tempfile.mkdtemp(prefix="netgraph_"))
        archive = root / Path(uploaded_file.name).name
        archive.write_bytes(uploaded_file.getbuffer())
        with zipfile.ZipFile(archive) as zf:
            shp = next((n for n in zf.namelist() if n.lower().endswith(".shp") and not Path(n).name.startswith("__MACOSX")), None)
            if shp is None:
                raise ValueError("ZIP does not contain a Shapefile (.shp).")
            zf.extractall(root)
            return root / shp
    handle = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    handle.write(uploaded_file.getbuffer()); handle.close()
    return Path(handle.name)


def read_vector(path: Path) -> gpd.GeoDataFrame:
    """Read a supported vector dataset without changing CRS or geometry."""
    suffix = path.suffix.lower()
    if suffix == ".parquet": return gpd.read_parquet(path)
    if suffix == ".feather": return gpd.read_feather(path)
    return gpd.read_file(path)


def gdf_to_geojson_bytes(gdf: gpd.GeoDataFrame) -> bytes:
    return gdf.to_json().encode("utf-8")


def gdf_to_csv_bytes(gdf: gpd.GeoDataFrame) -> bytes:
    return gdf.drop(columns="geometry", errors="ignore").to_csv(index=True).encode("utf-8")
