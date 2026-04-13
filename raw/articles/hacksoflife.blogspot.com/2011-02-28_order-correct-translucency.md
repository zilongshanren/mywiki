---
title: Order-Correct Translucency
url: http://hacksoflife.blogspot.com/2011/02/order-correct-translucency.html
author: Benjamin Supnik
published: '2011-02-28'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[order independent transparency demo](http://developer.amd.com/samples/demos/pages/atiradeonhd5800seriesrealtimedemos.aspx), I nearly wet myself. Translucency has been the bane of X-Plane authors for years. The problem is that translucent surfaces remove hidden surfaces behind them, leading to artifacts. The thought of on-hardware OIT was tantalizing.

That is, until I found out how the tech works. My understanding is that OIT is implemented by "writing your own back-end" - that is, instead of shading into a framebuffer, you write fragments into a 'deep' framebuffer by hand, using compute-shader-style ops to create linked lists of fragments. (That is, fragments live in a general store and the framebuffer is really list heads.) In a post processing pass, you go through the 'buckets' (that is, the linked lists) and sort out what you drew.

That's a lot more back-end than I wanted...as a [spoiled, lazy] app developer I was hoping for glEnable(GL_MAGIC_OIT_EXT) - but no such luck. The real issue is that, since our product already does a lot of 'back end' tricks within OpenGL, the cost of getting our shaders to run in a compute-style environment might be a bit high. (This is looking less burdensome with some of the newer extensions, but it still seems to me that it would be difficult to port legacy apps to OIT-style rendering without having compute-shader features like atomic counters inside the GLSL shading environment.)

As a side note, I also looked closely at depth peeling and even hacking the blend equation (e.g. accumulate and average) and both would probably be producable for X-Plane, which tends not to have that much translucent overlap - the most common case for us is windows.

The Traditional Approach - Automated

Now the traditional approach to translucency in X-Plane goes something like this:

- Force opaque drawing first.
- Use one-sided drawing and order the translucent polygons so they appear from back to front from any viewpoint.

Well, it turns out that this approach can be generalized: as long as none of our triangles intersect (except at their edges and corners), given any two triangles, we can always find a draw order between them that is correct. Given a set of triangles, we can always sort the whole mesh to be appropriately back-to-front. (At least, that's my theory until someone proves me wrong.)

There are basically three cases:

- Triangle B is fully on one side or the other of triangle A's plane. B should be clearly before or after A depending on which side it's on.
- Triangle A is fully on one side or the other of triangle B's plane. A should be clearly before or after B depending on which side it's on.
- Triangle B and A are both on one side of each other's plane; we can use either triangle to determine correct order - they will not conflict. (That is, this is a disjoint case, and either the two triangles are going to give you the same answer or they're facing in opposite directions and thus no visible at the same time.)

The ability to find this sort order depends on using one-sided triangles - this is what lets us decouple the sort order for two opposite directions. By definition if a triangle is visible to a vector V, its back side is visible to -V.

This approach of course doesn't solve all problems:

- Animation can deform the mesh in a way that violates our correct order.
- Multiple unrelated objects still need a relative ordering that makes sense.

Just a touch of angst...I'm no theoretician, and I can't help but wonder if there is a screwy case that this doesn't handle. In particular, the sort order needs to be a strict weak ordering or we're going to get goofy results, and I'm not entirely sure that it is.

## No comments:

## Post a Comment