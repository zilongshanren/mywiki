---
title: Mesh Simplification Part I - It's All About Squatters
url: http://hacksoflife.blogspot.com/2011/05/mesh-simplification-part-i-its-all.html
author: Benjamin Supnik
published: '2011-05-26'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Given an arrangement (that is, a set of line segments and possibly free points such that line segments don't cross or end in each other's interiors) we can iteratively simplify the map by replacing adjacent pairs of line segments with a "short-cut" (e.g. replace line segments pq and qr with pr) given the following conditions:

- The degree of vertex q is 2 (e.g. only pq and qr emerge from q).
- Line segment pr is not already in the arrangement.
- If p, q, and r are not collinear are no points in the interior of triangle pqr (nor directly between p and r). By definition there can't be any points on pq and qr.

- There is some kind of island geometry (or free vertex) and it will be on the wrong side of pqr after simplification, or
- The geometry "connects" to the world outside pr and pr will intersect at least one segment.

Given this, we can build

[an iterative algorithm for simplifying a mesh](http://www.springerlink.com/content/f3j0667118n71567/):

- Put every vertex that passes these tests into a queue, based on the error introduced by removing it.
- Remove the first vertex.
- Requeue neighboring vertices based on changed error metrics.

The Zone Is Not What We Want

Previously I had coded similar logic via a zone visiting calculation - that is, finding every face, line and point that the edge pr would intersect. This had a few problems:

- Arrangement zone calculations are really expensive. Given a simple polygon with X sides, we may have to do as many as X zone calculations (if any vertex is eligible for removal) and the zone calculation iterates the polygon boundary. Thus we have an O(N^2) calculation, which is really painful for large polygons made of a large number of small sides. (Sadly, that is precisely what my data tends to be.)
- The zone calculation is wrong; even if we don't crash into anything while computing the zone, if the zone has holes that would be on inside of triangle PQR then we still should not be simplifying. So we would have to iterate over holes as well as calculate the zone.

## No comments:

## Post a Comment