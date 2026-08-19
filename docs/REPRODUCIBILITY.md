# Reproducibility Guide

NetGraph Studio is designed to make graph-analysis workflows reproducible for users who do not program in Python.

## Minimum research record

Record:

- input dataset and source;
- workflow;
- algorithm/method;
- all user-selected parameters;
- input CRS;
- feature count;
- City2Graph version;
- NetGraph Studio version/commit;
- processing timestamp;
- output node and edge counts;
- exported result files.

## Recommended practice

1. Keep the original input data unchanged.
2. Record the exact parameters used.
3. Preserve the research/reproducibility JSON produced by the application.
4. Preserve the exported graph and tabular outputs.
5. Cite NetGraph Studio and City2Graph where required.
6. Report software versions in research methods or supplementary material.

## Fidelity principle

For a workflow implemented through City2Graph, compare NetGraph Studio output against a direct City2Graph execution using identical input, CRS, parameters, and software version when scientific equivalence is being evaluated.
