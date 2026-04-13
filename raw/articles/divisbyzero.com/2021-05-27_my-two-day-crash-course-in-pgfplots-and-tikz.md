---
title: My Two-Day Crash Course in PGFPlots and TikZ
url: https://divisbyzero.com/2021/05/27/my-two-day-crash-course-in-pgfplots-and-tikz/
author: Dave Richeson
published: '2021-05-27'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I will be teaching multivariable calculus in the fall. During the semester, I’ll have to make numerous figures in two-and three-dimensional space for exams and handouts. One of the things I wanted to do this summer was to learn how to use [TikZ](https://en.wikipedia.org/wiki/PGF/TikZ) to create graphs and other graphics in my LaTeX documents.

After a little exploration, I discovered that [PGFPlots](http://pgfplots.sourceforge.net) was the LaTeX package I was looking for. It makes drawing graphs in TikZ easy, and the graphs are highly customizable. So, for the last two days, I dove in and started playing with it. I’ve included some of my creations below.

If you would like to see the LaTeX code for these figures, you can open this [Overleaf](https://www.overleaf.com/read/hsfpzstppzrp) link. Feel free to copy and modify them. Since I’m a beginner, I can’t promise that I’ve created them the best and most efficient way.

There is one thing I should mention. In order to generate the contour plots (the last two figures at the bottom of this post), I had to install [gnuplot](http://www.gnuplot.info) on my computer. (This was a little bit involved.) If you are using Overleaf, you don’t have to do this, but if you are using a desktop LaTeX program, you will probably have to.

As a last comment: It may take a little while for the document to compile in Overleaf. Each figure has to be regenerated each time the document compiles. There is a way to keep this from happening—essentially it regenerates the figure only when there is a change to the code for that figure. You can read more about that approach on [this page](https://www.overleaf.com/learn/latex/Questions/I_have_a_lot_of_tikz,_matlab2tikz_or_pgfplots_figures,_so_I'm_getting_a_compilation_timeout._Can_I_externalise_my_figures%3F).

![](../../assets/a5440881e80457d7.png)


![](../../assets/a5440881e80457d7.png)

![](../../assets/1350520512a99fb2.png)


![](../../assets/1350520512a99fb2.png)

![](../../assets/84530046e9a66038.png)


![](../../assets/84530046e9a66038.png)