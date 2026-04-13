---
title: Supersampling and antialiasing distance fields
url: http://c0de517e.blogspot.com/2012/10/supersampling-and-antialiasing-distance.html
published: '2012-10-07'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Just found this note cleaning up my stuff, thought I might as well post it...



We had some issues with using signed distance fields for font rendering and antialiasing. The idea is to conceptually similar to doing a two dimentional marching squares and then computing the area of the resulting convex polygon.

If you can't (or don't want to read) my horrible note, the "algorithm" samples four taps of the distance field (use ddx/ddy UV for the width) on a (unit) square and then walks the vertices and edges of the square counterclockwise (first a vertex, then an edge, then the next vertex and so on).



The polygon is constructed by taking the coordinates of all the vertices that are inside the distance field and computing an intersection point for all the edges that are between two in-out vertices. The polygon area (which equals the coverage) is computed incrementally using the determinant method. All unrolled in a shader.

*Jason Peng, an incredibly talented UBC student implemented this at Capcom Vancouver. He tells me it worked :)*



*P.S. You'll notice that I write counterclockwise and then draw all the arrows clockwise... :) Stupid me.*

## No comments:

Post a Comment