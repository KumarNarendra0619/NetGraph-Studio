# NetGraph Studio

**A non-coder research workbench for City2Graph.**

NetGraph Studio makes selected geospatial graph workflows accessible to researchers, GIS users, planners, students and other non-programmers through a guided Streamlit interface.

> **Upload → Select workflow → Configure → Run → Explore → Export**

## What NetGraph Studio is

NetGraph Studio is an **independent interface and orchestration layer** around the open-source City2Graph library. It is designed to make City2Graph workflows usable without writing Python.

It is **not a replacement implementation of City2Graph**.

## Locked scientific architecture

```text
User
  ↓
Streamlit UI
  ↓
Input / Parameter Validation
  ↓
NetGraph Adapter
  ↓
Original City2Graph API
  ↓
City2Graph Result
  ↓
Presentation / Export
```

The UI is not the scientific engine. NetGraph Studio must not reimplement City2Graph graph-construction algorithms, silently change analytical parameters, or alter node/edge semantics. Where display projection or rendering requires transformation, a separate display copy is used so that the computational source remains unchanged.

## Current upstream baseline

The application is audited against **City2Graph 1.0.0** for the current build and pins `city2graph==1.0.0` for reproducibility. The upstream package declares Python `>=3.12,<3.15` and uses the BSD-3-Clause license.

Upstream project: https://github.com/c2g-dev/city2graph

Documentation: https://city2graph.net

## Supported workflow families

### Proximity / graph construction

- KNN
- Delaunay
- Gabriel
- Relative Neighbourhood
- Euclidean Minimum Spanning Tree
- Fixed Radius
- Waxman
- Euclidean / Manhattan / Network distance inputs
- Network layer and numeric weight-field selection

### Polygon contiguity

- Queen
- Rook

### Urban morphology

Direct adapter coverage for the upstream morphology workflow. Heterogeneous node and edge structures are retained as returned by City2Graph.

### Mobility / OD

Direct adapter coverage for `od_matrix_to_graph`, including edge-list and adjacency-matrix workflows and upstream-supported configuration such as zone IDs, weights, thresholds, self-loop policy, edge-geometry policy and directed/undirected mode.

### Transportation / GTFS

Direct adapter coverage for the upstream GTFS transportation API. NetGraph Studio does not reconstruct the transportation algorithm.

### GNN / PyG boundary

A dedicated boundary is available for City2Graph's PyTorch Geometric conversion APIs. PyTorch/PyG remain optional and are outside the basic non-coder installation.

## Result layer

Where supported by a workflow, users can inspect:

- node and edge counts
- connected components
- average degree
- interactive map preview
- node table
- edge table
- GeoJSON / CSV export
- GraphML / GML / edge-list export
- reproducibility JSON
- City2Graph and NetGraph Studio version metadata

## Research Mode

Research Mode records the analytical provenance needed to reproduce a run:

- workflow and method
- user-selected parameters
- input feature count
- input CRS
- processing time
- result node/edge counts
- City2Graph version
- NetGraph Studio version
- UTC timestamp
- algorithm-source declaration

## Non-coder UI principles

The interface follows four rules:

1. **Progressive disclosure:** show only parameters relevant to the selected method.
2. **Human-readable controls:** expose concepts and units, not Python argument names.
3. **No hidden scientific changes:** defaults affecting computation are visible or documented.
4. **Clear result separation:** computed results, display representation and diagnostics are presented separately.

Full UI specification: [`docs/STREAMLIT_UI.md`](docs/STREAMLIT_UI.md).

## Repository architecture

```text
NetGraph-Studio/
├── app.py
├── requirements.txt
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── netgraph/
│   ├── __init__.py
│   ├── adapter.py
│   ├── advanced.py
│   ├── export.py
│   ├── io.py
│   ├── report.py
│   └── ui/                     # planned UI component boundary
│       ├── __init__.py
│       ├── layout.py
│       ├── workflow_registry.py
│       ├── input_panel.py
│       ├── parameter_panel.py
│       ├── run_panel.py
│       ├── result_panel.py
│       ├── export_panel.py
│       └── messages.py
├── tests/
│   ├── test_adapter.py
│   ├── test_fidelity.py
│   ├── test_all_proximity_fidelity.py
│   ├── test_contiguity_fidelity.py
│   ├── test_validation.py
│   ├── test_imports.py
│   ├── test_streamlit_smoke.py
│   ├── test_app_smoke.py
│   ├── test_requirements.py
│   ├── test_export.py
│   ├── test_report.py
│   ├── test_upstream_contract.py
│   └── test_no_reimplementation.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── ATTRIBUTION.md
│   ├── STREAMLIT_UI.md
│   ├── DEBUG_STATUS.md
│   └── DEPLOY_STREAMLIT.md
├── .streamlit/
│   └── config.toml
└── .github/
    └── workflows/
        └── tests.yml
```

## Deployment

**Recommended public deployment:** GitHub + Streamlit Community Cloud.

GitHub Pages is not the application runtime because Streamlit requires a Python execution environment. See [`docs/DEPLOY_STREAMLIT.md`](docs/DEPLOY_STREAMLIT.md).

## Attribution and authorship boundary

NetGraph Studio is an independent project by **Dr. Narendra Kumar**.

NetGraph Studio uses **City2Graph** as an upstream open-source computational library. NetGraph Studio does not claim authorship of City2Graph's algorithms, source code or upstream implementation.

City2Graph remains an independent upstream project. NetGraph Studio is **not an official City2Graph product** and must not be represented as endorsed by or affiliated with the City2Graph maintainers unless an explicit relationship exists.

Detailed attribution policy: [`docs/ATTRIBUTION.md`](docs/ATTRIBUTION.md).

## License

NetGraph Studio source code is released under the **MIT License**. Copyright © 2026 Dr. Narendra Kumar.

The MIT license applies to NetGraph Studio's own source code. Third-party dependencies remain under their respective licenses. In particular, City2Graph remains subject to its upstream BSD-3-Clause license.

See:

- [`LICENSE`](LICENSE) — NetGraph Studio license
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) — third-party attribution and license boundary

## Scientific QA

A green GitHub Actions run is required before declaring a build runtime-PASS. Source inspection alone is not treated as a PASS.

The test suite covers imports, startup, dependency declarations, validation, direct City2Graph fidelity, contiguity fidelity, exports, reproducibility records, upstream API contracts and a guard against accidental graph-algorithm reimplementation.
