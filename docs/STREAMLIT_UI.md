# Streamlit UI Architecture

## Design objective

NetGraph Studio must let a non-programmer run City2Graph workflows without writing Python while keeping the scientific computation unchanged.

## Global layout

```text
┌─────────────────────────────────────────────────────────────┐
│ NetGraph Studio                                  Help | QA │
├─────────────────────────────────────────────────────────────┤
│ 1. DATA                                                     │
│    Upload vector data                                      │
│    [Upload GeoJSON / GeoPackage / Shapefile]               │
│    CRS • feature count • geometry type • validation status  │
├─────────────────────────────────────────────────────────────┤
│ 2. WORKFLOW                                                 │
│    [Choose analysis ▼]                                     │
│    Proximity | Contiguity | OD | Morphology | GTFS         │
├─────────────────────────────────────────────────────────────┤
│ 3. PARAMETERS                                               │
│    Context-sensitive controls only                          │
│    [parameter] [value ▼]                                    │
│    Scientific explanation / units / valid range             │
├─────────────────────────────────────────────────────────────┤
│                     [ RUN ANALYSIS ]                        │
├─────────────────────────────────────────────────────────────┤
│ 4. RESULT                                                   │
│    Summary | Map | Nodes | Edges | Diagnostics              │
│    [Export] [Research Record]                               │
└─────────────────────────────────────────────────────────────┘
```

## UX rules

### 1. Progressive disclosure

Show only parameters relevant to the selected workflow. Advanced parameters stay behind an **Advanced options** expander.

### 2. Human-readable labels

Use labels such as `Number of neighbours (k)` instead of `k`, `Network layer` instead of an internal variable name, and `Distance method` instead of an API argument name.

### 3. No hidden scientific defaults

Every default that affects computation must be visible or documented. The UI must not silently alter a user-selected parameter.

### 4. Validation before execution

Display clear errors before calling City2Graph when input geometry, CRS, required fields or network requirements are invalid.

### 5. Result-first presentation

After execution, show the scientific result before technical metadata. Technical details remain available under **Diagnostics** and **Research Record**.

## Main controls

### Data panel

- Upload file
- Layer selector where applicable
- Geometry type
- CRS
- Feature count
- Required-field selector
- Network weight field when required

### Workflow selector

Grouped categories:

- **Proximity:** KNN, Delaunay, Gabriel, Relative Neighbourhood, MST, Radius, Waxman
- **Contiguity:** Queen, Rook
- **Mobility:** OD Matrix
- **Urban morphology:** morphology workflow
- **Transportation:** GTFS
- **Graph ML boundary:** PyG conversion where optional dependencies are installed

### Run panel

The primary button should be explicit: **Run analysis**. During execution show a progress state and disable duplicate submissions.

## Result tabs

### Summary

- workflow
- method
- input features
- nodes
- edges
- connected components
- average degree where applicable
- processing time

### Map

Use a display copy for projection or rendering transformations. Never mutate the computational source objects.

### Nodes / Edges

Provide searchable, paginated tables with download controls.

### Diagnostics

Show validation messages, warnings, CRS information, dependency information and upstream version.

### Research Record

Offer a JSON record containing method, parameters, versions, timestamp and result summary.

## Export panel

Offer only formats supported by the result type:

- GeoJSON
- CSV
- GraphML
- GML
- edge list
- reproducibility JSON

## Error design

Errors must answer three questions:

1. What is wrong?
2. Why is it required?
3. What should the user change?

Avoid exposing raw Python tracebacks in the normal user path. A technical traceback may be available under Diagnostics for debugging.

## Accessibility and simplicity

- Avoid dense control panels.
- Keep one primary action visible.
- Use consistent terminology across workflows.
- Explain units beside numeric inputs.
- Do not require knowledge of NetworkX, GeoPandas or Python.
- Preserve keyboard-accessible Streamlit controls.

## Suggested implementation modules

```text
app.py
netgraph/ui/
├── __init__.py
├── layout.py
├── workflow_registry.py
├── input_panel.py
├── parameter_panel.py
├── run_panel.py
├── result_panel.py
├── export_panel.py
└── messages.py
```

These UI modules must call the adapter layer. They must never import private City2Graph internals to perform graph construction.
