# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'ExpenseDocAI'
copyright = '2024, DocMatrixAI'
author = 'DocMatrixAI'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
    'sphinxcontrib.httpdomain',
    'sphinxcontrib.openapi',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'

# -- Extension configuration ------------------------------------------------
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_class_signature = 'separated'

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Intersphinx settings
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'django': ('https://docs.djangoproject.com/en/stable/', 'https://docs.djangoproject.com/en/stable/_objects/'),
    'drf': ('https://www.django-rest-framework.org/', None),
}

# HTTP domain settings
http_index_shortname = 'api'
http_index_localname = 'ExpenseDocAI REST API'

# OpenAPI settings
openapi_spec_path = '../openapi.yaml'

# -- Custom configuration --------------------------------------------------
rst_epilog = '''
.. |project| replace:: ExpenseDocAI
.. |version| replace:: 1.0.0
.. |api_version| replace:: v1
.. |base_url| replace:: https://api.expensedocai.com/api/v1/
'''

# -- HTML theme options ---------------------------------------------------
html_theme_options = {
    'analytics_id': 'G-XXXXXXXXXX',  # Google Analytics
    'analytics_anonymize_ip': False,
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# -- Options for linkcheck builder ----------------------------------------
linkcheck_ignore = [
    r'http://localhost:\d+/',
    r'http://example\.com/.*',
    r'https://your-server\.com/.*',
]
linkcheck_timeout = 15
linkcheck_retries = 3
linkcheck_workers = 10

# -- Options for PDF output ----------------------------------------------
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': '',
    'figure_align': 'htbp'
}

# -- Options for manual page output --------------------------------------
man_pages = [
    ('index', 'expensedocai', 'ExpenseDocAI Documentation',
     [author], 1)
]

# -- Options for Texinfo output -----------------------------------------
texinfo_documents = [
    ('index', 'ExpenseDocAI', 'ExpenseDocAI Documentation',
     author, 'ExpenseDocAI', 'Intelligent Expense Document Processing.',
     'Miscellaneous'),
] 