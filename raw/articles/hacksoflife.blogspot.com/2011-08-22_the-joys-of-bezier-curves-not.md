---
title: The Joys of Bezier Curves [NOT]
url: http://hacksoflife.blogspot.com/2011/08/joys-of-bezier-curves-not.html
author: Benjamin Supnik
published: '2011-08-22'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Someone please remind me why bezier curves are such a common parametric curve choice in the computer graphics world? Some of their charming properties...



You can also intersect a bezier curve with a horizontal or vertical line - to do this you fill in the line coordinate and use the cubic equation (which does have a long but scary analytical solution) to find the roots. (See


Well, at least they're not riddled with

- No analytic solution for the curve's length. The integral will make you cry.
- No analytic solution for the intersection of two curves. Well,
[this guy](http://www.truetex.com/bezint.htm)found one, but he's not going to tell you what it is. - No solution to find the closest point of encounter between two disjoint curves.
- No analytic solution to find the parametric value to split the bezier at a particular known length interval (e.g. into two halves of equal length).

You can also intersect a bezier curve with a horizontal or vertical line - to do this you fill in the line coordinate and use the cubic equation (which does have a long but scary analytical solution) to find the roots. (See

[here](http://dev.x-plane.com/cgit/cgit.cgi/xptools.git/plain/src/Utils/CompGeomDefs2.h)for code.)Well, at least they're not riddled with

## No comments:

## Post a Comment