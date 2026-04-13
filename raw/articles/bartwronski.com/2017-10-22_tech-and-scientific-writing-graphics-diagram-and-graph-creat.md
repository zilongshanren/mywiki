---
title: Tech and scientific writing – graphics, diagram and graph creation tools
url: https://bartwronski.com/2017/10/22/tech-and-scientific-writing-graphics-diagram-and-graph-creation-tools/
published: '2017-10-22'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

Few days ago, I asked a question on twitter: [https://twitter.com/BartWronsk/status/919618905319997440](https://twitter.com/BartWronsk/status/919618905319997440)

“What is industry/academic standard for diagrams in tech writing? PowerPoint/GoogleDocs diagrams? Dedicated tool like Visio/Dia? Procedural?

I usually use first, but far from satisfied…For proc tried SVG,JS,Graphviz,even Mathematica, but results are either ugly or *lots* of work…”

I got 26 replies, thanks everyone who contributed!

To not have it lost and hoping that someone else will find it useful, writing down answers in a few categories with some comments. Please comment on this post if I got anything wrong and/or I omitted something.

Note that there are no real “conclusions”, almost everyone used something else! Probably almost anything on the list will work. But as a rule of thumb, probably it’s useful to have each of:

- Dedicated vector graphics program (I’ll give a try to Inkscape and Photoshop vector graphics),
- Favorite scientific environment for data exploration and plotting (Python+Matplotlib, Mathematica, Matlab),
- Some favorite environment for authoring documents (whether LaTeX, mathcha or just Powerpoint or Google Docs),
- maybe something interactive for web/blog (shadertoy, D3, Mathbox).

## Vector graphics software

[Adobe Illustrator](https://www.adobe.com/products/illustrator.html), Subscription $19.99/month, Mac/Windows

For many years standard / go-to for vector graphics. At the same time quite pricey subscription model and could be an overkill for simple diagrams?

[Affinity Designer](https://affinity.serif.com/en-us/), $49.99, Mac/Windows

No subscription alternative to Illustrator. Lots of people recommended it, worth having a look!

[Inkscape](https://inkscape.org/en/), Opensource/Free, Linux/Mac/Windows

Totally free and open source. Subjectively UI looks much cleaner than other open source graphics software.

[Omnigraffle](https://www.omnigroup.com/omnigraffle), $49/$99 iOS, $99/$199 Mac

Recommended by many people, UI looks pretty clean and productive, sadly Mac/iOS only.

[Xfig](http://mcj.sourceforge.net/), Opensource/Free, Linux/Mac/Windows

Dormant development, quite ugly interface (IMO). But open source and free.

## Dedicated diagram / flow chart software

[Microsoft Visio](https://products.office.com/en-us/Visio/), $299 or $18 subscription, Mac/Windows

Professional industry grade diagram software. Quite expensive…

[SmartDraw](https://www.smartdraw.com/), Subscription $9.95/month, Mac/Windows/Cloud

Flowchart marker; don’t know if it’s useful for other, more complicated graphs and diagrams.

[yEd](https://www.yworks.com/products/yed), Free, Linux/Mac/Windows

Graph and flowchart only (?), free and multiplatform.

[Dia](https://sourceforge.net/projects/dia-installer/), Free, Linux/Mac/Windows

Dormant open-source project. I used it few times and think there are better, more modern tools (?).

[Lucidchart](https://www.lucidchart.com/), both free and paid options

Don’t know much about it, looks like it’s more about flowcharts

[draw.io](https://www.draw.io/), Free, cloud/web based

UI looks very similar to Google Docs, very low entry barrier. Again more about just simple, graph-like diagrams / flow charts.

[Visual Paradigm](https://www.visual-paradigm.com/), $349, Linux/Mac/Windows

Another dedicated UML-like, visual diagram tool.

## Other software

[Microsoft Powerpoint](https://products.office.com/en-us/powerpoint) $109.99, Mac/Windows

My go-to drawing solutions for any presentations so far. Works great, supports animations, but is painfully limited.

[Photoshop ](http://www.adobe.com/products/photoshop.html)and vector graphics there, Subscription $9.99 a month, Mac/Windows

I’ve never used PS vector graphics, but it’s software I already pay for, so could be a good idea to try it.

[Mathcha](https://www.mathcha.io/), free, cloud

This one is very interesting – equation and mathematical graphics (simple plots, diagrams) online editor. Looks like way easier entry / access WYSIWYG LaTeX editor.

[Google Docs ](http://docs.google.com)and family, Free, cloud based

Using this quite a lot at work (what a surprise!) for drawing simple diagrams and it works pretty well. Not leaving document is a big plus, just like with Powerpoint.

[Grapher](https://en.wikipedia.org/wiki/Grapher), part of MacOS

Dedicated tool embedded in MacOS; surprisingly powerful for something included in every install!

## Interactive web based

[Shadertoy](https://www.shadertoy.com/), free

This could be a surprising choice, but check out e.g. [this ](https://www.shadertoy.com/view/MllczB)algorithm visualization from Leonard Ritter. Code + visualization in one place with animations and optional interactivity!

[Mathbox](https://acko.net/blog/making-mathbox/), free, Javascript library

Quite amazing math visualization library for JS and web. Amazing results, but it’s quite a heavy tool that could be overkill for small diagrams.

[Flot](http://www.flotcharts.org/), free, Javascript library

Interactive plotting for jQuery. Don’t know much about it (not using JS as much as I’d like for creating web pages).

[D3](https://d3js.org/), free, Javascript library

Beautiful data visualizations – but not really for generic graphs.

[Desmos calculator](https://www.desmos.com/calculator), free, online

Nice semi-interactive and powerful online mathematical function plotting tool. Good to not just visualize, but also explain reasoning behind some curve look.

[Render diagrams](http://renderdiagrams.org/) (or [second link](http://renderdiagrams.org/editor.html)), free, online

A fresh tool specialized in rendering diagrams and for graphics programmers! Has lots of built in primitives that occur very often in such use case / scenario. Looks like it’s early stage, but very promising, looking forward to its develpment!

## Procedural languages and libraries

[Asymptote](http://asymptote.sourceforge.net/), open source

Dedicated vector graphics language.

[Markdeep](https://casual-effects.com/markdeep/), open source

“Markdeep is a technology for writing plain text documents that will look good in any web browser (…). It supports diagrams, calendars, equations, and other features as extensions of Markdown syntax.”

Limited diagramming capabilities, but all-in-one document creation solution.

[Matplotlib](https://matplotlib.org/), Python, open source

Go-to Python solution for visualizing data. By default not prettiest, but very powerful and “just works”.

[LaTeX with PGF/TikZ](http://www.texample.net/tikz/), Tex, open source

LaTeX extension/language to define graphs and generally, graphics – programmaticly. Would love to learn it some day and become proficient, but even people who recommended it, warned of steep learning curve.

[UMLet ](http://www.umlet.com/)Free, has also UI

Free tool to create UML diagrams.

[Matlab](https://www.mathworks.com/products/matlab.html), $2150, Linux/Mac/Windows

The most expensive option of the list – numerical professional mathematical/engineering package with some graphics options among numerous others.

[GNU Octave](https://www.gnu.org/software/octave/), open source, all platforms

Free and open source alternative to Matlab! Probably not as powerful for most uses, but for graphs and vector graphics should be comparable. Used it at college for computer vision classes and well, it definitely worked fine for most algebraic problems.

[Gnuplot](http://www.gnuplot.info/), open source, all platforms

Simple command line tool for plots that I used few times at college. For quick plots very convenient.

[Mathematica](https://www.wolfram.com/mathematica/), $320, Linux/Mac/Windows

Affordable mathematical symbolic and numerical analysis and data exploration software. I wrote about it in the past, used it numerous times for plots in many of my blog posts and always recommend. I also played with graph plotting, though found it a little bit frustrating and not customizable/pretty enough by default.

[Graphviz](http://www.graphviz.org/), open source, all platforms

One of those “useful but ugly” pieces of software. Good for quickly creating graphs from code, for anything else no great (?).

[Svgwrite for Python](https://pythonhosted.org/svgwrite/), open source, all platforms

Python library for writing directly into SVG. Quite low level, but powerful for specific very “procedural” use cases.

[GGplot2 for R](http://ggplot2.org/), open source, all platforms

I don’t know much about R, but my understanding is that is its matplotlib equivalent. If you use R for data exploration, probably a goto solution.

#### Editing directly [PostScript](http://www.math.ubc.ca/~cass/graphics/manual/), open source, all platforms

Very low level and *hardcore* option; maybe easier with outputting ps directly/proceduraly from code?


Dedicated diagram / flow chart software: back in the days (2013-2015), I must use Visual Paradigm for the courses Distributed Systems, Software Architecture, and Requirements Analysis for Complex Software Systems. The software includes support for all UML diagrams (domain, class, flow, etc.) and also contains some handy utilities for reorganizing and untangling very large diagrams to make them more readable 🙂 (The only real disadvantage was copy-pasting: you really get punished if you copy-paste between diagrams since it looks more like a copying a “reference” instead of a “value”). Procedural languages and libraries: I am absolutely no fan of Matlab due to its Fortran kind of indexing starting from 1 instead of zero and due to refusing correcting some errata from papers (because it was published in that way). A free alternative using the same syntax and method names is GNU Octave.

Thanks for the suggestions! Totally forgot about Octave and I used it at college (most labs had no Matlab licences…)! Mathematica has same indexing, I guess it is “standard” there?

Do you know the Girih App?

http://girih.rockt.es