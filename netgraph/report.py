"""Reproducibility and research-record utilities."""

from __future__ import annotations

from datetime import datetime, timezone
import json

import city2graph


def build_record(*, operation: str, mode: str, parameters: dict, input_features: int,
                 input_crs: str | None, nodes: int, edges: int,
                 processing_seconds: float) -> dict:
    """Build a serializable analysis record without changing computation."""
    return {
        "application": "NetGraph Studio",
        "mode": mode,
        "operation": operation,
        "parameters": parameters,
        "input_features": input_features,
        "input_crs": input_crs,
        "result_nodes": nodes,
        "result_edges": edges,
        "processing_seconds": round(processing_seconds, 6),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "city2graph_version": getattr(city2graph, "__version__", "unknown"),
        "algorithm_source": "Original City2Graph public API",
        "output_fidelity_policy": "No silent algorithm, parameter, CRS, geometry, node, or edge changes.",
    }


def json_bytes(record: dict) -> bytes:
    """Serialize a research record as UTF-8 JSON."""
    return json.dumps(record, indent=2, default=str).encode("utf-8")
