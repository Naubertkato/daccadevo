# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import daccadevo

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'daccadevo'
copyright = '2021-%Y, N. Aubert-Kato'
author = 'N. Aubert-Kato'
release = daccadevo.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'autodoc2',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'myst_parser']

templates_path = ['_templates']
exclude_patterns = ['**/.git']

# -- Options for Autodoc2 extension -------------------------------------------
autodoc2_packages = [
    "../../src/daccadevo",
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
