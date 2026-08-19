"""App-level smoke tests that avoid starting a browser/server."""

from pathlib import Path


def test_streamlit_entrypoint_exists():
    candidates = [Path("app.py"), Path("streamlit_app.py"), Path("main.py")]
    assert any(path.exists() for path in candidates), "No Streamlit entrypoint found"


def test_project_metadata_exists():
    assert Path("requirements.txt").exists()
    assert Path("README.md").exists()
