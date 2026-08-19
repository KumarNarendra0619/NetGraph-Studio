"""Basic import/startup regression tests."""


def test_core_imports():
    import city2graph
    import geopandas
    import networkx
    import streamlit

    assert city2graph is not None
    assert geopandas is not None
    assert networkx is not None
    assert streamlit is not None


def test_netgraph_modules_import():
    import netgraph.adapter
    import netgraph.advanced
    import netgraph.export
    import netgraph.report

    assert netgraph.adapter.OPERATIONS
