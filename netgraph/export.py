"""Research-safe export helpers."""

from __future__ import annotations

import io
import networkx as nx


def graphml_bytes(graph: nx.Graph) -> bytes:
    """Export a NetworkX graph as GraphML bytes."""
    text = io.BytesIO()
    nx.write_graphml(graph, text)
    return text.getvalue()


def gml_bytes(graph: nx.Graph) -> bytes:
    """Export a NetworkX graph as GML bytes."""
    text = io.BytesIO()
    nx.write_gml(graph, text)
    return text.getvalue()


def edge_list_bytes(graph: nx.Graph) -> bytes:
    """Export a graph edge list as UTF-8 bytes."""
    return "\n".join(f"{u} {v}" for u, v in graph.edges()).encode("utf-8")


def pyg_bytes(data) -> bytes:
    """Serialize a PyTorch/PyG object when optional dependencies are installed."""
    import torch
    buffer = io.BytesIO()
    torch.save(data, buffer)
    return buffer.getvalue()
