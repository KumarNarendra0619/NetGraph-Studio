# NetGraph Studio — Debug Status

## Scope
NetGraph Studio is a thin, non-coder-friendly UI layer over the original City2Graph public API. Graph construction must remain delegated to City2Graph.

## Implemented regression coverage

- Core imports and module startup checks
- Dependency manifest sanity check
- Streamlit entrypoint/metadata smoke checks
- Input geometry/CRS validation
- Parameter validation
- KNN fidelity against direct City2Graph execution
- Delaunay fidelity
- Gabriel fidelity
- Relative Neighbourhood Graph fidelity
- Euclidean MST fidelity
- Fixed-radius fidelity
- Waxman fidelity with deterministic seed
- Queen/Rook contiguity fidelity
- Export regression checks
- Research reproducibility record checks

## Runtime truth
The repository CI workflow runs `pytest -q` on pushes and pull requests and supports manual dispatch. A green status must come from GitHub Actions; source inspection alone is not considered a PASS.

## Debugging rule
For every graph operation:

`same input + same parameters -> City2Graph direct result == NetGraph Studio result`

The adapter may validate inputs and translate UI parameters, but must not reimplement City2Graph graph construction.
