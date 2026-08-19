"""Regression tests for research reproducibility records."""

from netgraph.report import build_record, json_bytes


def test_build_record_contains_reproducibility_fields():
    record = build_record(
        operation="knn",
        mode="Simple",
        parameters={"k": 2},
        input_features=5,
        input_crs="EPSG:4326",
        nodes=5,
        edges=8,
        processing_seconds=0.123456789,
    )
    assert record["application"] == "NetGraph Studio"
    assert record["operation"] == "knn"
    assert record["parameters"] == {"k": 2}
    assert record["input_features"] == 5
    assert record["input_crs"] == "EPSG:4326"
    assert record["result_nodes"] == 5
    assert record["result_edges"] == 8
    assert record["processing_seconds"] == 0.123457
    assert record["timestamp_utc"]
    assert record["city2graph_version"]
    assert record["algorithm_source"] == "Original City2Graph public API"


def test_json_bytes_is_valid_utf8_json():
    data = json_bytes({"operation": "knn", "nodes": 5})
    assert data.startswith(b"{")
    assert b'"operation": "knn"' in data
