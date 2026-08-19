# NetGraph Studio — Research Workbench Architecture

## Product boundary

NetGraph Studio is not a replacement implementation of City2Graph. It is a no-code research orchestration and evidence layer around the original City2Graph computational API.

**Core rule:** UI validation, provenance, visualization and export may be extended; City2Graph graph-construction mathematics and defaults must not be silently rewritten.

## Research workflow

`Data → QC → Graph Design → Construction → Validation → Analysis → Robustness → Visualization → Reproducibility → Evidence Package`

### 1. Data
Supported workflows can ingest spatial layers and specialized inputs through the existing adapters.

### 2. QC
Before graph construction, report feature count, CRS, geometry types, invalid/empty/missing geometries, duplicates and missing values. The Workbench does not silently repair scientific inputs.

### 3. Graph Design
Expose the method and its parameters explicitly. Examples include KNN, fixed radius, Waxman and Queen/Rook contiguity.

### 4. Construction
Delegate to the existing `netgraph.adapter` / City2Graph calls.

### 5. Validation
Report nodes, edges, components, isolates, density, mean degree and related structural evidence.

### 6. Robustness / sensitivity
Allow an explicit user-defined parameter grid. Each run is independent and recorded; there are no hidden parameter substitutions.

### 7. Reproducibility
Record software, engine, operation, parameters, CRS, input SHA-256, timestamp and graph metrics.

### 8. Evidence package
Provide method records and machine-readable statistics suitable for later manuscript preparation. The software must not fabricate statistical interpretation or unsupported research claims.

## UI modes

- **Simple:** minimal upload → method → parameters → run → result path.
- **Research:** QC, method transparency, validation, sensitivity, evidence and reproducibility.
- **Expert:** future home for multi-layer/heterogeneous graphs and ML/GNN controls.

## Future modules

The architecture intentionally leaves explicit extension points for:

- statistical analysis
- centrality and accessibility analysis
- method comparison
- multi-method benchmarking
- paper-ready figure generation
- citation metadata
- GNN/PyG workflows
- richer reproducibility bundles

These must be implemented as downstream analytical/reporting layers and must not alter the City2Graph construction boundary.
