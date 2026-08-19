# Contributing to NetGraph Studio

Thank you for contributing to NetGraph Studio.

## Scientific principle

NetGraph Studio is an interface and integration layer. Graph construction should remain delegated to the supported City2Graph public API unless a change is explicitly designed and documented otherwise.

## Before submitting a change

1. Explain the scientific or usability motivation.
2. Keep input semantics and parameter meaning explicit.
3. Preserve reproducibility metadata.
4. Add or update tests for changed behavior.
5. Run the test suite locally when possible.
6. Document breaking changes in `CHANGELOG.md`.

## Pull requests

Pull requests should describe:

- the problem addressed;
- affected workflow(s);
- changes to City2Graph integration, if any;
- validation performed;
- expected effect on outputs;
- any limitations that remain.

Do not claim scientific equivalence without a direct fidelity or regression test.
