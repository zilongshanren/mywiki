---
title: Damn You, L2 Cache!!!
url: http://hacksoflife.blogspot.com/2011/05/damn-you-l2-cache.html
author: Benjamin Supnik
published: '2011-05-01'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[this](http://www.akkadia.org/drepper/cpumemory.pdf)is a good read. Having spent the weekend reading about how import it is not to miss cache and being reminded that having your structs fit in cache lines makes you bad-ass, I was all prepared to score an epic win against the forces of

[garbage collection](http://hacksoflife.blogspot.com/2006/12/garbage-collection-memory-management-by.html).

Let me take a step back.

X-Plane uses a series of custom allocation strategies in places where we know things that the system allocator cannot know (e.g. "all of these blocks have the same life-span", or "these allocations don't have to be thread-safe"), and this got us a win in terms of less CPU time being spent allocating.

X-Plane also uses a quad-tree-like structure to cull our scene-graph. The cull operation is very fast, and so (not surprisingly) when you profile the scene graph, the 'hot spots' in the quad tree are all L2 cache misses. (You can try this on X-Plane 9, just turn down objects to clear out driver time and see in-sim work.) In other words, the limiting factor on plowing through the scene graph is not CPU processing, rather it's keeping the CPU fed with more quad-tree nodes from memory.

The nodes in the quad tree come from one of these custom allocation strategies.

So my clever plan was: modify the custom allocator to try to keep quad-tree nodes together in memory, improving locality, improving cache hits, improving framerate, and proving once again that all of that misery I go through managing my own memory (and chasing down memory scribbles of my own creation) is totally worth it!

Unfortunately, my clever plan made things worse.

It turns out that the allocation pattern I had before was actually better than the one I very carefully planned out. The central problem with most parts of X-Plane's scene graph is: you don't know what "stuff" is going to come out of the user's installed custom scenery, and you don't know precisely what will and won't be drawn. Thus while there is some optimal way to set up the scene graph, you can't precompute it, and you can only come close with heuristics.

In this case the heuristic I had before (allocation order will be similar to draw order) turns out to be surprisingly good, and the allocation order I replaced it with (keep small bits of the scene graph separate so they can remain local within themselves later) was worse.

So...until next time, L2 cache, just know that somewhere, deep in my underground lair, I will be plotting to stuff you with good data. (Until then, I may have to go stuff myself with scotch.)

Another fine moment in the age-old war between the human mind and complex systems.




ReplyDeleteHuman Mind: 0 Complex System: 1

Grokked Knowledge: priceless

:-)

Paul.

Hi Paul,


ReplyDeleteYou may have left off some zeros after that '1'. :-)