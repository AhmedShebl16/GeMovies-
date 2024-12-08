# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project Setup -----------------------------------------------------

import os
import sys
import django

sys.path.insert(0, os.path.abspath('..'))
sys.path.append(os.curdir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GeMovies'
copyright = '2025, GeMovies-Inc'
author = 'GeMovies-Inc'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.githubpages',
    'sphinxcontrib.openapi',
    'ext.hocks'
]

templates_path = ['_templates']
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '*/migrations/*',
    '*/wsgi.py',
    '*/asgi.py',
    '*/__init__.py'
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['static']
html_favicon = 'static/images/logo_circle.png'
