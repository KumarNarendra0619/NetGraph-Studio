# Methodology and Scientific Scope

## Software role

NetGraph Studio is an interface and integration layer. It does not claim to introduce new graph-construction algorithms. The computational behavior is inherited from the supported City2Graph public APIs.

## Workflow pattern

```text
Input data
  → validation
  → workflow selection
  → parameter selection
  → City2Graph execution
  → result inspection
  → export / reproducibility record
```

## Method families

### Proximity

Supported workflows include KNN, Delaunay, Gabriel, Relative Neighbourhood, Euclidean Minimum Spanning Tree, Fixed Radius, and Waxman through the City2Graph proximity interface.

### Contiguity

Queen and Rook polygon adjacency workflows are exposed through the upstream contiguity interface.

### Urban morphology

Building/place and movement/street graph workflows are exposed through the upstream morphology interface. Heterogeneous graph semantics should be preserved.

### Mobility / OD

OD edge-list and adjacency-matrix workflows are exposed through the upstream OD interface, including relevant threshold, self-loop, geometry, and directedness controls where supported.

### Transportation / GTFS

GTFS processing is delegated to the upstream transportation API rather than reconstructed in the application.

## Validation philosophy

A NetGraph Studio result should be considered scientifically equivalent to the corresponding direct City2Graph call only when the relevant fidelity test passes for the same input and parameters.

Source-code inspection is not sufficient evidence of runtime equivalence.

## Limitations

- Runtime equivalence depends on the installed and pinned City2Graph version.
- Large datasets may be constrained by the deployment environment.
- Optional PyTorch/PyG functionality is not part of the minimal installation.
- A green CI run is required before declaring a build runtime-validated.
