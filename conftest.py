"""Root-level pytest configuration.

Ensures the repository root is on sys.path so the local ``netgraph``
package can be imported during test collection, even when the package
is not installed (e.g. via ``pip install -e .``).
"""
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
