---
title: Triangle rasterization in homogeneous coordinates gotcha
url: https://anteru.net/blog/2010/triangle-rasterization-in-homogeneous-coordinates-gotcha
published: '2010-05-03'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

There’s a very difficult to find bug you might encounter when you try to implement triangle rasterization in homogeneous coordinates (as described in “[Triangle scan conversion using 2D homogeneous coordinates](http://portal.acm.org/citation.cfm?id=258723)“.) You’ll face the problem if you transpose the interpolation matrix by chance – either because you forgot the transpose when doing the [standard 3x3 matrix inverse](http://en.wikipedia.org/wiki/Matrix_inverse#Inversion_of_3.C3.973_matrices), or because you multiply your vectors from the wrong side onto your matrix.

Anyway, what happens is that you suddenly get the same z-Value across your triangle. The weird thing is that the z-Value is actually correct for one of the vertices, so if you have pixel-sized triangles, everything will work out fine. It only breaks down once you interpolate across the triangle, as you always wind up with the same value.

![Triangle depth interpolation with transposed interpolation matrix Triangle depth interpolation with transposed interpolation matrix, each fragment in a triangle gets the same depth value.](../../assets/fa46a8aada35c06f.png)

Short explanation why this is difficult to track down: First of all, it’s the correct z-Value after all, and the matrix is far from symmetric, so you wouldn’t expect that the transpose would end up anywhere near the correct result. Second, the matrix condition is typically not too good, so numerical problems are actually something you’ll face – I spent quite some time to improve the condition of the matrix as well as trying out several inversion methods, just to make sure that numerical problems are not the problem. Finally, you have to use the colums/rows (depending on your layout) of the matrix for the edge half-space tests, so you can be sure that you have computed the entries of the matrix correctly.

With the properly transposed matrix, everything works fine. Small hint: You need to interpolate 1 to get w, for which you can save the matrix multiply and just compute the sum, which saves several multiplications with 1. Here’s the correct result for comparison:

![Triangle depth interpolation with correct interpolation matrix Triangle depth interpolation with correct interpolation matrix, depth varies smoothly accross a triangle](../../assets/28f78b03e35c9498.png)