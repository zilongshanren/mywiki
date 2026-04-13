---
title: How to Jam an Arrangement_2 into a General_polygon_set_2
url: http://hacksoflife.blogspot.com/2013/03/how-to-jam-arrangement2-into.html
author: Benjamin Supnik
published: '2013-03-14'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I spent about three hours yesterday tracking down a weird bug in CGAL - I have code that builds a general polygon set out of an arrangement, exports the polygons, and weirdly the polygons had duplicate points. This is an impossibility for a valid arrangement.


To my annoyance, I discovered today as I went to write the bug up that I knew about this bug...over


Basically if you are going to build a general polygon set by providing a pre-built arrangement, there are two things you must do:


(After redundant edge removal, the arrangement will contain no antennas, so it will always be possible to get consistency on both sides of a CCB.)To my annoyance, I discovered today as I went to write the bug up that I knew about this bug...over

[three years ago](http://www.hacksoflife.blogspot.com/2009/07/cgal-curves-faces-and-caution.html). :-( I get annoyed when I search for the answer to an obscure OpenGL problem and find my own post (e.g. I'm not going to find anything I didn't already know), but it's even more annoying to waste hours on the bug and then have that happen.Basically if you are going to build a general polygon set by providing a pre-built arrangement, there are two things you must do:

- Remove redundant edges - the GPS code assumes that the arrangement doesn't have needless edges (which will screw up traversal). Fortunately, the GPS code has a utility to do this, which I just call.
- Then you have to ensure that the direction of the underlying curves along the various edges are
*consistent*- that is, for a given counter-clockwise boundary, every underlying curve goes either with or against the edge.

I wrote code to enforce this second condition by flipping the curve of any halfedge where (1) the curve goes against the halfedge and (2) the halfedge is adjacent to the "contained" side of the map.

With this, polygon set operations work on arbitrary map input.

#### Why Did You Try This?

Forcing pre-made arrangements into polygon sets requires sub-classing the general polygon set template instantiation to get direect access to things like the arrangement, and it's not particularly safe. It also requires your arrangement to have the containment flag on the face data mixed in. Why go to the trouble? I did this for two reasons:

- Sometimes the polygonal set data I want to process came from an arrangement, and that arrangement is fairly huge. Having to construct the arrangement out of polygons the normal way requires geometry tests - topology data would be lost and rediscovered. For big maps this is really performance-painful.
- I have some operations that work on arrangements that are precursors to boolean sets. For example, the airport surface area data are fundamentally polygon sets (e.g. in the set is the airport surface area) but some of the constructive processing (e.g. simplifying the contour) run on arrangements.

## No comments:

## Post a Comment