---
title: SSE? It's the Memory, Stupid
url: http://hacksoflife.blogspot.com/2011/05/sse-its-memory-stupid.html
author: Benjamin Supnik
published: '2011-05-17'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

One last SSE note: I went to apply SSE optimizations to mesh indexed matrix transforms. While applying some very simple SSE transforms improved throughput 15%, that gain went away when I went for a more complex SSE implementation that tried to avoid the cost of unaligned loads.


Surprising? Well, when I Sharked the more complete implementation it was clear that it was bound up on memory bandwidth. Using the CPU more efficiently doesn't help much if the CPU is starved for data.

## No comments:

## Post a Comment