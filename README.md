# NetGraph Studio

**A non-coder friendly research workbench for City2Graph.**

NetGraph Studio provides a simple web interface for turning geospatial data into spatial graphs without requiring users to write Python.

## Core scientific principle

NetGraph Studio is an **independent UI and workflow layer around the original City2Graph Python library**. It does not reimplement City2Graph graph algorithms or change their mathematical operations.

```text
User → UI → Validation → City2Graph Adapter → Original City2Graph API → Results
```

The adapter exists only to translate safe UI selections into explicit City2Graph function calls.

## Current MVP

The first working UI scaffold includes:

- Streamlit web interface
- Simple / Research mode switch
- GeoJSON, GeoPackage, GeoParquet and Feather input
- Input feature, geometry and CRS summary
- KNN
- Delaunay
- Gabriel
- Relative Neighbourhood Graph
- Minimum Spanning Tree
- Fixed Radius
- Waxman
- Queen / Rook polygon contiguity
- Euclidean / Manhattan distance selection
- Node and edge statistics
- Interactive point/centroid preview
- GeoJSON and CSV downloads
- Research configuration record
- Automated adapter regression tests
- Direct City2Graph output-fidelity regression test for KNN
- GitHub Actions test workflow

## Modes

### Simple Mode

```text
Upload → Choose operation → Set parameters → Run → Result → Download
```

Designed for GIS users, students, planners and researchers who do not want to write Python.

### Research Mode

Adds:

- CRS information
- selected method and parameters
- processing time
- reproducibility information
- result statistics
- algorithm-source declaration

## Development roadmap

### Stage 2 — Output Fidelity & Validation

- Harden file validation and multi-file Shapefile handling.
- Add network-distance input and validation.
- Expand numerical regression tests against direct City2Graph calls.
- Verify node, edge, weight, geometry and CRS fidelity for supported workflows.

### Stage 3 — Extended City2Graph Workflows

- Morphology workflows.
- Mobility / OD workflows.
- Transportation workflows.
- Heterogeneous graph workflows.
- NetworkX / PyTorch Geometric exports where supported by City2Graph.

### Stage 4 — Visualization & Reproducibility

- Rich graph visualization.
- Richer map rendering.
- Full reproducibility report export.

### Stage 5 — Deployment

- Production hardening.
- CI/CD.
- Streamlit deployment.
- Release documentation.

## Output fidelity policy

NetGraph Studio will not silently:

- change scientific parameters
- reproject data without disclosure
- simplify geometries without disclosure
- replace City2Graph algorithms
- approximate graph construction
- alter node/edge semantics

Validation and visualization are separate from graph computation.

## Repository structure

```text
NetGraph-Studio/
├── app.py
├── requirements.txt
├── netgraph/
│   ├── __init__.py
│   ├── adapter.py
│   └── io.py
├── tests/
│   ├── test_adapter.py
│   └── test_fidelity.py
├── .streamlit/
│   └── config.toml
└── .github/workflows/
    └── tests.yml
```

## Attribution

NetGraph Studio uses the open-source [City2Graph](https://github.com/c2g-dev/city2graph) library. City2Graph is distributed under the BSD 3-Clause license. Users of City2Graph should cite:

Sato, Y., Pietrostefani, E., Mahabir, R., & Arribas-Bel, D. (2026). *City2Graph: A Python library for Heterogeneous Graph Neural Networks and spatial analysis in urban systems*. Computers, Environment and Urban Systems, 130, 102492. DOI: 10.1016/j.compenvurbsys.2026.102492.

City2Graph documentation: https://city2graph.net

NetGraph Studio is an independent project and is not an official City2Graph product unless explicitly stated by the City2Graph maintainers.
