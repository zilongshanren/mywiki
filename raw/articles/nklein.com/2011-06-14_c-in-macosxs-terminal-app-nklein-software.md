---
title: 'C- in MacOSX’s Terminal.app :: nklein software'
url: http://nklein.com/2011/06/c-in-macosxs-terminal-app/
author: Pat
published: '2011-06-14'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

After tonight’s [TC Lispers Meeting](http://tclispers.org/events/june-meeting-emacs-theme), I had a renewed interest in figuring out why C-<right arrow> didn’t work for me in Org-Mode or Paredit.

After a whole bunch of running in circles, I have discovered a combination that works (with [these clues](http://marc-abramowitz.com/archives/2006/10/05/ctrl-left-and-ctrl-right-in-bash-and-emacs/)). I have my `TERM`

variable set to `xterm-color`

. I configured the Terminal.app using its Keyboard settings to have it send the string “\033[1;5C” for C-<right arrow> and “\033[1;5D” for C-<left arrow>. (The “\033” is the escape key.)

This works for me even through `screen`

.

Bonus.

Thanks! I’ve been wanting this for ages!