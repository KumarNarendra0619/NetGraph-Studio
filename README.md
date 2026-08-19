# NetGraph Studio

**A No-Code Research Workbench for Spatial Network Analysis**  
*Powered by the City2Graph Python library*

[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-informational.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12--3.14-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red.svg)](https://streamlit.io/)
[![City2Graph](https://img.shields.io/badge/Engine-City2Graph%201.0.0-orange.svg)](https://github.com/c2g-dev/city2graph)
[![Research Software](https://img.shields.io/badge/Type-Research%20Software-purple.svg)](https://github.com/KumarNarendra0619/NetGraph-Studio)

> NetGraph Studio is an independent graphical interface for accessing supported City2Graph workflows without requiring users to write Python code.

---

## 1. Abstract

Spatial network analysis often requires users to combine geospatial preprocessing, graph-construction algorithms, parameter selection, visualization, and export workflows in Python. **NetGraph Studio** provides a no-code research interface that brings these operations into a single Streamlit workbench while retaining the computational semantics of the underlying **City2Graph** library.

The application is deliberately designed as an **integration and presentation layer**, not as a replacement implementation of graph algorithms. Supported graph construction is delegated to the City2Graph public API; NetGraph Studio handles user interaction, input validation, parameter translation, visualization, export, and reproducibility metadata.

### Research software objectives

- Lower the technical barrier to spatial network analysis.
- Preserve the computational behavior of the upstream City2Graph implementation.
- Make analytical parameters explicit and inspectable.
- Support reproducible research records and machine-readable outputs.
- Provide a practical bridge between GIS researchers and Python-based graph analytics.

---

## 2. Scientific Architecture

```text
                         NETGRAPH STUDIO
                    No-Code Research Interface
                              │
                 ┌────────────┴────────────┐
                 │                         │
          Input / Validation        Parameter Controls
                 │                         │
                 └────────────┬────────────┘
                              │
                       Adapter Layer
                              │
                       City2Graph API
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
      Proximity          Mobility / OD       Morphology
      Contiguity          Transportation
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                         Graph Result
                              │
              ┌───────────────┼───────────────┐
              │               │               │
           Mapping        Statistics        Export
              │               │               │
              └───────────────┼───────────────┘
                              │
                 Reproducibility Record
```

### Design principle

**The UI is not the scientific engine.** NetGraph Studio does not intentionally reimplement City2Graph graph-construction algorithms or silently change their node/edge semantics. Where visualization requires a display-specific representation, the application may create a temporary visualization copy without modifying the computational input/result.

---

## 3. Supported Analytical Workflows

| Workflow | Supported functionality | Primary output |
|---|---|---|
| Proximity | KNN, Delaunay, Gabriel, RNG, Euclidean MST, Fixed Radius, Waxman | Spatial graph |
| Contiguity | Queen, Rook, distance/weight configurations supported by upstream API | Spatial graph |
| Urban Morphology | Building/place and movement/street morphology workflow | Heterogeneous graph |
| Mobility / OD | Edge-list and adjacency-matrix OD workflows | Directed/undirected OD graph |
| Transportation | GTFS-based transportation workflow | Transit graph |
| GNN / PyG | Upstream PyTorch Geometric conversion boundary | PyG graph objects |

### Proximity and contiguity

- K-Nearest Neighbours (KNN)
- Delaunay triangulation
- Gabriel graph
- Relative Neighbourhood Graph (RNG)
- Euclidean Minimum Spanning Tree (MST)
- Fixed-radius graph
- Waxman graph
- Queen contiguity
- Rook contiguity
- Euclidean / Manhattan / network-distance configurations where supported
- Network layer and numeric weight-field selection where required

### Mobility / OD

The OD interface exposes the relevant upstream configuration boundary, including:

- edge-list or adjacency-matrix input
- zone identifier field
- source/target fields
- weight fields
- threshold
- self-loop policy
- edge-geometry policy
- directed/undirected graph semantics

### Urban morphology

The morphology interface delegates to the upstream City2Graph workflow and retains the heterogeneous node/edge structure returned by the library rather than flattening it into a generic graph representation.

### Transportation / GTFS

GTFS processing is delegated to the upstream City2Graph transportation API. NetGraph Studio does not reconstruct the transportation algorithm independently.

### GNN / PyG boundary

A dedicated adapter boundary is maintained for City2Graph's PyTorch Geometric conversion APIs. PyTorch/PyG remain optional so that the basic non-coder installation stays lightweight.

---

## 4. Method–Parameter Matrix

| Method family | Examples | Typical parameters | Output |
|---|---|---|---|
| Proximity | KNN | `k`, metric | Graph |
| Proximity | Radius | radius, metric | Graph |
| Proximity | Waxman | alpha, beta, distance configuration | Graph |
| Proximity | Delaunay / Gabriel / RNG | geometry | Graph |
| Connectivity | MST | distance configuration | Graph |
| Contiguity | Queen / Rook | geometry, weight configuration | Graph |
| OD | OD matrix / edge list | threshold, directed, loops, geometry | OD graph |
| Morphology | Building–movement | distance/buffer/geometry parameters | Heterogeneous graph |
| GTFS | Transit | feed and transportation parameters | Transit graph |

The exact parameter set remains governed by the audited City2Graph public API rather than by a separate reimplementation.

---

## 5. Data and Input Model

NetGraph Studio is intended for researchers working with spatial and network datasets. Supported inputs depend on the selected workflow and are validated before processing.

Typical data classes include:

- point or polygon geospatial layers
- network/street layers
- OD edge lists
- OD adjacency matrices
- building and movement layers
- GTFS feeds
- numeric attribute fields used as network weights

The application reports relevant input metadata such as feature count and CRS in Research Mode.

---

## 6. Result and Export Layer

The interface is designed around a simple non-coder workflow:

```text
Upload → Select workflow → Set parameters → Run → View → Export
```

Results can include:

- node count
- edge count
- connected components
- average degree
- interactive map preview
- node and edge tables
- GeoJSON / CSV exports where applicable
- GraphML / GML / edge-list exports where applicable
- research/reproducibility JSON
- City2Graph version metadata

Directed workflows retain directed graph semantics through the result and export layer where supported.

---

## 7. Research Mode and Reproducibility

Research Mode records the analytical context needed to understand and reproduce a run, including:

- workflow
- selected method
- user-selected parameters
- input feature count
- input CRS
- processing time
- result node/edge counts
- City2Graph version
- UTC timestamp
- algorithm-source declaration

See [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) for the reproducibility protocol.

---

## 8. Validation and Scientific QA

The repository includes multiple test layers:

- core import/startup checks
- Streamlit entrypoint smoke tests
- dependency manifest checks
- input and parameter validation
- direct City2Graph fidelity tests
- proximity-method regression tests
- Queen/Rook contiguity fidelity tests
- export regression tests
- reproducibility-record tests
- upstream public-signature contract tests
- no-reimplementation guard for graph construction

### Fidelity principle

For a supported workflow, the intended invariant is:

```text
Same input + same parameters
            ↓
   Direct City2Graph API
            ≡
    NetGraph Studio
```

A source-code inspection is **not** treated as a runtime PASS. A green GitHub Actions execution is required before a build is declared runtime-verified.

---

## 9. Reproducibility and Versioning

The current baseline pins:

```text
city2graph==1.0.0
```

This prevents uncontrolled upstream changes from altering the computational environment. The audited City2Graph 1.0.0 baseline declares Python `>=3.12,<3.15`.

For research use, record the NetGraph Studio version/commit, City2Graph version, input dataset, parameter configuration, and exported research record.

---

## 10. Repository Structure

```text
NetGraph-Studio/
├── app.py
├── LICENSE
├── THIRD-PARTY-NOTICES
├── CITATION.cff
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── requirements.txt
│
├── netgraph/
│   ├── __init__.py
│   ├── adapter.py
│   ├── advanced.py
│   ├── io.py
│   ├── export.py
│   └── report.py
│
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
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── METHODOLOGY.md
│   ├── REPRODUCIBILITY.md
│   ├── DEBUG_STATUS.md
│   └── DEPLOY_STREAMLIT.md
│
├── .streamlit/
│   └── config.toml
│
└── .github/
    └── workflows/
        └── tests.yml
```

---

## 11. Installation

### Python environment

Use Python 3.12–3.14 and install the pinned dependencies:

```bash
pip install -r requirements.txt
```

### Run locally

```bash
streamlit run app.py
```

The browser interface is intended to hide Python implementation details from end users.

---

## 12. Web Deployment

The recommended public deployment is **GitHub + Streamlit Community Cloud**.

GitHub Pages is not the application runtime because NetGraph Studio is a Python/Streamlit application. The deployment guide is available at [`docs/DEPLOY_STREAMLIT.md`](docs/DEPLOY_STREAMLIT.md).

The intended public-user experience is:

**Upload → Choose → Configure → Run → Inspect → Export**

---

## 13. Academic Software Citation

If NetGraph Studio contributes to a research workflow, please cite the software using the metadata in [`CITATION.cff`](CITATION.cff). The project should be cited by release/commit where possible so that analyses remain traceable.

NetGraph Studio should not be presented as the original source of City2Graph algorithms. City2Graph must be acknowledged separately when its functionality is used.

---

## 14. City2Graph Attribution

NetGraph Studio uses the open-source [City2Graph](https://github.com/c2g-dev/city2graph) Python library as a third-party dependency.

City2Graph is an independent upstream project developed by **Yuta Sato and City2Graph contributors** and distributed under the **BSD 3-Clause License**. The applicable upstream notice is preserved in [`THIRD-PARTY-NOTICES`](THIRD-PARTY-NOTICES).

City2Graph documentation: https://city2graph.net

**NetGraph Studio is an independent project and is not an official City2Graph product unless explicitly stated by the City2Graph maintainers.**

---

## 15. License

NetGraph Studio application code is released under the **BSD 3-Clause License**. Copyright (c) 2026 Dr. Narendra Kumar.

City2Graph remains a separate third-party work under its own BSD 3-Clause License and copyright notice. These works are not merged into a single copyright claim.

See:

- [`LICENSE`](LICENSE) — NetGraph Studio
- [`THIRD-PARTY-NOTICES`](THIRD-PARTY-NOTICES) — City2Graph and third-party attribution

---

## 16. Contributing

Contributions are welcome when they preserve the scientific and architectural principles of the project. Before changing graph-construction behavior, contributors should verify the relevant City2Graph public API and add or update fidelity/regression tests.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 17. Project Status

**Development status:** Active research software / pre-release validation.

The repository is being developed toward a stable non-coder research interface. Runtime CI, representative end-to-end datasets, and deployment verification must pass before a release is labelled production-ready.

---

## Links

- **Repository:** https://github.com/KumarNarendra0619/NetGraph-Studio
- **City2Graph:** https://github.com/c2g-dev/city2graph
- **City2Graph documentation:** https://city2graph.net
