---
title: When Good Floating Point Goes Bad?
url: http://hacksoflife.blogspot.com/2010/09/when-good-floating-point-goes-bad.html
author: Benjamin Supnik
published: '2010-09-27'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

- For real floating point data, dot products may not go to zero; the zero dot product is at the heart of "is this a left or right turn" and "which side of a line am I on". Rounding errors may force points to fall to one side of a line or another.
- Even more weirdly, there's no guarantee that points will consistently fall on one side of a line or another; the rounding errors need to be treated as effectively random. A point that is moving across a line may give 'jittery' results as the point slowly crosses the line.
- Order matters. Given the same theoretical line, defining it by swapping the input points (e.g. line AB instead of BA) may have unpredictable effects on side-of tests for very small distances.
- Finally, there is no function more hellish than intersection. The more parallel the lines, the more completely insane the intersection results become. Serious paranoia is advised when dealing with intersections, because the routines can give you a positive result ("yes there was an intersection") with lunatic results ("and the intersection is on Mars"). I usually cope with this by using a dot product test to case out the near-collinear case, which is then handled in a different algorithm that doesn't require clean intersections.

## Monday, September 27, 2010


### When Good Floating Point Goes Bad?

We have a handful of linear algebra/geometry routines in X-Plane that simplify writing geometric tests. In their heart, they almost all turn into dot products. So: when can we not trust them?


## No comments:

## Post a Comment