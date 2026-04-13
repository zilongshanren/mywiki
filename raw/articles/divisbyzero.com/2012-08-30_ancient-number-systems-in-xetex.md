---
title: Ancient number systems in XeTeX
url: https://divisbyzero.com/2012/08/30/ancient-number-systems-in-xetex/
author: Dave Richeson
published: '2012-08-30'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I am teaching a history of mathematics class this semester. We are beginning with a brief discussion of ancient number systems: [Egyptian](http://en.wikipedia.org/wiki/Egyptian_numerals), [Babylonian](http://en.wikipedia.org/wiki/Babylonian_numerals), [Mayan](http://en.wikipedia.org/wiki/Maya_numerals), [Chinese](http://en.wikipedia.org/wiki/Counting_rods), [Incan](http://en.wikipedia.org/wiki/Quipu), [Greek](http://en.wikipedia.org/wiki/Greek_numerals), [Roman](http://en.wikipedia.org/wiki/Roman_numerals), and [Hindu-Arabic](http://en.wikipedia.org/wiki/Hindu–Arabic_numeral_system). As I was writing up the first homework assignment it occured to me that I should investigate whether these numbers could be typeset using LaTeX.

It quickly became apparent that, because fonts are involved, I would have to use [XeTeX](http://en.wikipedia.org/wiki/XeTeX) rather than LaTeX. It was a fun (although time consuming) exercise. In the end I was able to typeset Egyptian hieroglyphics, Babylonian cuneiform, and Chinese rod numerals. Because the syntax was often messy, I spent a while burying the complicated TeX in the headers so that the numbers would be easy to work with in the document.

For example, to generate the Egyptian hieroglyphics for 123 I write

\Ehun\Eten\Eten\Eone\Eone\Eone.

The fraction 1/123 is

\Efrac{\Ehun\Eten\Eten\Eone\Eone\Eone}.

To express 123 in cuneiform all I have to write is

\Bnum{123}.

To create a number board with the Chinese counting rods representing 123 I type

\Cnum{|x|x|x|}{\Cvone & \Chtwo & \Cvthree}.

If you would like to give this a try, download my .tex files:

[babylonian.tex](http://users.dickinson.edu/~richesod/math301-401/babylonian.tex) and [babylonian.pdf](http://users.dickinson.edu/~richesod/math301-401/babylonian.pdf)

I’d love to be able to do something similar with the Mayan numbers. I tried for a while, but couldn’t get them to work.

[Update: I figured out how to generate Mayan numerals. [Here’s a Tex file](http://users.dickinson.edu/~richesod/math301-401/numbersystems.tex) with all four number systems—Egyptian, Babylonian, Chinese, and Mayan.]

Disclaimer: I know my way around TeX pretty well, but I’m not a power user. It took me quite a while to get all this to work. I’m not sure I can offer much trouble-shooting advice if you can’t get this to work on your computer.

That’s quite cool! We don’t offer a “History of Mathematics” type course at my college…but I’ll file this post away just in case we eventually do.

I don’t have a reason to use this right now, but this is so cool. Thanks for sharing.

This is great! Thanks for sharing.

Hi Professor Richeson, is it possible that you can share that History of Mathematics course with us?, maybe the reading list, the topics that you cover, some lectures notes, whatever.

A few people have asked me that. Unfortunately, for day-to-day operations everything is on Moodle (our CMS), and thus it requires a password. But I’ll see what I can do at the end of the semester. It would be nice to do something like you suggest.

About Mayan numbers : your difficulty probably comes from the fact that they are not yet encoded in unicode. However, LaTeX packages exists to type Mayan http://www.math.univ-toulouse.fr/~orevkov/mayaps.html and Epi-Olmec http://obelix.ee.duth.gr/~apostolo/Epi-Olmec/ . Since both these writing systems use the same mesoamerican numbers, you can probably use any of the 2 packages for your purpose.

Thanks! I’ll be sure to look at those links.