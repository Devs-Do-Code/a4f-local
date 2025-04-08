"""
a4f-local: A unified wrapper for various reverse-engineered AI provider APIs.
"""
__version__ = "0.1.0"

# Import the main client class to make it available directly, e.g., `from a4f_local import A4F`
from .client import A4F

# Optionally, pre-run discovery when the package is imported
# from .providers import _discovery
# _discovery.find_providers() # Ensure registry is populated early

# Define what gets imported with 'from a4f_local import *'
__all__ = ['A4F']
