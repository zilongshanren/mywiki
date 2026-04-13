---
title: Don't Go Anywhere!
url: http://hacksoflife.blogspot.com/2011/03/dont-go-anywhere.html
author: Benjamin Supnik
published: '2011-03-07'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

All is good and I'm sipping my coffee when I hit a break-point. Hrm...looks like we have a NaN. Well, we divided by a sum of some elements of a vector. What's in the vector?

print ag_block.spellings_s.[0].widths[1]Ah...8 tiles. At this point I am already dead. If you've debugged threaded apps you already know what went wrong:

- The array access operator in vector is really a function call (particularly in debug mode - we jam bounds checks in there).
- GDB has to let the application 'run' to run the array operator, and at that instant, the sim's thread can switch.
- The new thread will run until it hits some kind of break-point.
- If you have 8 threads running the same operation, you will hit the break point you expect...but from the wrong thread.

A brute force solution is to turn off threading - in X-Plane you can simply tell the sim that your machine has one core using the command line. But that means slow load times.

Fortunately gdb has these clever commands:

set scheduler-locking onWhen you set scheduler locking on, the thread scheduler can't jump threads. This is handy before an extended inspection session with STL classes. You can apparently put the scheduler into 'step' mode, which will switch on run but not on step, but I haven't needed that yet.

set scheduler-locking off

## No comments:

## Post a Comment