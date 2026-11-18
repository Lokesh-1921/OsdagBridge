"""Shared LaTeX document, table, and figure formatting."""

from .report_utils import _tex


def preamble(project_name, job_number, report_date, report_version='Rev 0'):
    pn = _tex(project_name)
    jn = _tex(job_number)
    rd = _tex(report_date)
    rv = _tex(report_version)
    return r"""
\documentclass[12pt,a4paper]{report}

% Packages
\usepackage[a4paper, left=16mm, right=16mm, top=15mm, bottom=16mm, includeheadfoot, headheight=18pt, headsep=18pt, footskip=28pt]{geometry}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{array}
\usepackage{tabularx}
\usepackage{float}
\usepackage{fancyhdr}
\usepackage[hidelinks]{hyperref}
\usepackage{xcolor}
\usepackage{setspace}
\usepackage{enumitem}
\usepackage{caption}

\captionsetup{
    labelfont=bf,
    skip=5pt,
    justification=raggedright,
    singlelinecheck=false,
    format=plain
}
\usepackage{subcaption}
\usepackage{multirow}
\usepackage{colortbl}
\usepackage{longtable}
\setlength{\LTleft}{\fill}
\setlength{\LTright}{\fill}
\usepackage{titlesec}
\usepackage{titletoc}
\usepackage{lastpage}
\usepackage{makecell}
\usepackage{etoolbox}
\usepackage{needspace}

\numberwithin{table}{chapter}
\numberwithin{figure}{chapter}
% Table layout and spacing: consistent padding, row height, and longtable pre/post skips
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.12}
\setlength{\LTpre}{6pt}
\setlength{\LTpost}{6pt}
% Table rules (outline thickness) and small extra row height for clarity
\setlength{\arrayrulewidth}{0.5pt}
\setlength{\extrarowheight}{0.6pt}

% Prevent tables from overflowing past the page bottom:
% if fewer than 5 lines remain, break to the next page first.
\BeforeBeginEnvironment{table}{\needspace{5\baselineskip}}
\BeforeBeginEnvironment{longtable}{\needspace{5\baselineskip}}

\definecolor{osdagGreen}{HTML}{91B014}
\definecolor{reportAlert}{HTML}{B42318}

% The first head owns the numbered caption. Both heads use the same cells.
\newcommand{\ReportTableHead}[2]{%
  \caption{#1}\\
  \hline
  #2\\\hline
  \endfirsthead
  \hline
  #2\\\hline
  \endhead
}
\newcommand{\ReportTableGap}{\par\addvspace{6pt}}
\newcommand{\ReportFigureWidth}{0.85\linewidth}
\newcommand{\ReportFigureGap}{\par\addvspace{4pt}}
\newcommand{\ReportPlaceholderWidth}{0.96\linewidth}
\newcommand{\ReportDrawingCellWidth}{0.31\textwidth}
\newcommand{\ReportCompactTable}{\small\setlength{\tabcolsep}{3pt}}

\newcommand{\ReportFooter}{%
  \fancyfoot[L]{\small Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay}
  \fancyfoot[R]{\small Page \thepage\ of \pageref{LastPage}}
  \renewcommand{\footrulewidth}{1pt}
  \renewcommand{\footrule}{{\color{osdagGreen}\hrule width\headwidth height\footrulewidth}}
}
\fancypagestyle{main}{
  \fancyhf{}
  \fancyhead[L]{\small """ + pn + r""" $|$ """ + jn + r"""}
  \fancyhead[R]{\small """ + rd + r""" $|$ """ + rv + r"""}
  \renewcommand{\headrule}{{\color{osdagGreen}\hrule width\headwidth height 1pt}}
  \ReportFooter
}
\fancypagestyle{plain}[main]{}
\fancypagestyle{firstpage}{
  \fancyhf{}
  \renewcommand{\headrulewidth}{0pt}
  \ReportFooter
  \fancyfoot[R]{}
}
\pagestyle{main}
\setstretch{1.15}

% Custom Commands
\newcommand{\placeholder}[1]{\textit{\textless #1\textgreater}}
\newcommand{\todo}[1]{\colorbox{yellow}{TODO: #1}}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}
\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}

\newcommand{\sdstar}{\textsuperscript{*}}

\titleformat{\chapter}[block]
  {\normalfont\Large\bfseries\centering}{\thechapter}{1em}{}
\titlespacing*{\chapter}{0pt}{0pt}{10pt}
\setcounter{tocdepth}{2}

\begin{document}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TITLE PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def title_page(m, osdag_logo, org_logo):
    if osdag_logo:
        lhs = r'\includegraphics[width=\linewidth,keepaspectratio]{' + osdag_logo.replace('\\', '/') + r'}'
    else:
        lhs = r'\textit{(Osdag Logo)}'

    if org_logo:
        rhs = r'\includegraphics[width=\linewidth,height=2.2cm,keepaspectratio]{' + org_logo.replace('\\', '/') + r'}'
    else:
        rhs = r''

    logos_tex = r"""\noindent
\begin{minipage}[c]{0.6\textwidth}
\raggedright
""" + lhs + r"""
\end{minipage}%
\hfill
\begin{minipage}[c]{0.35\textwidth}
\raggedleft
""" + rhs + r"""
\end{minipage}
\\[1cm]
"""

    return r"""
\hypersetup{pageanchor=false}
\begin{titlepage}
\thispagestyle{firstpage}
\centering
\vspace*{1.5cm}
""" + logos_tex + r"""
{\Huge \textbf{OsdagBridge}}\\[0.3cm]
{\large Open Source Software for Steel Girder Bridge Design}\\[1.5cm]
{\Large Design Report}\\[1.5cm]
\begin{tabular}{|L{4cm}|L{10cm}|}
\hline
\textbf{Project Name} & """ + _tex(m.project_name) + r""" \\
\hline
\textbf{Project Location} & """ + _tex(m.project_location) + r""" \\
\hline
\textbf{Author / Designer} & """ + _tex(m.designer) + r""" \\
\hline
\textbf{Reviewer} & """ + _tex(m.reviewer) + r""" \\
\hline
\textbf{Organization} & """ + _tex(m.company) + r""" \\
\hline
\textbf{Client Name and Organization} & """ + _tex(m.client) + r""" \\
\hline
\textbf{Job Number} & """ + _tex(m.job_number) + r""" \\
\hline
\textbf{Date} & """ + _tex(m.report_date) + r""" \\
\hline
\textbf{Report Version} & """ + (_tex(m.subtitle) if m.subtitle else '') + r""" \\
\hline
\end{tabular}
\end{titlepage}
\hypersetup{pageanchor=true}
"""


# ═══════════════════════════════════════════════════════════════════════════════
# TOC
# ═══════════════════════════════════════════════════════════════════════════════

def toc_section():
    return r"""
% Chapter / TOC Formatting
% TOC styling using titletoc
\titlecontents{chapter}[1.5em]
  {\normalfont\vspace{2pt}}
  {\contentslabel{1.5em}}
  {\hspace*{-1.5em}}
  {\hfill\contentspage}

\titlecontents{section}[3.8em]
  {\normalfont}
  {\contentslabel{2.3em}}
  {\hspace*{-2.3em}}
  {\hfill\contentspage}

\titlecontents{subsection}[7.0em]
  {\normalfont}
  {\contentslabel{3.2em}}
  {\hspace*{-3.2em}}
  {\hfill\contentspage}

\newpage
\renewcommand{\contentsname}{\centering\Large\bfseries Table of Contents}
\tableofcontents
"""


CHART_BAR_COLOR = "#56762D"
CHART_LIMIT_COLOR = "#B42318"
CHART_DPI = 180
UR_CHART_SIZE = (7.2, 2.6)
QUANTITY_CHART_SIZE = (7.2, 2.4)


def chart_figure(path, caption):
    """Embed a temporary chart in report layout using a PyLaTeX Figure."""
    from pylatex import Figure, NoEscape

    figure = Figure(position="H")
    figure.add_image(path.as_posix(), width=NoEscape(r"0.93\linewidth"))
    figure.add_caption(caption)
    return figure.dumps()


def _fig_or_placeholder(path, caption, width=r'0.9\textwidth'):
    """Embed figure if path is provided (file already copied to assets), else show placeholder box.
    path is the relative path as pdflatex will see it (e.g. 'assets/plan.png').
    """
    if path:
        p = path.replace('\\', '/')
        return (r'\begin{figure}[H]' + '\n'
                r'\centering' + '\n'
                r'\includegraphics[width=' + width + ']{' + p + '}\n'
                r'\caption*{' + caption + '}\n'
                r'\end{figure}')
    return (r'\begin{figure}[H]' + '\n'
            r'\centering' + '\n'
            r'\fbox{\parbox{\ReportPlaceholderWidth}{' + '\n'
            r'\textit{[ PLACEHOLDER: ' + caption + r' ]}' + '\n'
            r'}}' + '\n'
            r'\caption*{' + caption + '}\n'
            r'\end{figure}')

def _fig_embed(path, caption, width=r'\textwidth', height=None):
    """Embed a real figure when path is provided (already copied); otherwise use an fbox placeholder."""
    if path:
        p = path.replace('\\', '/')
        opts = 'width=' + width
        if height:
            opts += ',height=' + height + ',keepaspectratio'
        return (r'\begin{figure}[H]' + '\n'
                r'\ReportFigureGap' + '\n'
                r'\centering' + '\n'
                r'\includegraphics[' + opts + ']{' + p + '}\n'
                r'\ReportFigureGap' + '\n'
                r'\caption*{\small ' + caption + '}\n'
                r'\ReportFigureGap' + '\n'
                r'\end{figure}')
    # fbox placeholder — matches template exactly
    return (r'\par\noindent\fbox{\parbox{\ReportPlaceholderWidth}{' + '\n'
            r'\textit{[ PLACEHOLDER: ' + caption + r' ]}' + '\n'
            r'}}' + '\n\\par\n')
