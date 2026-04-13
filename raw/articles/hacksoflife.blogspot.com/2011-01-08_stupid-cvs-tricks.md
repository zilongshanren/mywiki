---
title: Stupid CVS Tricks
url: http://hacksoflife.blogspot.com/2011/01/stupid-cvs-tricks.html
author: Benjamin Supnik
published: '2011-01-08'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[this](http://durak.org/sean/pubs/software/cvsbook/Enabling-Watches-In-The-Repository.html)) how to get CVS to notify us somewhere other than the mail service of the server it's running on. See the link for instructions, but basically you can make a 'users' dictionary file that maps users to custom external email addresses...the file isn't in the default config (which is weird).

Also, note that the CVS watch command can do two things:

- It can subscribe to events (edit, unedit and commit). When you watch add yourself with some or all of these events, you get email (looked up via users). Since watches go to specific subscribed users, the CVS notify file uses a wildcard to send to specific users. (This is different from loginfo which sends to a list of everyone who cares about any commit for a given module.)
- It can force a file to be checked out locked (thus forcing an edit/unedit workflow) using cvs watch on. We only use this to force our X-Code project file to be checked out locked (to prevent the accumulation of lots of trivial project changes).

## No comments:

## Post a Comment