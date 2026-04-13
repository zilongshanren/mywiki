---
title: 'dirswitch.el: a fish shell-style directory switcher for shell-mode'
url: https://www.masteringemacs.org/article/dirswitchel-fish-shellstyle-directory-switcher-shellmode
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

A friend of mine showed me [Fish Shell](http://fishshell.com/), a shell replacement for Mac and Linux. One of its coolest features was a “quick directory switcher” that lets you jump to directories you’ve previously visited in that session.

Feeling left out I decided to write dirswitch.el, a directory switcher for `M-x shell`

, Emacs’s built-in shell mode (see [Running shells in Emacs: an Overview](https://www.masteringemacs.org/articles/2010/11/01/running-shells-in-emacs-overview/).)

Like Shell’s `M-r`

history search functionality (which works much like isearch) dirswitch.el will record directories you visit and let you rapidly switch between them by pressing `C-M-n`

and `C-M-p`

.

It’s still a rough prototype but it’s a hallmark example of what a few hours of Emacs hacking can accomplish.

You can get it from [my Github](https://github.com/mickeynp/dirswitch.el) and it’ll probably appear in a package manager near you soon.