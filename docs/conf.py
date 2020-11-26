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
copyright = '2020, Nebulon, Inc.'
author = 'Tobias Flitsch'

# The version and full version including alpha/beta/rc tags
version = "1.0"
release = '1.0rc1'

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

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'xcode'

# The master toctree document.
master_doc = 'index'

# -- Options for autodoc -----------------------------------------------------

autodoc_default_options = {}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'default'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'NebPyClientDoc'

# -- Options for LaTeX output ------------------------------------------------

latex_engine = 'xelatex'
latex_elements = {
    'fontpkg': r'''
\setmainfont{Open Sans}
\setsansfont{Open Sans}
'''
}
latex_show_urls = 'footnote'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
    (
        'index',
        'NebPyClient.tex',
        'Nebulon Python SDK documentation',
        'Nebulon',
        'manual'
    ),
]
