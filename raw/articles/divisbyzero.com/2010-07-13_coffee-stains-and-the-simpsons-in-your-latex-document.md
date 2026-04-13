---
title: Coffee stains and the Simpsons in your LaTeX document
url: https://divisbyzero.com/2010/07/13/coffee-stains-and-the-simpsons-in-your-latex-document/
author: Dave Richeson
published: '2010-07-13'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

A few weeks ago [John D. Cook](http://twitter.com/johndcook) posted a tweet [asking for suggestions](http://twitter.com/TeXtip/status/16777354796) for his [@TeXtip](http://twitter.com/TeXtip/) Twitter feed.

Usually @TeXtip posts are useful tips or factual tidbits about the typesetting program. I decided to send him [a humorous suggestion](http://twitter.com/divbyzero/statuses/16936952952) instead. He [posted the tip on Twitter](http://twitter.com/TeXtip/status/18359194273) yesterday. I sent him a link to [Hanno Rein’s coffee.sty package](http://hanno-rein.de/archives/349) which adds a coffee stain to any LaTeX document.

Today I remembered another fun LaTeX package that I’d encountered years ago. The [Simpsons package](http://tug.ctan.org/tex-archive/usergrps/uktug/baskervi/4_4/) allows you to insert Bart, Homer, Maggie, Mr. Burns, Lisa, Marge, or the Springfield Nuclear Power Plant into your LaTeX document. (The screenshot below is from the [Comprehensive LaTeX Symbol List](http://www.ctan.org/tex-archive/info/symbols/comprehensive/symbols-a4.pdf).)

![Screen shot 2010-07-13 at 8.43.31 AM](../../assets/48b6b82b4b50732b.png)


To use this on your own, go to [this web page](http://tug.ctan.org/tex-archive/usergrps/uktug/baskervi/4_4/) and download the simpsons.sty file. Put it somewhere that LaTeX can find it (putting it in the same directory as your tex file is fine) and put \usepackage{simpsons} at the start of your document. Then you can get your favorite character to appear using the commands \Bart, \Homer, etc. (no dollar signs needed, by the way). You can make the character turn to the left using \Left. Also, you can specify the location of the characters’ two pupils by using the \Goofy command (the coordinates for the normal pupil locations are (0,0) and (0,0)). For example, \Left\Goofy\Bart(1,1.6)(.85,1.6) produces an image of the left-facing Bart rolling his eyes at his sister Lisa (below).

## 3 Comments

Comments are closed.