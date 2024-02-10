import hyperfocus


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "hyperfocus"
copyright = '2024, <a href="https://u8slvn.github.io/" target="_blank">u8slvn</a>'
author = "u8slvn"
version = hyperfocus.__version__
release = hyperfocus.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
]

source_suffix = ".rst"
templates_path = ["_templates"]
exclude_patterns = []
master_doc = "index"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_theme_options = {
    "show_powered_by": False,
    "github_user": "u8slvn",
    "github_repo": "hyperfocus",
    "show_related": False,
    "note_bg": "#FFF59C",
}

html_static_path = ["_static"]

html_sidebars = {
    "index": [
        "logo.html",
        "sidebar.html",
        "searchbox.html",
    ],
    "**": [
        "logo.html",
        "sidebar.html",
        "localtoc.html",
        "relations.html",
        "searchbox.html",
    ],
}

html_show_copyright = True
html_show_sourcelink = False
