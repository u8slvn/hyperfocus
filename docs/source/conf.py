import hyperfocus


# -- Project information -----------------------------------------------------

project = "HyperFocus"
copyright = '2024, <a href="https://u8slvn.github.io/" target="_blank">u8slvn</a>'
author = "u8slvn"
version = hyperfocus.__version__
release = hyperfocus.__version__

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
]
source_suffix = ".rst"
templates_path = ["_templates"]
exclude_patterns = []
master_doc = "index"

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"
html_title = "HyperFocus Documentation"
html_static_path = ["_static"]
html_style = "custom.css"
html_theme_options = {
    "show_powered_by": True,
    "github_user": "u8slvn",
    "github_repo": "hyperfocus",
    "show_related": False,
    "note_bg": "#FFF59C",
}
html_sidebars = {
    "index": [
        "sidebar-header.html",
        "navigation.html",
        "searchbox.html",
        "sidebar-project-links.html",
    ],
    "**": [
        "sidebar-logo.html",
        "sidebar-header.html",
        "navigation.html",
        "searchbox.html",
        "sidebar-project-links.html",
    ],
}
html_show_copyright = True
html_show_sourcelink = False
