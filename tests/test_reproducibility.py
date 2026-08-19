"""Reproducibility record regression tests."""

import json

from netgraph.report import build_record, json_bytes


def test_research_record_contains_required_metadata():
    record = build_record(
        operation="KNN",
        mode="Research",
        parameters={"k": 5},
        input_features=10,
        input_crs="EPSG:4326",
        nodes=10,
        edges=20,
        processing_seconds=1.2345678,
    )

    required = {
        "application",
        "mode",
        "operation",
        "parameters",
        "input_features",
        "input_crs",
        "result_nodes",
        "result_edges",
        "processing_seconds",
        "timestamp_utc",
        "city2graph_version",
        "algorithm_source",
        "output_fidelity_policy",
    }
    assert required.issubset(record)
    assert record["application"] == "NetGraph Studio"
    assert record["operation"] == "KNN"
    assert record["parameters"] == {"k": 5}
    assert record["input_features"] == 10
    assert record["input_crs"] == "EPSG:4326"
    assert record["result_nodes"] == 10
    assert record["result_edges"] == 20
    assert record["processing_seconds"] == 1.234568
    assert record["algorithm_source"] == "Original City2Graph public API"


def test_research_record_is_valid_utf8_json():
    record = build_record(
        operation="Queen",
        mode="Research",
        parameters={"contiguity": "queen"},
        input_features=4,
        input_crs="EPSG:4326",
        nodes=4,
        edges=5,
        processing_seconds=0.5,
    )
    payload = json_bytes(record)
    restored = json.loads(payload.decode("utf-8"))
    assert restored["operation"] == "Queen"
    assert restored["parameters"]["contiguity"] == "queen"
