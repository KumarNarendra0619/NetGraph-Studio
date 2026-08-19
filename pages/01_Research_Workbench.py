"""Research Workbench — transparent no-code research workflow.

This page orchestrates the existing NetGraph/City2Graph adapter. It does not
reimplement graph algorithms or modify City2Graph mathematics/defaults.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import io
import json

import geopandas as gpd
import networkx as nx
import pandas as pd
import streamlit as st

from netgraph.adapter import OPERATIONS, run_operation
from netgraph.io import read_vector, save_uploaded_file

st.set_page_config(page_title="Research Workbench · NetGraph Studio", page_icon="🧪", layout="wide")

st.markdown("""
<style>
.rw-hero{padding:22px 24px;border:1px solid rgba(47,124,246,.22);border-radius:18px;background:linear-gradient(135deg,rgba(47,124,246,.10),rgba(109,93,252,.06));margin-bottom:18px}
.rw-title{font-size:1.65rem;font-weight:850;letter-spacing:-.03em}.rw-sub{opacity:.72;margin-top:4px}
.rw-step{font-size:.72rem;text-transform:uppercase;letter-spacing:.10em;font-weight:800;color:#2f7cf6;margin:8px 0}
.rw-card{border:1px solid rgba(128,128,128,.18);border-radius:14px;padding:14px 16px;background:rgba(128,128,128,.025);height:100%}
.rw-ok{color:#16834b;font-weight:750}.rw-warn{color:#a66a00;font-weight:750}.rw-code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.78rem}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="rw-hero">
  <div class="rw-title">🧪 Research Workbench</div>
  <div class="rw-sub">From geospatial data to transparent, reproducible network evidence — without coding.</div>
</div>
""", unsafe_allow_html=True)

if "rw_result" not in st.session_state:
    st.session_state.rw_result = None


def file_hash(uploaded) -> str:
    data = uploaded.getvalue()
    return hashlib.sha256(data).hexdigest()


def graph_from_result(result):
    if isinstance(result, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
        return result, None, None
    if isinstance(result, tuple) and len(result) == 2 and hasattr(result[0], "geometry"):
        nodes, edges = result
        directed = isinstance(edges.index, pd.MultiIndex) and bool(edges.attrs.get("directed", False))
        graph = nx.DiGraph() if directed else nx.Graph()
        graph.add_nodes_from(nodes.index)
        if isinstance(edges.index, pd.MultiIndex):
            graph.add_edges_from((i[0], i[1]) for i in edges.index)
        return graph, nodes, edges
    return None, None, None


def quality_report(gdf: gpd.GeoDataFrame) -> dict:
    geom = gdf.geometry
    invalid = int((~geom.is_valid).sum()) if len(gdf) else 0
    empty = int(geom.is_empty.sum()) if len(gdf) else 0
    missing = int(geom.isna().sum()) if len(gdf) else 0
    duplicates = int(gdf.geometry.to_wkb().duplicated().sum()) if len(gdf) else 0
    return {
        "features": len(gdf),
        "crs": str(gdf.crs),
        "geometry_types": ", ".join(sorted(geom.geom_type.dropna().unique().tolist())),
        "invalid_geometries": invalid,
        "empty_geometries": empty,
        "missing_geometries": missing,
        "duplicate_geometries": duplicates,
        "missing_values": int(gdf.isna().sum().sum()),
    }


def graph_metrics(graph: nx.Graph) -> dict:
    n, e = graph.number_of_nodes(), graph.number_of_edges()
    degree = dict(graph.degree())
    try:
        components = nx.number_connected_components(graph.to_undirected())
    except Exception:
        components = None
    return {
        "nodes": n,
        "edges": e,
        "components": components,
        "isolates": len(list(nx.isolates(graph))),
        "density": float(nx.density(graph)) if n > 1 else 0.0,
        "mean_degree": float(sum(degree.values()) / n) if n else 0.0,
        "max_degree": max(degree.values()) if degree else 0,
    }


# 01 DATA + QC
st.markdown('<div class="rw-step">01 · Data & quality control</div>', unsafe_allow_html=True)
uploaded = st.file_uploader("Upload the spatial input layer", type=["geojson", "json", "gpkg", "parquet", "feather", "shp"], key="rw_input")
if uploaded is None:
    st.info("Start with a point or polygon layer. The Workbench will inspect it before any graph is constructed.")
    st.stop()

try:
    gdf = read_vector(save_uploaded_file(uploaded))
except Exception as exc:
    st.error(f"Input could not be read: {exc}")
    st.stop()

qc = quality_report(gdf)
q1, q2, q3, q4 = st.columns(4)
q1.metric("Features", f"{qc['features']:,}")
q2.metric("Invalid geometries", f"{qc['invalid_geometries']:,}")
q3.metric("Missing geometries", f"{qc['missing_geometries']:,}")
q4.metric("Duplicate geometries", f"{qc['duplicate_geometries']:,}")

if qc["invalid_geometries"] or qc["empty_geometries"] or qc["missing_geometries"]:
    st.warning("QC found geometry issues. NetGraph Studio will not silently repair them; review the input before running the graph.")
else:
    st.markdown('<div class="rw-ok">✓ Geometry QC passed without automatic modification.</div>', unsafe_allow_html=True)

with st.expander("View QC details", expanded=False):
    st.json(qc)

# 02 GRAPH DESIGN
st.markdown('<div class="rw-step">02 · Graph design</div>', unsafe_allow_html=True)
method_key = st.selectbox("Graph construction method", list(OPERATIONS), format_func=lambda x: OPERATIONS[x].label)
params: dict = {}
if method_key == "knn":
    params["k"] = st.number_input("k — nearest neighbours", min_value=1, max_value=100, value=5)
elif method_key == "radius":
    params["radius"] = st.number_input("Connection radius", min_value=0.000001, value=1000.0)
elif method_key == "waxman":
    c1, c2 = st.columns(2)
    params["beta"] = c1.number_input("Beta", min_value=0.000001, max_value=1.0, value=0.2)
    params["r0"] = c2.number_input("r0", min_value=0.000001, value=1000.0)
    params["seed"] = st.number_input("Random seed", min_value=0, value=42)
elif method_key == "contiguity":
    params["contiguity"] = st.selectbox("Contiguity rule", ["queen", "rook"])

if method_key != "contiguity":
    params["distance_metric"] = st.selectbox("Distance metric", ["euclidean", "manhattan", "network"])
    params["network_gdf"] = None
    params["network_weight"] = None

st.caption("Transparent method contract: NetGraph Studio validates and records parameters, then delegates graph construction to City2Graph.")

# 03 VALIDATION / RUN
st.markdown('<div class="rw-step">03 · Construct & validate</div>', unsafe_allow_html=True)
run_col, sens_col = st.columns([2, 1])
with run_col:
    run_now = st.button("▶ Construct graph with City2Graph", type="primary", use_container_width=True)
with sens_col:
    run_sensitivity = st.checkbox("Sensitivity analysis", value=False, help="Runs the selected method repeatedly with an explicit parameter grid. No hidden parameter changes are applied.")

sensitivity_values = None
if run_sensitivity:
    if method_key == "knn":
        sensitivity_values = st.multiselect("k values", [1, 3, 5, 7, 9, 11, 15], default=[3, 5, 7, 9])
    elif method_key == "radius":
        sensitivity_values = st.text_input("Radius values (comma-separated)", "500,1000,1500,2000")
    else:
        st.info("Sensitivity controls are currently enabled for KNN and fixed-radius workflows; other methods remain single-run to avoid ambiguous parameter grids.")

if run_now:
    started = datetime.now(timezone.utc)
    try:
        result = run_operation(gdf, method_key, **params)
        elapsed = (datetime.now(timezone.utc) - started).total_seconds()
        graph, nodes, edges = graph_from_result(result)
        if graph is None:
            st.warning("The selected operation returned a result that is not represented as a NetworkX graph by this page.")
        else:
            metrics = graph_metrics(graph)
            record = {
                "software": "NetGraph Studio",
                "engine": "City2Graph",
                "operation": method_key,
                "parameters": {k: ("<GeoDataFrame>" if k == "network_gdf" else v) for k, v in params.items()},
                "input": {"features": len(gdf), "crs": str(gdf.crs), "sha256": file_hash(uploaded)},
                "metrics": metrics,
                "processing_seconds": elapsed,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            }
            st.session_state.rw_result = {"graph": graph, "nodes": nodes, "edges": edges, "metrics": metrics, "record": record}
    except Exception as exc:
        st.error(f"City2Graph returned an error: {exc}")

# Sensitivity runs are explicit and reproducible.
if run_sensitivity and sensitivity_values:
    values = sensitivity_values
    if method_key == "radius" and isinstance(values, str):
        try:
            values = [float(v.strip()) for v in values.split(",") if v.strip()]
        except ValueError:
            values = []
    rows = []
    if values:
        with st.status("Running explicit sensitivity grid…", expanded=False) as status:
            for value in values:
                local = dict(params)
                local["k" if method_key == "knn" else "radius"] = value
                try:
                    res = run_operation(gdf, method_key, **local)
                    graph, _, _ = graph_from_result(res)
                    if graph is not None:
                        m = graph_metrics(graph)
                        m["parameter"] = value
                        rows.append(m)
                except Exception as exc:
                    rows.append({"parameter": value, "error": str(exc)})
            status.update(label="Sensitivity complete", state="complete")
    if rows:
        sensitivity_df = pd.DataFrame(rows)
        st.markdown("#### Sensitivity evidence")
        st.dataframe(sensitivity_df, use_container_width=True)
        st.download_button("Download sensitivity CSV", sensitivity_df.to_csv(index=False).encode("utf-8"), "graph_sensitivity.csv", "text/csv")

# 04 EVIDENCE + REPRODUCIBILITY
result = st.session_state.rw_result
if result:
    st.markdown('<div class="rw-step">04 · Evidence & reproducibility</div>', unsafe_allow_html=True)
    m = result["metrics"]
    a, b, c, d, e = st.columns(5)
    a.metric("Nodes", f"{m['nodes']:,}")
    b.metric("Edges", f"{m['edges']:,}")
    c.metric("Components", str(m["components"]))
    d.metric("Density", f"{m['density']:.4f}")
    e.metric("Mean degree", f"{m['mean_degree']:.2f}")

    t1, t2, t3 = st.tabs(["Graph evidence", "Method record", "Research package"])
    with t1:
        st.dataframe(pd.DataFrame([m]), use_container_width=True)
        if result["nodes"] is not None:
            st.dataframe(result["nodes"].drop(columns="geometry", errors="ignore"), use_container_width=True)
    with t2:
        st.json(result["record"])
        st.download_button("Download reproducibility JSON", json.dumps(result["record"], indent=2, default=str).encode("utf-8"), "netgraph_reproducibility.json", "application/json")
    with t3:
        package = {
            "01_method_record.json": json.dumps(result["record"], indent=2, default=str),
            "02_graph_metrics.csv": pd.DataFrame([m]).to_csv(index=False),
            "03_readme.txt": "NetGraph Studio research evidence package. Graph construction delegated to City2Graph; parameters and input hash recorded for reproducibility.",
        }
        st.info("The research package records computational evidence; it does not fabricate interpretation or manuscript claims.")
        st.download_button("Download method record", package["01_method_record.json"].encode(), "01_method_record.json", "application/json")
        st.download_button("Download metrics table", package["02_graph_metrics.csv"].encode(), "02_graph_metrics.csv", "text/csv")

st.caption("Research integrity rule: automation is transparent, parameter changes are explicit, and City2Graph remains the computational engine.")
