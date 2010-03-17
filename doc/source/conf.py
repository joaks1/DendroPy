# -*- coding: utf-8 -*-
#
# DendroPy documentation build configuration file, created by
# sphinx-quickstart on Wed Oct 21 18:04:56 2009.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys, os
from dendropy import __version__ as PROJECT_VERSION

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.append(os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.doctest',
              'sphinx.ext.intersphinx',
              'sphinx.ext.coverage',
              'sphinx.ext.pngmath',
              'sphinx.ext.ifconfig']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'DendroPy'
copyright = u'2009, Jeet Sukumaran and Mark T. Holder'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = PROJECT_VERSION
# The full version, including alpha/beta/rc tags.
release = PROJECT_VERSION

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = ['tutorial/whatsnew']

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = []

# The reST default role (used for this markup: `text`) to use for all documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

rst_epilog = """
.. |js| replace:: Jeet Sukumaran
.. _js: http://www.jeetworks.org/about
.. |mth| replace:: Mark T. Holder
.. _mth: http://people.ku.edu/~mtholder

.. |DendroPy| replace:: DendroPy
.. _DendroPy: http://packages.python.org/DendroPy/
.. |dendropy_homepage_url| replace:: http://packages.python.org/DendroPy/
.. |dendropy_tutorial_url| replace:: http://packages.python.org/DendroPy/tutorial/index.html
.. |dendropy_library_url| replace:: http://packages.python.org/DendroPy/library/index.html
.. |dendropy_download_url| replace:: http://pypi.python.org/pypi/DendroPy
.. |dendropy_public_repo_url| replace:: http://github.com/jeetsukumaran/DendroPy

.. |Python| replace:: Python
.. _Python: http://www.python.org/
.. |Python26| replace:: Python 2.6
.. _Python 2.6: http://www.python.org/download/releases/2.6/
.. |setuptools| replace:: setuptools
.. _setuptools: http://pypi.python.org/pypi/setuptools
.. |Git| replace:: Git
.. _Git: http://git-scm.com/

.. |dendropy_logo| replace:: /_static/dendropy.png
.. |dendropy_library_doc| replace:: /library/index
.. |dendropy_tutorial_doc| replace:: /tutorial/index
.. |sumtrees_doc| replace:: /scripts/sumtrees

.. |sumtrees_citation| replace:: Sukumaran, J. and Mark T. Holder. 2009. *SumTrees: Summarization of Split Support on Phylogenetic Trees. Version 1.0.2*. Part of the *DendroPy Phylogenetic Computation Library Version 2.6.1* (|dendropy_homepage_url|).
.. |dendropy_citation| replace:: Sukumaran, J. and Mark T. Holder. 2009. *DendroPy Phylogenetic Computing Library Version 3.0.0* (|dendropy_homepage_url|).
.. |dendropy_copyright| replace:: **Copyright 2009 Jeet Sukumaran and Mark T. Holder**

.. |Tree| replace:: :class:`~dendropy.dataobject.tree.Tree`
.. |TreeList| replace:: :class:`~dendropy.dataobject.tree.TreeList`
.. |Node| replace:: :class:`~dendropy.dataobject.tree.Node`
.. |Edge| replace:: :class:`~dendropy.dataobject.tree.Edge`
.. |Taxon| replace:: :class:`~dendropy.dataobject.taxon.Taxon`
.. |TaxonSet| replace:: :class:`~dendropy.dataobject.taxon.TaxonSet`
.. |DataSet| replace:: :class:`~dendropy.dataobject.dataset.DataSet`
.. |CharacterMatrix| replace:: :class:`~dendropy.dataobject.char.CharacterMatrix`
.. |DnaCharacterMatrix| replace:: :class:`~dendropy.dataobject.char.DnaCharacterMatrix`
.. |RnaCharacterMatrix| replace:: :class:`~dendropy.dataobject.char.RnaCharacterMatrix`
.. |ProteinCharacterMatrix| replace:: :class:`~dendropy.dataobject.char.ProteinCharacterMatrix`
.. |StandardCharacterMatrix| replace:: :class:`~dendropy.dataobject.char.StandardCharacterMatrix`
.. |ContinuousCharacterMatrix| replace:: :class:`~dendropy.dataobject.char.ContinuousCharacterMatrix`
.. |CharacterDataVector| replace:: :class:`~dendropy.dataobject.char.CharacterDataVector`
.. |CharacterDataCell| replace:: :class:`~dendropy.dataobject.char.CharacterDataCell`
"""

_source_archive_url = """
.. |source_archive_url| replace:: http://pypi.python.org/packages/source/D/DendroPy/DendroPy-%s.tar.gz
""" % version

rst_epilog += _source_archive_url

# -- Options for HTML output ---------------------------------------------------

if False:

    # The theme to use for HTML and HTML Help pages.  Major themes that come with
    # Sphinx are currently 'default' and 'sphinxdoc'.
    html_theme = 'sphinxdoc'

else:
    html_theme = 'default'

    # Theme options are theme-specific and customize the look and feel of a theme
    # further.  For a list of options available for each theme, see the
    # documentation.
    # orange =CB9832  green = 81916A,
#    html_theme_options = {
#
#        #'bodyfont': '#000000',
#        #'headfont': '#000000',
#
#        'relbarbgcolor': '#343430', #'#',
#        'relbartextcolor': '#ffffff',
#        'relbarlinkcolor': '#fff000',
#
#        'sidebarbgcolor': '#404040',
#        'sidebartextcolor': '#ffffff',
#        'sidebarlinkcolor': '#CB9832',
#
#        'bgcolor': '#eeeedd',
#        'textcolor': '#000000',
#        'linkcolor': '#0000ff',
#
#        'headbgcolor': '#ccccbb',
#        'headtextcolor': '#006600',
#        'headlinkcolor': '#fff000',
#
#        'codebgcolor': '#ffffff',
#        'codetextcolor': '#000000',
#
#        'footerbgcolor': '#000000',
#        'footertextcolor': '#ffffff',
#
#    }

#html_style = "dendropy.css"

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = project + " Phylogenetic Computing Library v" + version

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = project +" v" + version

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/dendropy.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_use_modindex = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = 'DendroPydoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'DendroPy.tex', u'DendroPy Documentation',
   u'Jeet Sukumaran and Mark T. Holder', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'http://docs.python.org/': None}
