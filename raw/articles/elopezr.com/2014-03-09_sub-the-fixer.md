---
title: Sub the Fixer
url: https://www.elopezr.com/sub-the-fixer/
author: Redorav
published: '2014-03-09'
source_blog: The Code Corsair
source_site: http://www.elopezr.com
category: game programming
fetched: '2026-04-13'
---

Sub the Fixer is a **subtitle fixer** for video subtitles int the .srt format. It aims to fix common problems that derive from the use of OCR programs (such as [SupRip](http://exar.ch/suprip/) or [SubRip](http://zuggy.wz.cz/)) to convert static .sup image files extracted from DVDs and Blu-rays into editable text, such as the popular .srt format. This program attempts to fix them by applying a series of idiomatic rules, such as not allowing a capital I in the middle of a word.

It is written in **Python** and makes heavy use **Regular Expressions**. It also uses the wxPython GUI libraries, the python bindings of the portable and multiplatform [wxWidgets](http://www.wxwidgets.org/) project.

**Example:** a common mistake is confusing lower-case l with capital I, especially when using the arial font.

**l** saw a **I**arge crocodi**I**e **I**ast fa**II**, with my friend **I**an, who **I**ives in **I**owa.

In this example, three rules are being used. First, a lower-case l can never appear on its own in a text, that is, surrounded by spaces. Second, a word in the middle of a sentence is never capitalized, unless it’s a proper name for a place or a persona. I’m sorry Ian, if you’re living in Iowa, but I can’t let you write ‘Iast’ or ‘Iarge’. Third, capital I’s can never appear in the middle of a word. Therefore, the text would get corrected as

**I** saw a **l**arge crocodi**l**e **l**ast fa**ll**, with my friend **l**an, who **l**ives in **l**owa.

There is a problem, then, with proper names (depending on the font you will or won’t see that Iowa and Ian are spelled with a lower-case l), but it is much easier to correct those than to correct every other word that starts with lower-case l and has been capitalized by mistake. It’s probably easy to fix that with a dictionary, which could be added at some point.

Currently, the program supports **7 languages** which use roman-derived alphabets, with specific rules applied to them. English, Spanish, French, Italian, German, Polish and Portuguese.

**Download**

The current version can be found [here](http://dl.dropbox.com/u/14054799/Portfolio%20Uploads/SubtitleFixer.pyw).

Bear in mind you need to install [wxPython](http://www.wxpython.org/) for the GUI to work. As there is no support for Python 3, you should use either Python 2.6 or 2.7.

I have not tested all possible cases, in case you find a bug [let me know](mailto:e.lopezr@elopezr.com?subject=Bug%20in%20Sub%20the%20Fixer!).