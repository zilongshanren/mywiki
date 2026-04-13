---
title: I Just Saw a Race Condition
url: http://hacksoflife.blogspot.com/2010/09/i-just-saw-race-condition.html
author: Benjamin Supnik
published: '2010-09-01'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

As far as I can tell, this is what happened:

- The variable I was printing was subject to writes in a race condition - some other thread was splatting it.
- After printing the variable, I printed some pieces of an STL container, which had to execute code in the attached process, which temporarily released all threads.
- Thus when I turn around, the program has been running.

## No comments:

## Post a Comment