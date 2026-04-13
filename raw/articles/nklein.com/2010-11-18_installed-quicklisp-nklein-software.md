---
title: 'Installed Quicklisp :: nklein software'
url: http://nklein.com/2010/11/installed-quicklisp/
author: Pat
published: '2010-11-18'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I installed [Quicklisp](http://www.quicklisp.org/) tonight. It was super-simple. In about 1/2 an hour, I got slime up and running and installed all of the packages that I regularly use.

It installs itself in a **quicklisp/** subdirectory of your home directory. I didn’t really want it cluttering up my normal **ls** output, so I moved it to **.quicklisp/** and updated my **.sbclrc** to refer to this new path. It had to recompile everything when I loaded it next, but it handled it gracefully.

It took me less than a minute to get slime set up. This is an improvement of about five hours and fifty-nine minutes over the previous time that I set up slime.

I definitely give my two thumbs up for Quicklisp.

Thanks, Zach!

You could have installed slime with

so it would immediately have been installed in the directory of your choice!

(Look up in FAQ.)

Awesome. If it hadn’t moved easily, I would have poked deeper. As it was, it took me only a few seconds to relocate it.