---
title: Using LyX to write ACM and Eurographics articles
url: http://momentsingraphics.de/UsingLyX.html
author: Your coauthors will hate it
published: '2019-11-11'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Using LyX to write ACM and Eurographics articles

If you are familiar with [my work](http://momentsingraphics.de/Publications.html), you may be surprised to hear that I barely ever write documents in LaTeX. All of my first author papers, as well as my bachelor, master and PhD thesis are written entirely in [LyX](https://www.lyx.org/). LyX is a text editor that generates LaTeX code for you. I appreciate it because it helps me get through the creative process of writing without distraction and aids my mathematical research through its excellent formula editor.

Since I believe that it deserves to be more well-known and well-liked among academics, this blog post gives a brief introduction to its concept, explains why and how I use it and under which circumstances you might want to use it. At the bottom there are downloads for layout files that I wrote to be able to create ACM and Eurographics articles using LyX.

## What is LyX?

[LyX](https://www.lyx.org/WhatIsLyX) describes itself as What You See Is What You Mean editor. You edit a visual representation of the semantics of a LaTeX document (see [Figure 1](http://momentsingraphics.de#LyXScreenshot)). All information needed to generate LaTeX code from your LyX document is visible on screen in some way. What you see is relatively close to what you get in your PDF, especially compared to raw LaTeX code, but it is not supposed to be identical. You can have bits of LaTeX code in your LyX document if you need to, but use of this "[evil red text](https://wiki.lyx.org/FAQ/ERT)" is discouraged.

![LyXScreenshot](../../assets/43c99437f11164ba.png)


![LyXScreenshot](../../assets/43c99437f11164ba.png)

**Figure 1:**A screenshot of LyX showing an excerpt from a

[recent paper](http://momentsingraphics.de/Siggraph2019.html). Note that labels and cross-references show the full identifier of the label like LaTeX code but formulas look the way they do in a PDF.

With the click of a button, LyX will gather all relevant files, generate LaTeX code, use the TeX distribution of your choice to compile it and give you [a PDF](http://momentsingraphics.de/Media/Siggraph2019/Peters2019-CompactSpectra.pdf) that is as pretty as anything else created with LaTeX. There are also some other output formats, like HTML or plain text. It is free open source software written in C++ and highly responsive. After 24 years, it is still under active development. Every once in a while, I encounter a crash but at least the emergency save feature has never let me down.

## Why I like it

For academic writing, there is no way around LaTeX but that does not mean that you have to write your LaTeX code manually. I prefer LyX because it does not get in the way of my creative process. Editing LaTeX directly, your code looks completely different from the final document, so you compile frequently. Every time you compile, it takes a little while and then there may be some trivial syntax error. Having fixed that, you compile again, read your text and note that you wrote \(x^-1\) instead of \(x^{-1}\). You go back to that point in the code, fix it, recompile, reread your text and at that point, you can continue thinking about things that matter. With LyX, the presentation in the editor is closer to the final product, so you compile less often. Besides it is hardly possible to create a LyX document that does not compile (without evil red text), so you are less likely to be interrupted by trivial errors.

Though, for me the best thing about LyX is its formula editor. It is the best one I know. Everything else feels sluggish in comparison. For the most part, you just type LaTeX code but it turns into nicely typeset formulas immediately. You do not type braces but instead navigate the cursor into or out of little boxes. If you forgot a command, the toolbars give you quick access to all the most common building blocks of formulas.

LyX has become an essential part of my workflow for mathematical research. If I am unsure where an idea will take me, I like to use a whiteboard but for other derivations I always use LyX. In a chain of equations or implications, I just keep copying the previous line and edit it until I think that making more changes in one step would be incomprehensible. If something goes wrong, it is easy to start over without erasing everything. And you automatically get a somewhat orderly record of everything you tried. All of this takes a lot of frustration out of the process. I would rather not write, let alone derive, formulas like the one in [Figure 2](http://momentsingraphics.de#LongFormula) in raw LaTeX.

## How I use it

When writing papers in LyX, I like to have one file per section. It makes it easier to find parts and makes version histories more informative. All these child documents are tied together by a Paper.lyx that incorporates them as [input](https://wiki.lyx.org/FAQ/Multidoc). Additionally, I always have a file with macros for each mathematical identifier that I use (see [Figure 3](http://momentsingraphics.de#Macros)). This way, typing formulas feels more like typing code with multi-word identifiers. It aids me in thinking and makes it harder to introduce typos. It also lets me change notation any time, although I hardly ever do that.

Most of my figures come straight out of [matplotlib](https://matplotlib.org/). I export them as PDF using [pyplot.savefig()](https://matplotlib.org/api/_as_gen/matplotlib.pyplot.savefig.html) and add them into floats in the LyX document. Subfloats, i.e. small figures labeled (a), (b), (c) inside larger ones, are trivial to do and often make it easier to discuss different aspects in turn. Specifying their width is most convenient using Column Width % as unit.

One hurdle when you prepare your submission in LyX is that you need a [layout file](https://wiki.lyx.org/Layouts/Layouts). It is essentially a wrapper around the LaTeX class file telling LyX how to expose various commands and environments in the user interface. I wrote one for the [ACM master article template](https://www.acm.org/publications/proceedings-template) and for the [Eurographics layout](https://www.eg.org/wp/eurographics-publications/guidelines/#cgf_authors). They are not particularly sophisticated but have served me well for several publications. A small amount of [evil red text](https://wiki.lyx.org/FAQ/ERT) may be needed to specify meta-data, especially in the author list. You can [download my layouts here](http://momentsingraphics.de/Media/UsingLyX/ACMAndEGLyXLayouts.zip) and use these [installation instructions](https://wiki.lyx.org/LyX/UserDir).

## Your coauthors will hate it

This blog post is essentially a love letter to LyX. Honesty mandates that I point out the biggest problem in using it for academic writing. [Learning LyX](https://wiki.lyx.org/LyX/LyXHelpDocuments) takes time. And the way it works, it is best to first learn LaTeX, at least to some extent. It is something you can do to increase your productivity in the long run. Nobody likes to be forced to use a program like that, especially not close to a submission deadline. Therefore, you should not use LyX if you expect major contributions to the writing from one of your coauthors (unless that coauthor happens to be a LyX fan).

On the plus side, I sometimes had to send LaTeX code generated by LyX to publishers for copy editing. I never got any complaints about that. Going from LyX to LaTeX is quite easy. Going the other way is the painful part. LyX can import LaTeX code but due to the intricacies of class files, this feature is fairly limited and often resorts to [evil red text](https://wiki.lyx.org/FAQ/ERT).

## Conclusion

LyX is great, so you should go [download it right now](https://www.lyx.org/Download). If you work with formulas a lot, you will never want to miss its formula editor. And if you feel sick of typing LaTeX code, it will take that burden from you. Just make sure your coauthors are ok with that.