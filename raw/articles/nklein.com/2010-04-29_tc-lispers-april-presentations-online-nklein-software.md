---
title: 'TC Lispers April Presentations online :: nklein software'
url: http://nklein.com/2010/04/tc-lispers-april-presentations-online/
author: Pat
published: '2010-04-29'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

The Twin Cities Lisp Users Group meeting for April was last Monday. The main topic was Web Frameworks, but there were also two shorter talks.

## Weblocks Presentation

Patrick Stein gave this presentation at the TC Lispers meeting in April 2010.


## Allegro Serve and Web Actions Presentation

Robert Goldman gave this presentation at the TC Lispers meeting in April 2010.

*Apology:** Unfortunately, ScreenFlow bombed out on me when I went to stop recording. It subsequently saw that it had a partial project there but was unable to recover it. As such, there is no video available for this presentation. Feh. â Patrick*

## Hunchentoot Presentation

Paul Krueger gave this presentation at the TC Lispers meeting in April 2010.


[Hunchentoot](http://vimeo.com/11312889) on [Vimeo](http://vimeo.com).

## Cocoa Lisp Controller Presentation

Paul Krueger gave this presentation at the TC Lispers meeting in April 2010.

[LispController Reference Manual](http://trac.clozure.com/ccl/browser/trunk/source/contrib/krueger/InterfaceProjects/Documentation/LispController%20Reference.pdf)[Tutorial Document for Building Cocoa Interfaces with Lisp](http://trac.clozure.com/ccl/browser/trunk/source/contrib/krueger/InterfaceProjects/Documentation/InterfaceBuilderWithCCLTutorial2.1.pdf)[Paul Krueger’s Cocoa Lisp contributions to CCL](http://trac.clozure.com/ccl/browser/trunk/source/contrib/krueger/InterfaceProjects)


[Cocoa Lisp Controller](http://vimeo.com/11315777) on [Vimeo](http://vimeo.com).

## CL-Growl Presentation

Patrick Stein gave this presentation at the TC Lispers meeting in April 2010.


I’d like to get in touch with Paul Krueger regarding the LispCast code he updated for Hunchentoot. I may be doing an updated version of Eric Norman’d LispCast screencasts, and that code would be quite helpful.

I couldn’t find his email address anywhere. If you have a way of contacting him, could you let him know my email address: XXXXXXX? Or Dr. Krueger, if you’re reading this, please contact me.

Thanks.

@24:30 in the Weblocks video Patrick mentions the inconvenience of how it binds on the current function value, for myself I use a lambda that calls the desired defun, which allows for straightforward C-c C-c in slime as one would hope/expect.

It’s true. Instead of this:

I can do this:

(apply #'foo args)))