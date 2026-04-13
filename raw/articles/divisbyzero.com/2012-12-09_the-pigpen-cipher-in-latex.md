---
title: The Pigpen Cipher in Latex
url: https://divisbyzero.com/2012/12/09/the-pigpen-cipher-in-latex/
author: Dave Richeson
published: '2012-12-09'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Recently my son and his friends have been enjoying sending secret messages back-and-forth using the [pigpen cipher](http://en.wikipedia.org/wiki/Pigpen_cipher) (also called the masonic cipher or Freemason’s cipher). It produces codes that look like:

![](../../assets/ebec7fb3258b2dd8.png)


The pigpen cipher is a simple [substitution cipher](http://en.wikipedia.org/wiki/Monoalphabetic_substitution)—there is a 1-1 correspondence between these special symbols and letters of the alphabet. The correspondence is illustrated in the chart below. Each letter is replaced by the boundaries around the letter and a dot if there is one. So, for example,

![](../../assets/0bffbbcfb783b191.png)


![](../../assets/453318320ca97109.png)


I, being a lover of Latex, wondered if it was possible to create pigpen ciphers in Latex. It is! The cipher text text above was created using Oliver Corff’s [Pigpen Cipher](http://www.ctan.org/tex-archive/fonts/pigpen) package. After downloading the package and including it in the Latex file you must simply type

{\pigpenfont MATH IS FUN}

to obtain

![](../../assets/ec527970e920ea5c.png)


**Update 2023:** I couldn’t get this to work when I tried it again now, years later. After some searching online, I found a comment on [the TeX Stack Exchange](https://tex.stackexchange.com/questions/630734/pigpen-on-macos/630746#630746) site saying that you have to add one line to the preamble to fix the problem:

\documentclass[]{article}

\usepackage{pigpen}

\pdfgentounicode=0

\begin{document}

THE PIGPEN CIPHER WORKS NOW!\\

{\pigpenfont THE PIGPEN CIPHER WORKS NOW}!

\end{document}

(Pigpen cipher key (picture) from [Wikipedia](http://en.wikipedia.org/wiki/File:Pigpen_cipher_key.svg))

I don’t know if you’re interested, I recently used Corff’s font to create my own font, the Rose Croix Cipher font, after failing to find anything similar online. Examples of the Rose Croix Cipher can be seen at scottishrite.org, at the top and bottom of the page. (The Rose Croix is the 18th degree of the Scottish Rite of Freemasonry.)

Nice work. Thanks for the link.