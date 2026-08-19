"""Smoke-test the Streamlit entrypoint without launching a server."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).resolve().parent.parent / "app.py"


def test_app_starts_without_exception():
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    assert not app.exception
    assert any("NetGraph Studio" in str(title.value) for title in app.title)
