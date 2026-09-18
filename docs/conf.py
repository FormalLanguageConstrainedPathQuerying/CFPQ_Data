# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from datetime import date

_REPO_ROOT = os.path.abspath("..")
sys.path.insert(0, _REPO_ROOT)

# nb2plots executes notebook cells in a separate Jupyter kernel process that
# does not inherit the sys.path modification above. Expose the repository root
# via PYTHONPATH so the kernel imports cfpq_data from this checkout instead of
# a (possibly stale) copy installed in site-packages.
_existing_pythonpath = os.environ.get("PYTHONPATH")
os.environ["PYTHONPATH"] = (
    _REPO_ROOT + os.pathsep + _existing_pythonpath
    if _existing_pythonpath
    else _REPO_ROOT
)

# -- Project information -----------------------------------------------------

project = "CFPQ_Data"
copyright = f"2019-{date.today().year}, vdshk"
author = "vdshk"

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The short X.Y version
import cfpq_data

version = cfpq_data.__version__
# The full version, including alpha/beta/rc tags
release = cfpq_data.__version__.replace("_", "")

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.autosummary",
    "sphinx_copybutton",
    "numpydoc",
    "nb2plots",
    "texext",
]

# generate autosummary pages
autosummary_generate = True

# The default options for autodoc directives.
# They are applied to all autodoc directives automatically.
# It must be a dictionary which maps option names to the values.
# Setting None or True to the value is equivalent to giving only the option
# name to the directives.
autodoc_default_options = {
    "members": True,
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Treat every unresolved cross-reference (:obj:, :ref:, :doc:, intersphinx)
# as a warning instead of silently emitting a broken link.
nitpicky = True

# linkcheck: treat 401 responses as working (auth-required pages exist).
linkcheck_allow_unauthorized = True

# linkcheck: identify with a descriptive User-Agent. Wikipedia answers 403
# ("Too many requests") to generic client UAs from some networks while the
# pages remain valid; their robot policy asks for a descriptive UA.
linkcheck_user_agent = (
    "CFPQ_Data-docs-linkcheck "
    "(https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data)"
)

# linkcheck: skip exactly these two hosts. Both answer 403 to datacenter
# clients (verified 2026-09: a browser User-Agent still gets 403, so the
# blocking is IP-based) while the pages remain valid for human readers —
# dl.acm.org hosts cited papers, dacapobench.sourceforge.net is the source
# of the avrora graph. Re-verify with a residential connection before
# removing an entry; every other URL is checked in full.
linkcheck_ignore = [
    r"https?://dl\.acm\.org/.*",
    r"https?://dacapobench\.sourceforge\.net.*",
]

# linkcheck: check URLs sequentially. Wikipedia rate-limits parallel requests
# from datacenter IPs with 403 ("Too many requests") even for a descriptive
# User-Agent, while sequential requests pass (verified 2026-09); the default
# worker pool makes the check flaky on such networks. Every URL is still
# checked in full — this only changes the concurrency.
linkcheck_workers = 1

# linkcheck: retry broken results. Wikipedia's rate limit can outlast a
# single attempt even for sequential requests (verified 2026-09-18: one URL
# answered 403 to every attempt of a run while identical direct requests
# passed); the session-level retries above add backoff between attempts, and
# this adds outer attempts on top. A genuinely broken link still fails after
# all retries.
linkcheck_retries = 5

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = {
#     '.rst': 'restructuredtext',
#     '.txt': 'markdown',
#     '.md': 'markdown',
# }
source_suffix = ".rst"

# The encoding of source files.
source_encoding = "utf-8"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "borland"

# A list of prefixes that are ignored when creating the module index.
# (new in Sphinx 0.6)
modindex_common_prefix = ["cfpq_data."]

doctest_global_setup = "import cfpq_data"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "collapse_navigation": True,
    # 3 levels: section (Dataset) -> category (C alias analysis) -> graph page.
    # With the Dataset wrapper section, graph pages sit one level deeper than
    # before; depth 3 keeps them directly reachable in the sidebar.
    "navigation_depth": 3,
    "show_prev_next": False,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/FormalLanguageConstrainedPathQuerying/CFPQ_Data",
            "icon": "fab fa-github",
        },
        {
            "name": "PyPI",
            "url": "https://pypi.org/project/cfpq-data/",
            "icon": "fas fa-box",
        },
    ],
    "navbar_end": ["navbar-icon-links"],
}

html_logo = "_static/img/CFPQDataLogo.svg"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"

# Custom css files
# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
html_css_files = [
    "css/copybutton.css",
    "css/about.css",
    "css/custom.css",
]

# Every page (including the homepage) renders the same left sidebar: the
# section links plus the active section's toctree. No per-page exceptions.
html_sidebars = {
    "**": ["sidebar-nav-bs"],
}

# If true, the reST sources are included in the HTML build as _sources/<name>.
html_copy_source = False

html_use_opensearch = (
    "https://formallanguageconstrainedpathquerying.github.io/CFPQ_Data/"
)


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "CFPQ_Data"

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "cfpq_data", "CFPQ_Data Documentation", [author], 1)]

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "networkx": ("https://networkx.org/documentation/stable/", None),
    "pyformlang": ("https://pyformlang.readthedocs.io/en/latest/", None),
}

# CI runners occasionally drop outbound connections mid-fetch (2026-09-16:
# networkx.org reset the connection, leaving every networkx cross-reference
# unresolved and failing the build under the no-warnings policy). Retry
# transient connection errors; when all attempts fail, the error propagates
# and the build still fails.
import time as _time
from typing import Any

from requests import Response
from requests.exceptions import ConnectionError as _RequestsConnectionError
from requests.exceptions import Timeout as _RequestsTimeout
from sphinx.util import requests as _sphinx_requests

_orig_intersphinx_get = _sphinx_requests.get


_RETRY_COUNT = 3
_RETRY_BACKOFF = 2.0


def _get_with_retries(url: str, **kwargs: Any) -> Response:
    attempt = 0
    while True:
        try:
            return _orig_intersphinx_get(url, **kwargs)
        except (_RequestsConnectionError, _RequestsTimeout):
            if attempt == _RETRY_COUNT:
                raise
            attempt += 1
            _time.sleep(_RETRY_BACKOFF * attempt)


# ty rejects this signature-identical rebind of a module attribute (pyright
# accepts it), so the assignment is suppressed for it.
_sphinx_requests.get = _get_with_retries  # type: ignore

# linkcheck: Wikipedia rate-limits datacenter IPs with transient 403s even
# for sequential requests (verified 2026-09-18: en.wikipedia.org answered
# 403 to the link check while the same URL answered 200 to a direct request
# moments later). Retry transient failures inside the session — the path
# both linkcheck and intersphinx go through — so one rate-limited response
# does not fail the whole check; a persistent block still reports broken
# after the retries are exhausted.
_orig_session_request = _sphinx_requests._Session.request


def _session_request_with_retries(
    self: Any, method: str, url: str, **kwargs: Any
) -> Response:
    attempt = 0
    while True:
        try:
            response = _orig_session_request(self, method, url, **kwargs)
        except (_RequestsConnectionError, _RequestsTimeout):
            if attempt == _RETRY_COUNT:
                raise
            attempt += 1
            _time.sleep(_RETRY_BACKOFF * attempt)
            continue
        if response.status_code in (403, 429) and attempt < _RETRY_COUNT:
            attempt += 1
            _time.sleep(_RETRY_BACKOFF * attempt)
            continue
        return response


_sphinx_requests._Session.request = _session_request_with_retries  # type: ignore

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = "obj"

# -- Options for numpydoc extension ------------------------------------------

numpydoc_show_class_members = False
