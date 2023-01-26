# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "h-transport-materials"
copyright = "2023, Remi Delaporte-Mathurin, James Dark, Thomas Fuerst"
author = "Remi Delaporte-Mathurin, James Dark, Thomas Fuerst"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_design"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = ["_static"]
html_css_files = ["style.css"]

html_theme_options = {
    "repository_url": "https://github.com/RemDelaporteMathurin/h-transport-materials",
    "use_repository_button": True,
}

html_title = "H-transport-materials"
