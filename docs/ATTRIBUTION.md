# Attribution and Upstream Relationship

## NetGraph Studio

NetGraph Studio is an independent interface and orchestration project by **Dr. Narendra Kumar**. Its purpose is to make selected City2Graph workflows accessible to users who do not write Python.

## City2Graph

NetGraph Studio uses the open-source **City2Graph** library as its upstream computational engine. City2Graph is an independent project maintained by its upstream authors and contributors.

Upstream project:

- Repository: https://github.com/c2g-dev/city2graph
- Documentation: https://city2graph.net

The upstream project's own license, copyright notices and citation guidance remain applicable to the City2Graph software.

## Boundary of responsibility

NetGraph Studio does not claim authorship of City2Graph's algorithms or upstream implementation. The NetGraph Studio adapter calls the upstream public API and exposes the returned results through a non-coder interface.

NetGraph Studio is **not an official City2Graph product** and should not be presented as endorsed by, maintained by, or affiliated with the City2Graph maintainers unless explicit permission or an official relationship exists.

## How to cite NetGraph Studio

Use the repository citation metadata provided by NetGraph Studio for the specific release being used. When publishing results produced through NetGraph Studio, also acknowledge City2Graph as the upstream computational library and follow its current citation guidance.

## License separation

- NetGraph Studio source code: MIT License, copyright Dr. Narendra Kumar, 2026.
- City2Graph: distributed under its upstream BSD-3-Clause license.
- Other dependencies: remain under their respective licenses.

A dependency's license does not become the license of NetGraph Studio source code, and NetGraph Studio's MIT license does not replace an upstream dependency's license.
