# NetGraph Studio Architecture

## Purpose

NetGraph Studio is a non-coder research workbench that exposes City2Graph workflows through a guided Streamlit interface. It is an interface and orchestration layer, not a replacement implementation of City2Graph.

## Scientific boundary

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
City2Graph result
  ↓
Result normalization for presentation only
  ↓
Map / tables / metrics / export
```

### Non-negotiable rules

1. Do not reimplement City2Graph graph-construction algorithms in NetGraph Studio.
2. Pass user-selected analytical parameters to the upstream API without silent changes.
3. Preserve node and edge semantics returned by City2Graph.
4. Validation may reject invalid input before execution, but must not silently repair scientific parameters.
5. Presentation transformations must use a separate display copy where required; source data and computational inputs remain unchanged.
6. Every result should retain upstream version metadata for reproducibility.

## Repository layers

```text
app.py                       # Streamlit entry point
netgraph/
├── adapter.py               # Upstream API boundary
├── advanced.py              # Advanced workflow adapters
├── export.py                # Result serialization/export
├── io.py                    # Input loading and schema checks
└── report.py                # Research/reproducibility record

tests/                       # Fidelity, validation, smoke and regression tests
docs/                        # Architecture, deployment and attribution documentation
.streamlit/                  # Streamlit runtime configuration
.github/workflows/           # CI
```

## UI architecture

The UI follows one consistent five-step workflow:

**Upload → Select workflow → Configure → Run → Explore / Export**

The user should never need to know Python function names, GeoPandas internals, NetworkX objects or City2Graph implementation details.

## Workflow registry

The application should maintain a small registry mapping a human-readable workflow to an adapter operation and parameter schema. Example:

```text
KNN → adapter.run_operation(...)
Delaunay → adapter.run_operation(...)
Gabriel → adapter.run_operation(...)
RNG → adapter.run_operation(...)
MST → adapter.run_operation(...)
Radius → adapter.run_operation(...)
Waxman → adapter.run_operation(...)
Queen / Rook → adapter.run_operation(...)
OD Matrix → adapter.run_operation(...)
GTFS → adapter.run_operation(...)
Morphology → adapter.run_operation(...)
```

The registry is UI metadata. It must not contain a second implementation of the scientific algorithms.

## Result contract

Every completed workflow should expose, where available:

- nodes
- edges
- graph statistics
- map preview
- node table
- edge table
- export controls
- reproducibility metadata

The result layer must distinguish between **computed result** and **display representation**.

## Reproducibility metadata

Record at minimum:

- workflow name
- method
- user-selected parameters
- input feature count
- input CRS
- processing time
- result node count
- result edge count
- City2Graph version
- NetGraph Studio version
- UTC timestamp
- source/algorithm attribution

## Deployment boundary

The public application is designed for Streamlit Community Cloud. GitHub Pages is not the runtime target because Streamlit requires a Python execution environment.
