# NetGraph Studio

**A non-coder research workbench for City2Graph.**

NetGraph Studio provides a simple GitHub/Streamlit interface for running geospatial graph workflows without writing Python.

## Locked scientific architecture

```text
User → Simple UI → Input Validation → NetGraph Adapter → Original City2Graph API → Result → Visualization / Export
```

**The UI is not the scientific engine.** NetGraph Studio does not reimplement City2Graph algorithms, silently reproject data, change parameters, simplify geometry, or alter node/edge semantics.

## Implemented workflow stages

### 1. Proximity / Contiguity

- KNN
- Delaunay
- Gabriel
- Relative Neighbourhood
- Euclidean Minimum Spanning Tree
- Fixed Radius
- Waxman
- Queen / Rook contiguity
- Euclidean / Manhattan / Network distance inputs
- Network layer + numeric weight-field selection

### 2. Urban Morphology

A direct adapter to City2Graph's morphology workflow for building/place and movement/street layers. Heterogeneous node and edge dictionaries are retained as returned by City2Graph.

### 3. Mobility / OD

A direct adapter to `od_matrix_to_graph`, supporting edge-list and adjacency-matrix workflows, zone IDs, weights, thresholds and directed/undirected configuration through the upstream API.

### 4. Transportation / GTFS

A direct adapter to the upstream GTFS transportation API. NetGraph Studio does not reconstruct the transportation algorithm.

### 5. GNN / PyG boundary

The repository contains a dedicated adapter boundary for City2Graph's PyTorch Geometric conversion APIs. PyTorch/PyG remain optional and are deliberately kept outside the basic non-coder installation until final deployment hardening.

## Result layer

- Node and edge counts
- Components
- Average degree
- Interactive map preview where spatial nodes are directly renderable
- Node/edge tables
- GeoJSON and CSV export
- GraphML, GML and edge-list export
- Research/reproducibility JSON
- City2Graph version metadata

## Research mode

Research Mode records:

- workflow and method
- user-selected parameters
- input feature count
- input CRS
- processing time
- result node/edge counts
- City2Graph version
- UTC timestamp
- algorithm-source declaration

## Scientific QA — intentionally deferred

As requested for this build phase, the repository now contains the QA/fidelity framework, but the final debugging campaign is intentionally deferred until all stages are assembled.

The debugging campaign will compare direct City2Graph execution with NetGraph Studio execution for:

- node IDs
- edge pairs
- edge attributes/weights
- geometry
- CRS
- graph statistics
- heterogeneous node/edge types

The result of each comparison will be recorded as PASS/FAIL. No claim of zero defects is made before this campaign is completed.

## Repository structure

```text
NetGraph-Studio/
├── app.py
├── requirements.txt
├── netgraph/
│   ├── __init__.py
│   ├── adapter.py
│   ├── advanced.py
│   ├── export.py
│   ├── io.py
│   ├── report.py
│   └── validation.py
├── tests/
│   ├── test_adapter.py
│   └── test_fidelity.py
├── .streamlit/
│   └── config.toml
└── .github/workflows/
    └── tests.yml
```

## Deployment target

Primary target: **GitHub + Streamlit**.

The application is designed so that a non-Python user sees a controlled workflow rather than Python functions or code.

## Attribution

NetGraph Studio uses the open-source [City2Graph](https://github.com/c2g-dev/city2graph) library. City2Graph is an independent upstream project. Users must comply with City2Graph's applicable license and citation requirements.

City2Graph documentation: https://city2graph.net

NetGraph Studio is an independent project and is not an official City2Graph product unless explicitly stated by the City2Graph maintainers.
