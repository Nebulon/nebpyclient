# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
source_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..'
    )
)
sys.path.insert(0, source_dir)

# -- Project information -----------------------------------------------------

project = 'Nebulon Python SDK'
copyright = '2021, Nebulon, Inc.'
author = 'Tobias Flitsch'

# The version and full version including alpha/beta/rc tags
with open(os.path.join(source_dir, "nebpyclient/VERSION"), "r") as fh:
    version_parts = fh.read().strip().split(".")
    version = version_parts[0] + "." + version_parts[1]
    release = ".".join(version_parts)

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store'
]

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# -- Options for autodoc -----------------------------------------------------

autodoc_default_options = {
    'autodoc_typehints': 'description'
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages. See the documentation for
# a list of builtin themes.
#
html_theme = 'default'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'NebPyClientDoc'


def clean_method(app, what, name, obj, options, signature, return_annotation):
    if what == 'method':
        tmp = signature.replace("<class '", "").replace("'>", "")
        return tmp, return_annotation
    return signature, return_annotation


def setup(app):
    app.connect('autodoc-process-signature', clean_method)
