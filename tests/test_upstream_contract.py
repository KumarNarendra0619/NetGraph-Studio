"""Contract tests against the current City2Graph 1.x public API.

These tests catch upstream signature drift before it reaches the Streamlit UI.
They do not duplicate City2Graph implementation tests.
"""

import inspect

import city2graph
import city2graph.mobility as mobility
import city2graph.proximity as proximity
import city2graph.transportation as transportation


def required_parameters(function, names):
    signature = inspect.signature(function)
    parameters = signature.parameters
    for name in names:
        assert name in parameters, f"{function.__name__} no longer exposes '{name}'"


def test_proximity_public_contract():
    required_parameters(proximity.knn_graph, ["k", "distance_metric", "network_gdf", "network_weight", "as_nx"])
    required_parameters(proximity.fixed_radius_graph, ["radius", "distance_metric", "as_nx"])
    required_parameters(proximity.waxman_graph, ["beta", "r0", "seed", "distance_metric", "as_nx"])
    required_parameters(proximity.contiguity_graph, ["contiguity", "as_nx"])


def test_advanced_public_contract():
    required_parameters(city2graph.morphological_graph, ["buildings_gdf", "segments_gdf", "center_point", "distance", "clipping_buffer", "contiguity", "keep_buildings", "as_nx"])
    required_parameters(mobility.od_matrix_to_graph, ["od_data", "zones_gdf", "zone_id_col", "matrix_type", "source_col", "target_col", "weight_cols", "threshold", "include_self_loops", "compute_edge_geometry", "directed", "as_nx"])
    required_parameters(transportation.travel_summary_graph, ["start_time", "end_time"])


def test_city2graph_version_is_1_x():
    version = getattr(city2graph, "__version__", "")
    assert version.startswith("1."), f"Unexpected City2Graph version: {version!r}"
