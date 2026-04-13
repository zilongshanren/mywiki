---
title: merge_edge - Fixed, Sort of.
url: http://hacksoflife.blogspot.com/2011/08/mergeedge-fixed-sort-of.html
author: Benjamin Supnik
published: '2011-08-29'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

A while ago I wrote that you


The issue is that CGAL caches the direction of a half-edge and doesn't invalidate the cache when you merge the edge. Since it is replacing the curve of one of the two edges (the other is deleted) the cache could get out of sync with the curve, which causes chaos.


The work-around requires that you know which of two edges is going to be saved. If you pass two halfedges h1 and h2 such that h1's target is h2's source (and that point is the vertex to be removed) then h1 and its twin are kept (and represent the merged edge) and h2 (and its twin) are deleted.


If h1 has the same direction as the new curve, you can simply merge h1,h2. But if they run in opposite directions this means that h1 and h2 must not have the same direction (because two same-direction curves add up to the same direction curve). If h1 does not match the curve then h2 does . If h2 matches the curve then h2's twin matches the curve's opposite. Therefore the wokr-around when the curve and h1 don't match is to merge h2's twin, h1's twin with the curve reversed.

[can't use CGAL's merge_edge](http://hacksoflife.blogspot.com/2008/10/cgla-abusing-mergeedge.html)if the two half-edges run in opposite X directions. It turns out this isn't entirely true; as of CGAL 3.4 (yes, it's been a while since we went to latest) you can merge if you're very careful.The issue is that CGAL caches the direction of a half-edge and doesn't invalidate the cache when you merge the edge. Since it is replacing the curve of one of the two edges (the other is deleted) the cache could get out of sync with the curve, which causes chaos.

The work-around requires that you know which of two edges is going to be saved. If you pass two halfedges h1 and h2 such that h1's target is h2's source (and that point is the vertex to be removed) then h1 and its twin are kept (and represent the merged edge) and h2 (and its twin) are deleted.

If h1 has the same direction as the new curve, you can simply merge h1,h2. But if they run in opposite directions this means that h1 and h2 must not have the same direction (because two same-direction curves add up to the same direction curve). If h1 does not match the curve then h2 does . If h2 matches the curve then h2's twin matches the curve's opposite. Therefore the wokr-around when the curve and h1 don't match is to merge h2's twin, h1's twin with the curve reversed.

## No comments:

## Post a Comment