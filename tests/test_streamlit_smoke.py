"""Smoke-test the Streamlit entrypoint without launching a server."""

from streamlit.testing.v1 import AppTest


def test_app_starts_without_exception():
    app = AppTest.from_file("app.py", default_timeout=30).run()
    assert not app.exception
    assert any("NetGraph Studio" in str(title.value) for title in app.title)
