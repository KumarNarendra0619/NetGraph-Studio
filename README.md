# NetGraph Studio

**A non-coder research workbench for City2Graph.**

NetGraph Studio provides a simple GitHub/Streamlit interface for running geospatial graph workflows without writing Python.

## Locked scientific architecture

```text
User → Simple UI → Input Validation → NetGraph Adapter → Original City2Graph API → Result → Visualization / Export
```

**The UI is not the scientific engine.** NetGraph Studio does not reimplement City2Graph algorithms, silently alter analysis parameters, or change node/edge semantics. Visualization may use a separate temporary copy for display projection; source data and City2Graph computation remain unchanged.

## Upstream baseline

The application is currently audited against **City2Graph 1.0.0** from the upstream repository's current `main` revision used for this build. The dependency is pinned to `city2graph==1.0.0` for reproducibility. City2Graph 1.0.0 declares Python `>=3.12,<3.15` and is licensed BSD-3-Clause.

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

A direct adapter to `od_matrix_to_graph`, supporting edge-list and adjacency-matrix workflows, zone IDs, weights, thresholds, self-loop policy, edge-geometry policy and directed/undirected configuration through the upstream API.

### 4. Transportation / GTFS

A direct adapter to the upstream GTFS transportation API. NetGraph Studio does not reconstruct the transportation algorithm.

### 5. GNN / PyG boundary

The repository contains a dedicated adapter boundary for City2Graph's PyTorch Geometric conversion APIs. PyTorch/PyG remain optional and are deliberately kept outside the basic non-coder installation.

## Result layer

- Node and edge counts
- Components
- Average degree
- Interactive map preview
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

## Scientific QA

The repository now contains both implementation and regression/fidelity coverage. The test suite includes:

- core import/startup checks
- dependency manifest checks
- input and parameter validation
- direct City2Graph fidelity tests for all proximity methods
- Queen/Rook contiguity fidelity
- export regression tests
- reproducibility-record tests
- upstream City2Graph public-signature contract tests
- a guard against accidentally reimplementing graph construction in the adapter

A green GitHub Actions run is still required before declaring the assembled build runtime-PASS. Source inspection alone is not treated as a PASS.

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
│   └── report.py
├── tests/
│   ├── test_adapter.py
│   ├── test_fidelity.py
│   ├── test_all_proximity_fidelity.py
│   ├── test_contiguity_fidelity.py
│   ├── test_validation.py
│   ├── test_imports.py
│   ├── test_app_smoke.py
│   ├── test_requirements.py
│   ├── test_export.py
│   ├── test_report.py
│   ├── test_upstream_contract.py
│   └── test_no_reimplementation.py
├── docs/
│   └── DEBUG_STATUS.md
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
