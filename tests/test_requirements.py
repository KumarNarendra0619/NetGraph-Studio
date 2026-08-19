"""Dependency manifest sanity checks."""

from pathlib import Path


def test_required_dependencies_are_declared():
    text = Path("requirements.txt").read_text(encoding="utf-8").lower()
    for package in ["city2graph", "geopandas", "networkx", "streamlit"]:
        assert package in text
