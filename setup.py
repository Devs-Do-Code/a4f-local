# setup.py shim
# Allows editable installs and provides compatibility for older tools
# that don't fully support pyproject.toml.
# Configuration should primarily live in pyproject.toml.

from setuptools import setup

if __name__ == "__main__":
    setup()
