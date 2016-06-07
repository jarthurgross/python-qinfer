# -*- coding: utf-8 -*-
#
# QInfer documentation build configuration file, created by
# sphinx-quickstart on Tue Aug 14 21:12:57 2012.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

## MODULE MOCKING ##############################################################

if not tags.has('nomock'):

    # ReadTheDocs doesn't support modules which depend on NumPy, so we must mock
    # them up as suggested by the FAQ:
    # http://read-the-docs.readthedocs.org/en/latest/faq.html#i-get-import-errors-on-libraries-that-depend-on-c-modules
    import sys

    class Mock(object):
        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, *args, **kwargs):
            return Mock()

        @classmethod
        def __getattr__(cls, name):
            if name in ('__file__', '__path__'):
                return '/dev/null'
            elif name[0] == name[0].upper():
                mockType = type(name, (), {})
                mockType.__module__ = __name__
                return mockType
            else:
                return Mock()

    # TODO: replace with RTD build from requirements.txt!
    # MOCK_MODULES = [
    #     'scipy',
    #     'scipy.ndimage',
    #     'scipy.ndimage.filters',
    #     'scipy.linalg',
    #     'scipy.optimize',
    #     'scipy.spatial',
    #     'scipy.special',
    #     'scipy.stats',
    #     'scipy.stats.distributions',
    #     'scipy.interpolate',
    #     'scipy.integrate',
    #     'sklearn',
    #     'sklearn.cluster',
    #     'sklearn.metrics',
    #     'sklearn.metrics.pairwise',
    # ]
    # for mod_name in MOCK_MODULES:
    #     sys.modules[mod_name] = Mock() 

###############################################################################

import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../../src'))

# The LaTeX preamble is placed here so that it can be used both by pngmath
# and by the LaTeX output plugin.
with open('abstract.txt', 'r') as f:
    abstract = f.read()

preamble = r"""
\usepackage{amsfonts}
\usepackage{bbm}
\usepackage[bold]{hhtensor}
\newcommand{\T}{\mathrm{T}}
\newcommand{\Tr}{\mathrm{Tr}}
\newcommand{\ident}{\mathbbm{1}}
\newcommand{\ave}{\mathrm{ave}}

\makeatletter
\renewcommand{\maketitle}{%
  \begin{titlepage}%
    \let\footnotesize\small
    \let\footnoterule\relax
    \rule{\textwidth}{1pt}%
    \ifsphinxpdfoutput
      \begingroup
      % These \defs are required to deal with multi-line authors; it
      % changes \\ to ', ' (comma-space), making it pass muster for
      % generating document info in the PDF file.
      \def\\{, }
      \def\and{and }
      \pdfinfo{
        /Author (\@author)
        /Title (\@title)
      }
      \endgroup
    \fi
    \begin{flushright}%
      \sphinxlogo%
      {\rm\Huge\py@HeaderFamily \@title \par}%
      % {\em\LARGE\py@HeaderFamily \py@release\releaseinfo \par}
      \vfill
      {\LARGE\py@HeaderFamily
        \begin{tabular}[t]{c}
          \@author
        \end{tabular}
        \par}
      \vfill
      {\large
       \@date \par
       \vfill
       \py@authoraddress \par
      }%
      {\bf\sffamily ABSTRACT }

      ABSTRACT_HERE%
      \vfill
    \end{flushright}%\par
    \@thanks
  \end{titlepage}%
  %\cleardoublepage%
  \setcounter{footnote}{0}%
  \let\thanks\relax\let\maketitle\relax
  %\gdef\@thanks{}\gdef\@author{}\gdef\@title{}
}
\makeatother
""".replace("ABSTRACT_HERE", abstract)

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.intersphinx', 'sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.mathjax', 'sphinx.ext.extlinks',
    'matplotlib.sphinxext.only_directives',
    'matplotlib.sphinxext.plot_directive'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'QInfer'
copyright = u'2012, Christopher Ferrie and Christopher Granade'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '1.0'
# The full version, including alpha/beta/rc tags.
release = '1.0b4'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all documents.
default_role = "obj"

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['qinfer']


# -- Options for HTML output ---------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

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
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Output file base name for HTML help builder.
htmlhelp_basename = 'QInferdoc'


# -- Options for LaTeX output --------------------------------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'QInfer.tex', u'QInfer: Bayesian Inference for Quantum Information',
   u'Christopher Granade and Christopher Ferrie', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Additional stuff for the LaTeX preamble.
latex_preamble = preamble

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
latex_domain_indices = False


# latex_elements = {
#     'maketitle': r"""
# \begin{abstract}
# Lorem ipsum
# \end{abstract}
# \maketitle
# """
# }

# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'qinfer', u'QInfer Documentation',
     [u'Christopher Ferrie and Christopher Granade'], 1)
]


# -- Options for Epub output ---------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = u'QInfer'
epub_author = u'Christopher Ferrie and Christopher Granade'
epub_publisher = u'Christopher Ferrie and Christopher Granade'
epub_copyright = u'2012, Christopher Ferrie and Christopher Granade'

# The language of the text. It defaults to the language option
# or en if the language is not set.
#epub_language = ''

# The scheme of the identifier. Typical schemes are ISBN or URL.
#epub_scheme = ''

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#epub_identifier = ''

# A unique identification for the text.
#epub_uid = ''

# HTML files that should be inserted before the pages created by sphinx.
# The format is a list of tuples containing the path and title.
#epub_pre_files = []

# HTML files shat should be inserted after the pages created by sphinx.
# The format is a list of tuples containing the path and title.
#epub_post_files = []

# A list of files that should not be packed into the epub file.
#epub_exclude_files = []

# The depth of the table of contents in toc.ncx.
#epub_tocdepth = 3

# Allow duplicate toc entries.
#epub_tocdup = True



## EXTLINKS CONFIGURATION ######################################################

extlinks = {
    'arxiv': ('http://arxiv.org/abs/%s', 'arXiv:'),
    'doi': ('https://dx.doi.org/%s', 'doi:'),
}

## OTHER CONFIGURATION PARAMETERS ##############################################

plot_pre_code = """
import numpy as np
from qinfer import *

import matplotlib.pyplot as plt
try: plt.style.use('ggplot')
except: pass
"""

plot_include_source = True

plot_formats = [
    'svg', 'pdf',
    ('hires.png', 250),
    ('png', 125)
]

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'https://docs.python.org/3/': None,
    'numpy': ('https://docs.scipy.org/doc/numpy',None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference',None),
    'IPython': ('https://ipython.org/ipython-doc/stable/', None),
    'ipyparallel': ('https://ipyparallel.readthedocs.io/en/latest/', None)
}

autodoc_member_order = 'bysource'
autodoc_default_flags = ['show-inheritance', 'undoc-members']
pngmath_latex_preamble = preamble
doctest_global_setup = '''
from __future__ import division, print_function
import numpy as np
'''

