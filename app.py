"""NetGraph Studio — non-coder City2Graph research workbench."""
from __future__ import annotations
from datetime import datetime, timezone
import geopandas as gpd
import networkx as nx
import pandas as pd
import streamlit as st
from shapely.geometry import Point
from netgraph.adapter import OPERATIONS, run_operation
from netgraph.advanced import morphology_graph, od_graph, gtfs_graph
from netgraph.export import graphml_bytes, gml_bytes, edge_list_bytes
from netgraph.io import gdf_to_csv_bytes, gdf_to_geojson_bytes, read_vector, save_uploaded_file
from netgraph.report import build_record, json_bytes

st.set_page_config(page_title="NetGraph Studio", page_icon="🕸️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
/* NetGraph Studio: compact desktop tool styling. No scientific computation is changed. */
.block-container { max-width: 1450px; padding-top: 1.2rem; padding-bottom: 2rem; }
[data-testid="stSidebar"] { border-right: 1px solid rgba(128,128,128,.18); }
[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }
.ng-header { display:flex; align-items:center; justify-content:space-between; gap:20px; padding:14px 18px; border:1px solid rgba(128,128,128,.20); border-radius:12px; margin-bottom:14px; background:rgba(128,128,128,.045); }
.ng-brand { font-size:1.45rem; font-weight:750; letter-spacing:-.02em; }
.ng-sub { color:rgba(128,128,128,.95); font-size:.88rem; margin-top:2px; }
.ng-badge { border:1px solid rgba(128,128,128,.25); border-radius:999px; padding:5px 10px; font-size:.75rem; white-space:nowrap; }
.ng-section { font-size:.95rem; font-weight:700; margin:8px 0 8px; }
.ng-help { color:rgba(128,128,128,.9); font-size:.82rem; margin:0 0 10px; }
div[data-testid="stMetric"] { padding:10px 12px; border:1px solid rgba(128,128,128,.18); border-radius:10px; }
.stButton > button { border-radius:8px; font-weight:650; }
[data-testid="stFileUploader"] { border:1px dashed rgba(128,128,128,.38); border-radius:10px; padding:4px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ng-header">
  <div>
    <div class="ng-brand">🕸️ NetGraph Studio</div>
    <div class="ng-sub">No-code spatial network analysis powered by City2Graph</div>
  </div>
  <div class="ng-badge">City2Graph 1.0.0 • Research-ready</div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Workspace")
    mode = st.radio("Working mode", ["Simple", "Research"], horizontal=True, label_visibility="collapsed")
    workflow = st.selectbox(
        "Tool",
        ["Proximity / Contiguity", "Urban Morphology", "Mobility / OD", "Transportation / GTFS", "GNN Export"],
        help="Choose the type of graph workflow you want to run."
    )
    st.divider()
    st.markdown("**Workflow**")
    st.caption("1. Upload data  •  2. Choose method  •  3. Set parameters  •  4. Run  •  5. Export")
    st.divider()
    st.caption("Scientific engine: original City2Graph API. NetGraph Studio provides validation, controls, visualization and export.")


def load_layer(label: str, key: str):
    uploaded = st.file_uploader(label, type=["geojson", "json", "gpkg", "parquet", "feather", "shp"], key=key)
    if uploaded is None:
        return None
    try:
        gdf = read_vector(save_uploaded_file(uploaded))
        st.success(f"Loaded {len(gdf):,} features  |  CRS: {gdf.crs}")
        return gdf
    except Exception as exc:
        st.error(f"Could not read the layer: {exc}")
        return None


def show_result(result, *, operation: str, params: dict, input_features: int, input_crs: str | None, elapsed: float):
    directed = bool(params.get("directed", False))
    if isinstance(result, tuple) and len(result) == 2 and hasattr(result[0], "geometry"):
        nodes_gdf, edges_gdf = result
        graph = nx.DiGraph() if directed else nx.Graph()
        graph.add_nodes_from(nodes_gdf.index)
        if isinstance(edges_gdf.index, pd.MultiIndex):
            graph.add_edges_from([(x[0], x[1]) for x in edges_gdf.index])
    elif isinstance(result, tuple) and len(result) == 2 and isinstance(result[0], dict):
        nodes_gdf, edges_gdf = result
        graph = nx.Graph()
        for layer in nodes_gdf.values():
            graph.add_nodes_from(layer.index)
        for layer in edges_gdf.values():
            if isinstance(layer.index, pd.MultiIndex):
                graph.add_edges_from([(x[0], x[1]) for x in layer.index])
    elif isinstance(result, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
        graph, nodes_gdf, edges_gdf = result, None, None
    else:
        st.write(result)
        return

    a, b, c, d = st.columns(4)
    a.metric("Nodes", f"{graph.number_of_nodes():,}")
    b.metric("Edges", f"{graph.number_of_edges():,}")
    try:
        components = nx.number_connected_components(graph.to_undirected())
    except Exception:
        components = "—"
    c.metric("Components", str(components))
    d.metric("Average degree", f"{sum(dict(graph.degree()).values()) / max(graph.number_of_nodes(), 1):.2f}")

    tab_map, tab_data, tab_export, tab_record = st.tabs(["Map", "Data", "Export", "Research record"])
    with tab_map:
        if nodes_gdf is not None and not isinstance(nodes_gdf, dict) and not nodes_gdf.empty:
            preview = nodes_gdf.copy()
            if not all(preview.geometry.geom_type.isin(["Point", "MultiPoint"])):
                preview["geometry"] = preview.geometry.centroid
            if preview.crs is not None and preview.crs.to_epsg() != 4326:
                preview = preview.to_crs(4326)
            st.map(preview, use_container_width=True)
        else:
            st.info("This workflow returns heterogeneous layers. Use Data and Export to inspect the complete result.")
    with tab_data:
        if isinstance(nodes_gdf, dict):
            for name, layer in nodes_gdf.items():
                st.write(f"**Nodes — {name}**")
                st.dataframe(layer.drop(columns="geometry", errors="ignore"), use_container_width=True)
        elif nodes_gdf is not None:
            st.dataframe(nodes_gdf.drop(columns="geometry", errors="ignore"), use_container_width=True)
            st.download_button("Download nodes GeoJSON", gdf_to_geojson_bytes(nodes_gdf), "nodes.geojson", "application/geo+json")
            st.download_button("Download nodes CSV", gdf_to_csv_bytes(nodes_gdf), "nodes.csv", "text/csv")
        if isinstance(edges_gdf, dict):
            for name, layer in edges_gdf.items():
                st.write(f"**Edges — {name}**")
                st.dataframe(layer.drop(columns="geometry", errors="ignore"), use_container_width=True)
        elif edges_gdf is not None:
            st.dataframe(edges_gdf.drop(columns="geometry", errors="ignore"), use_container_width=True)
            st.download_button("Download edges GeoJSON", gdf_to_geojson_bytes(edges_gdf), "edges.geojson", "application/geo+json")
            st.download_button("Download edges CSV", gdf_to_csv_bytes(edges_gdf), "edges.csv", "text/csv")
    with tab_export:
        st.download_button("Download GraphML", graphml_bytes(graph), "netgraph.graphml", "application/xml")
        st.download_button("Download GML", gml_bytes(graph), "netgraph.gml", "text/plain")
        st.download_button("Download edge list", edge_list_bytes(graph), "edges.txt", "text/plain")
    record = build_record(operation=operation, mode=mode, parameters=params, input_features=input_features, input_crs=input_crs, nodes=graph.number_of_nodes(), edges=graph.number_of_edges(), processing_seconds=elapsed)
    with tab_record:
        st.json(record)
        st.download_button("Download reproducibility JSON", json_bytes(record), "netgraph_analysis.json", "application/json")


if workflow == "Proximity / Contiguity":
    st.markdown("### Proximity & Contiguity")
    st.markdown('<p class="ng-help">Create spatial graphs from point or polygon layers using City2Graph methods.</p>', unsafe_allow_html=True)
    gdf = load_layer("Upload spatial layer", "main_layer")
    if gdf is not None:
        st.markdown('<div class="ng-section">1 · Choose graph method</div>', unsafe_allow_html=True)
        operation_key = st.selectbox("Graph method", list(OPERATIONS), format_func=lambda x: OPERATIONS[x].label)
        operation = OPERATIONS[operation_key]
        params = {}
        if operation_key == "knn":
            params["k"] = st.number_input("Number of neighbours (k)", 1, 100, 5, help="Each feature connects to its k nearest neighbours.")
        elif operation_key == "radius":
            params["radius"] = st.number_input("Maximum connection distance", min_value=0.000001, value=1000.0)
        elif operation_key == "waxman":
            c1, c2 = st.columns(2)
            params["beta"] = c1.number_input("Beta", min_value=0.000001, max_value=1.0, value=0.2)
            params["r0"] = c2.number_input("r0", min_value=0.000001, value=1000.0)
            params["seed"] = st.number_input("Random seed", min_value=0, value=42)
        elif operation_key == "contiguity":
            params["contiguity"] = st.selectbox("Contiguity rule", ["queen", "rook"])
        if operation_key != "contiguity":
            st.markdown('<div class="ng-section">2 · Distance settings</div>', unsafe_allow_html=True)
            params["distance_metric"] = st.selectbox("Distance metric", ["euclidean", "manhattan", "network"])
            params["network_gdf"] = None
            params["network_weight"] = None
            if params["distance_metric"] == "network":
                network = load_layer("Upload network layer", "network_layer")
                if network is None:
                    st.stop()
                params["network_gdf"] = network
                fields = ["<geometry length>"] + [c for c in network.columns if c != network.geometry.name and network[c].dtype.kind in "biufc"]
                choice = st.selectbox("Network weight field", fields)
                params["network_weight"] = None if choice == "<geometry length>" else choice
        st.markdown('<div class="ng-section">3 · Run</div>', unsafe_allow_html=True)
        if st.button("▶ Run City2Graph", type="primary", use_container_width=True):
            started = datetime.now(timezone.utc)
            try:
                result = run_operation(gdf, operation_key, **params)
                elapsed = (datetime.now(timezone.utc) - started).total_seconds()
                safe = {k: "<GeoDataFrame>" if k == "network_gdf" else v for k, v in params.items()}
                show_result(result, operation=operation.label, params=safe, input_features=len(gdf), input_crs=str(gdf.crs), elapsed=elapsed)
            except Exception as exc:
                st.error(f"City2Graph returned an error: {exc}")

elif workflow == "Urban Morphology":
    st.markdown("### Urban Morphology")
    st.markdown('<p class="ng-help">Build the heterogeneous place–movement graph from buildings and street segments.</p>', unsafe_allow_html=True)
    buildings = load_layer("Upload building polygons", "buildings")
    streets = load_layer("Upload street / movement segments", "streets")
    if buildings is not None and streets is not None:
        st.markdown('<div class="ng-section">Analysis centre</div>', unsafe_allow_html=True)
        if buildings.crs is None:
            st.error("Buildings layer must have a CRS before morphology analysis.")
            st.stop()
        bounds = buildings.total_bounds
        c1, c2 = st.columns(2)
        cx = c1.number_input("Centre X", value=float((bounds[0] + bounds[2]) / 2), format="%.6f")
        cy = c2.number_input("Centre Y", value=float((bounds[1] + bounds[3]) / 2), format="%.6f")
        center_point = gpd.GeoSeries([Point(cx, cy)], crs=buildings.crs)
        params = {
            "contiguity": st.selectbox("Place contiguity", ["queen", "rook"]),
            "distance": st.number_input("Analysis distance", min_value=0.000001, value=500.0),
            "clipping_buffer": st.number_input("Clipping buffer", min_value=0.0, value=300.0),
            "keep_buildings": st.checkbox("Keep building geometries", True),
        }
        if st.button("▶ Build Morphological Graph", type="primary", use_container_width=True):
            started = datetime.now(timezone.utc)
            try:
                result = morphology_graph(buildings, streets, center_point, **params)
                elapsed = (datetime.now(timezone.utc) - started).total_seconds()
                show_result(result, operation="Morphological graph", params={**params, "center_point": f"({cx}, {cy})"}, input_features=len(buildings), input_crs=str(buildings.crs), elapsed=elapsed)
            except Exception as exc:
                st.error(f"City2Graph morphology returned an error: {exc}")

elif workflow == "Mobility / OD":
    st.markdown("### Mobility / OD")
    st.markdown('<p class="ng-help">Convert an origin–destination table into a spatial mobility graph.</p>', unsafe_allow_html=True)
    zones = load_layer("Upload zone layer", "zones")
    od_file = st.file_uploader("Upload OD CSV", type=["csv"], key="od_csv")
    if zones is not None and od_file is not None:
        od = pd.read_csv(od_file)
        matrix_type = st.selectbox("OD format", ["edgelist", "adjacency"])
        zone_id_col = st.selectbox("Zone ID column", list(zones.columns))
        directed = st.checkbox("Directed graph", True)
        params = {"zone_id_col": zone_id_col, "matrix_type": matrix_type, "as_nx": False, "directed": directed, "include_self_loops": st.checkbox("Keep self-loops", False), "compute_edge_geometry": st.checkbox("Create edge geometry", True)}
        if matrix_type == "edgelist":
            source_col = st.selectbox("Origin column", list(od.columns))
            target_col = st.selectbox("Destination column", list(od.columns), index=min(1, len(od.columns)-1))
            numeric = list(od.select_dtypes(include="number").columns)
            if not numeric:
                st.error("OD edge list needs a numeric weight column.")
                st.stop()
            weight_col = st.selectbox("Flow / weight column", numeric)
            params.update(source_col=source_col, target_col=target_col, weight_cols=[weight_col])
            params["threshold"] = st.number_input("Minimum flow threshold", min_value=0.0, value=0.0)
            params["threshold_col"] = weight_col if params["threshold"] > 0 else None
        if st.button("▶ Build OD Graph", type="primary", use_container_width=True):
            started = datetime.now(timezone.utc)
            try:
                result = od_graph(od, zones, **params)
                elapsed = (datetime.now(timezone.utc) - started).total_seconds()
                show_result(result, operation="OD / Mobility graph", params=params, input_features=len(zones), input_crs=str(zones.crs), elapsed=elapsed)
            except Exception as exc:
                st.error(f"City2Graph mobility returned an error: {exc}")

elif workflow == "Transportation / GTFS":
    st.markdown("### Transportation / GTFS")
    st.markdown('<p class="ng-help">Upload a GTFS feed and build a travel-summary graph for a selected service period.</p>', unsafe_allow_html=True)
    gtfs = st.file_uploader("Upload GTFS ZIP feed", type=["zip"], key="gtfs")
    if gtfs is not None:
        c1, c2 = st.columns(2)
        start_date = c1.date_input("Service start date")
        end_date = c2.date_input("Service end date", value=start_date)
        if end_date < start_date:
            st.error("End date cannot be earlier than start date.")
            st.stop()
        if st.button("▶ Build Transit Graph", type="primary", use_container_width=True):
            started = datetime.now(timezone.utc)
            try:
                result = gtfs_graph(gtfs.getvalue(), calendar_start=start_date.strftime("%Y%m%d"), calendar_end=end_date.strftime("%Y%m%d"))
                elapsed = (datetime.now(timezone.utc) - started).total_seconds()
                show_result(result, operation="GTFS travel-summary graph", params={"calendar_start": start_date.strftime("%Y%m%d"), "calendar_end": end_date.strftime("%Y%m%d")}, input_features=0, input_crs=None, elapsed=elapsed)
            except Exception as exc:
                st.error(f"City2Graph transportation returned an error: {exc}")

else:
    st.markdown("### GNN / PyTorch Geometric")
    st.markdown('<p class="ng-help">Use the City2Graph PyG conversion boundary. Advanced ML dependencies remain optional for the basic deployment.</p>', unsafe_allow_html=True)
    st.info("PyTorch/PyG are intentionally separated from the basic no-code installation. Run a graph workflow first, then use the dedicated PyG adapter in an ML-enabled environment.")
