# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
# Point to the project root to find the package
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'a4f-local'
copyright = '2025, DevsDoCode' # Updated copyright holder
author = 'DevsDoCode' # Updated author

# Attempt to get the version from the package __init__
try:
    from a4f_local import __version__ as release
except ImportError:
    release = '0.1.0' # Fallback version

version = '.'.join(release.split('.')[:2]) # Short X.Y version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc', # Include documentation from docstrings
    'sphinx.ext.napoleon', # Support NumPy and Google style docstrings
    'sphinx.ext.intersphinx', # Link to other projects' documentation
    'sphinx.ext.viewcode', # Add links to source code
    'sphinx_rtd_theme', # Use the Read the Docs theme
    # Add other extensions here if needed
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Intersphinx mapping allows linking to other documentation
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# Autodoc settings
autodoc_member_order = 'bysource' # Keep source order for members

# Napoleon settings (if using Google/NumPy style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options are theme-specific
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
