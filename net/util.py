from pylab import *


def mapsubplot(szx, szy, ids, fn, args):
    for i, arg in zip(ids, args):
        subplot(szx, szy, i)
        fn(arg)

"""
Help in creating reproducible figures for latex

- Fig class figures out path to fig folder
- Fig class knows all existing fig subclasses
- fig subclass creates necessary files by
    - setting itself up
    - call self.plot function
    - saving fig to correct location
    - rendering latex source for inclusion or independent compilation

Given

class foo_spec32(Fig):
    pass

we'll have

- figs/foo_spec32.png
- figs/foo_spec32.tex
- figs/foo_spec32-main.tex

where the tex files have a filled in figure template with scaling/size,
image file, caption, title, and label filled in based on class info.

the -main.tex file can be compiled independently, or .tex is include
in another document.

"""


class Fig(object):
    # determines figure path

    latex_template = """
    \begin{figure}[t]
        \begin{centering}
            \includegraphics[scale=#1]{#2}
        \end{centering}
    \caption{\textbf{#3}: #4}
    \label{#5}
    \end{figure}
    """

    @property
    def latex(self):
        fignm = type(self).__name__
        figtitle = type(self).__doc__
        caption = figtitle + self.captions
        filename = self.figpath + fignm + self.figtype



class Foobar(Fig):
    """Foobar plot"""
    # class docstring becomes title

    def setup(self):
        # create data
        pass

    def plot(self):
        """
        Here we show bla bla bla
        """
        pass

