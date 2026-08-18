"""NetGraph Studio Streamlit application."""

from __future__ import annotations

from datetime import datetime, timezone

import networkx as nx
import streamlit as st

from netgraph.adapter import OPERATIONS, run_operation
from netgraph.io import gdf_to_csv_bytes, gdf_to_geojson_bytes, read_vector, save_uploaded_file

st.set_page_config(page_title="NetGraph Studio", page_icon="🕸️", layout="wide")

st.title("🕸️ NetGraph Studio")
st.caption("A simple research workbench for City2Graph — no Python required.")

with st.sidebar:
    st.header("Workflow")
    mode = st.radio("Mode", ["Simple", "Research"], index=0)
    st.divider()
    st.markdown("**Scientific rule**")
    st.caption("NetGraph Studio calls the original City2Graph public API. The UI does not reimplement graph algorithms.")

st.subheader("1. Upload geospatial data")
uploaded = st.file_uploader(
    "Choose a vector layer",
    type=["geojson", "json", "gpkg", "parquet", "feather", "shp"],
    help="For the first release, use a single-file vector format such as GeoJSON, GeoPackage, or GeoParquet.",
)

if uploaded is None:
    st.info("Upload a geospatial layer to begin.")
    st.stop()

try:
    input_path = save_uploaded_file(uploaded)
    gdf = read_vector(input_path)
except Exception as exc:
    st.error(f"Could not read the input layer: {exc}")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Features", f"{len(gdf):,}")
c2.metric("Geometry", ", ".join(sorted(gdf.geometry.geom_type.unique())))
c3.metric("CRS", str(gdf.crs) if gdf.crs else "Missing")

st.subheader("2. Choose analysis")
operation_key = st.selectbox(
    "Graph method",
    options=list(OPERATIONS),
    format_func=lambda key: OPERATIONS[key].label,
)
operation = OPERATIONS[operation_key]
st.caption(operation.description)

params = {}
if operation_key == "knn":
    params["k"] = st.number_input("Number of neighbours (k)", min_value=1, value=5, step=1)
elif operation_key == "radius":
    params["radius"] = st.number_input("Maximum connection distance", min_value=0.000001, value=1000.0, step=100.0)
elif operation_key == "waxman":
    col1, col2 = st.columns(2)
    params["beta"] = col1.number_input("Beta", min_value=0.000001, max_value=1.0, value=0.2, step=0.05)
    params["r0"] = col2.number_input("r0", min_value=0.000001, value=1000.0, step=100.0)
    params["seed"] = st.number_input("Random seed", min_value=0, value=42, step=1)
elif operation_key == "contiguity":
    params["contiguity"] = st.selectbox("Contiguity rule", ["queen", "rook"])

if operation_key != "contiguity":
    params["distance_metric"] = st.selectbox("Distance metric", ["euclidean", "manhattan"], index=0)
else:
    params["distance_metric"] = st.selectbox("Distance metric", ["euclidean", "manhattan"], index=0)

run = st.button("🚀 Run City2Graph", type="primary", use_container_width=True)

if run:
    with st.spinner("Running the original City2Graph operation…"):
        started = datetime.now(timezone.utc)
        try:
            result = run_operation(gdf, operation_key, **params)
            elapsed = (datetime.now(timezone.utc) - started).total_seconds()
        except Exception as exc:
            st.error(f"City2Graph returned an error: {exc}")
            st.stop()

    st.success(f"Graph created successfully in {elapsed:.2f} seconds.")

    if isinstance(result, nx.Graph):
        graph = result
        nodes_gdf = None
        edges_gdf = None
    else:
        nodes_gdf, edges_gdf = result
        graph = nx.Graph()
        graph.add_nodes_from(nodes_gdf.index)
        graph.add_edges_from(edges_gdf.index.tolist())

    st.subheader("3. Results")
    a, b, c, d = st.columns(4)
    a.metric("Nodes", f"{graph.number_of_nodes():,}")
    b.metric("Edges", f"{graph.number_of_edges():,}")
    c.metric("Components", f"{nx.number_connected_components(graph.to_undirected()):,}")
    d.metric("Average degree", f"{sum(dict(graph.degree()).values()) / max(graph.number_of_nodes(), 1):.2f}")

    tab1, tab2, tab3 = st.tabs(["Map", "Graph data", "Research record"])

    with tab1:
        if nodes_gdf is not None and not nodes_gdf.empty:
            points = nodes_gdf.copy()
            points["geometry"] = points.geometry.centroid
            st.map(points, use_container_width=True)
        else:
            st.info("Map preview is unavailable for this result type.")

    with tab2:
        if nodes_gdf is not None:
            st.write("**Nodes**")
            st.dataframe(nodes_gdf.drop(columns="geometry", errors="ignore"), use_container_width=True)
            st.download_button("Download nodes GeoJSON", gdf_to_geojson_bytes(nodes_gdf), "nodes.geojson", "application/geo+json")
            st.download_button("Download nodes CSV", gdf_to_csv_bytes(nodes_gdf), "nodes.csv", "text/csv")
        if edges_gdf is not None:
            st.write("**Edges**")
            st.dataframe(edges_gdf.drop(columns="geometry", errors="ignore"), use_container_width=True)
            st.download_button("Download edges GeoJSON", gdf_to_geojson_bytes(edges_gdf), "edges.geojson", "application/geo+json")
            st.download_button("Download edges CSV", gdf_to_csv_bytes(edges_gdf), "edges.csv", "text/csv")

    with tab3:
        st.json(
            {
                "application": "NetGraph Studio",
                "mode": mode,
                "operation": operation.label,
                "operation_key": operation_key,
                "parameters": params,
                "input_features": len(gdf),
                "input_crs": str(gdf.crs),
                "nodes": graph.number_of_nodes(),
                "edges": graph.number_of_edges(),
                "processing_time_seconds": round(elapsed, 3),
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "algorithm_source": "Original City2Graph public API",
            }
        )
