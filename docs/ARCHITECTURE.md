# NetGraph Studio Architecture

## Purpose

NetGraph Studio is a no-code research workbench for supported City2Graph workflows. Its purpose is to reduce the programming barrier without replacing the upstream graph-construction engine.

## Architectural boundary

```text
User
  ↓
Streamlit UI
  ↓
Input / Parameter Validation
  ↓
NetGraph Adapter Layer
  ↓
City2Graph Public API
  ↓
Graph / Network Result
  ↓
Visualization + Statistics + Export
  ↓
Research / Reproducibility Record
```

## Scientific invariants

- User-interface operations must not silently modify scientific parameters.
- Graph construction should be delegated to the supported City2Graph API.
- Node and edge semantics returned by City2Graph should be preserved.
- Visualization transformations must be isolated from analytical data.
- Export should represent the computed result rather than a separately reconstructed graph.
- Software-version metadata should be recorded for reproducibility.

## Main workflow families

| Family | Purpose | Upstream boundary |
|---|---|---|
| Proximity | Point-based spatial graphs | City2Graph proximity API |
| Contiguity | Polygon adjacency graphs | City2Graph contiguity API |
| Urban morphology | Building/street heterogeneous graphs | City2Graph morphology API |
| Mobility / OD | Origin-destination network construction | City2Graph OD API |
| Transportation | GTFS-based network workflows | City2Graph transportation API |
| GNN / PyG | Graph conversion boundary | City2Graph PyG API |

## Reproducibility model

Each research result should retain, where available:

- workflow;
- method;
- selected parameters;
- input feature count;
- input CRS;
- processing time;
- result node/edge counts;
- City2Graph version;
- timestamp;
- algorithm-source declaration.

This architecture separates scientific computation from presentation and supports reproducible research workflows.
