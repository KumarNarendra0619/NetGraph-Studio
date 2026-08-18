# NetGraph Studio

**A non-coder friendly research workbench for City2Graph.**

NetGraph Studio provides a simple web interface for turning geospatial data into spatial graphs without requiring users to write Python.

## Core scientific principle

NetGraph Studio is a **UI wrapper around the original City2Graph Python library**. It does not reimplement City2Graph graph algorithms or change their mathematical operations.

```text
User → UI → Validation → City2Graph Adapter → Original City2Graph API → Results
```

The adapter exists only to translate safe UI selections into explicit City2Graph function calls.

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
- package/runtime metadata
- processing log
- reproducibility configuration
- result statistics

## Planned workflow areas

- Spatial proximity graphs
- Contiguity graphs
- Urban morphology
- Street/network graphs
- Mobility / OD graphs
- Public transport graphs
- Heterogeneous graphs
- GNN-ready exports

## Output fidelity policy

NetGraph Studio will not silently:

- change scientific parameters
- reproject data without disclosure
- simplify geometries without disclosure
- replace City2Graph algorithms
- approximate graph construction
- alter node/edge semantics

Validation and visualization are separate from graph computation.

## Technology

- Python
- Streamlit
- GeoPandas
- City2Graph
- NetworkX
- optional PyTorch Geometric

## Development status

Foundation implementation in progress.

## Attribution

NetGraph Studio uses the open-source [City2Graph](https://github.com/c2g-dev/city2graph) library. City2Graph is distributed under the BSD 3-Clause license. Users of City2Graph should cite:

Sato, Y., Pietrostefani, E., Mahabir, R., & Arribas-Bel, D. (2026). *City2Graph: A Python library for Heterogeneous Graph Neural Networks and spatial analysis in urban systems*. Computers, Environment and Urban Systems, 130, 102492. DOI: 10.1016/j.compenvurbsys.2026.102492.

City2Graph documentation: https://city2graph.net
