---
title: A Simple, and Trivially Parallelizable Triangle Rasterization Approach
url: https://erkaman.github.io/posts/fast_triangle_rasterization.html
source_blog: Eric Arnebäck
source_site: https://erkaman.github.io/
category: graphics
fetched: '2026-04-19'
---

$\newcommand{\mvec}[1]{\mathbf{#1}}\newcommand{\gvec}[1]{\boldsymbol{#1}}\definecolor{eqcol2}{RGB}{114,0,172}\definecolor{eqcol1}{RGB}{172,0,114}\definecolor{eqcol3}{RGB}{0,172,114}\definecolor{eqcol4}{RGB}{230,190,120}$In this article, a triangle rasterization algorithm that is easy to implement, yet trivial to parallelize is described. The algorithm is as follows: it turns out that it is not difficult to test whether an arbitrary point is inside a triangle. Armed with such a test, a triangle can easily be rasterized by first finding the bounding box of the triangle, and then only rasterizing the pixels inside this bounding box that pass the test.

Thus, we first need to derive a test that allows us to check whether some point is inside a triangle. Consider the triangle with the vertices $\mvec{v_0}$, $\mvec{v_1}$, $\mvec{v_2}$

Let us in particular consider the edge $(\mvec{v_0}, \mvec{v_1})$. A point is either on one side of the edge, or on the other side. The points on the correct side will be in the red area

Certainly, a point that is not in the red area cannot be inside the
triangle. However, observe that not all points in the red area will be
inside the triangle, For instance, the points on the wrong side of the
edge $(\mvec{v_1}, \mvec{v_2})$ will be outside the triangle. The
points that are on the correct sides of the edges $(\mvec{v_0},
\mvec{v_1})$ *and* $(\mvec{v_1}, \mvec{v_2})$ are in the below red area

However, we are not yet satisfied; the red area still
contains areas that are outside the triangle. In our final red area,
only points that are on the correct side of $(\mvec{v_0},
\mvec{v_1})$, $(\mvec{v_1}, \mvec{v_2})$, *and* $(\mvec{v_2},
\mvec{v_0})$ are in the red area:

So we have described a simple test that allows us to check whether a point is inside the triangle: it must be on the correct side of all the three edges. Next, we need a way to check whether some point is on the correct side of a single edge.

The point $\mvec{p}$ is clearly on the correct side of the edge $(\mvec{v_0},\mvec{v_1})$, and it is easy to check for this. We define $\mvec{p} = (p_x, p_y, 0)$, $\mvec{v_0} = (v_{0x}, v_{0y}, 0)$, $\mvec{v_1} = (v_{1x}, v_{1y}, 0)$, so that the $z$-component is always zero. Consider now the cross product $(\mvec{v_1}-\mvec{v_0}) \times (\mvec{p}-\mvec{v_0})$:

by
the [right-hand
rule](https://en.wikipedia.org/wiki/Cross_product#Definition), the $z$-component of this cross product must be positive if
$\mvec{p}$ is on the correct side of the edge. If it is on the wrong
side, the below situation will occur.

Thus, if the $z$-component of the cross product is negative, then the point cannot possibly be inside the triangle. Finally, the $z$-component of this cross product is calculated as \[ ((\mvec{v_1}-\mvec{v_0}) \times (\mvec{p}-\mvec{v_0}))_z = (v_{1x}-v_{0x})(p_{y}-v_{0y}) - (v_{1y} - v_{0y})(p_{x}-v_{0x}) \] if this value is positive, then the point is on the correct side, otherwise, it is not inside the triangle. We repeat this test for all the three edges, if it passes all three, the point must be contained in the triangle.

Finally, we can now use this test to implement a rasterization algorithm. We find the smallest axis-aligned bounding box that contains the triangle, and then loop over all pixels contained in the box. For each pixel center, we perform the three edge tests, and if all three pass, the pixel is rasterized.

This rasterization algorithm has the advantage that it is trivial to
parallelize. It can be implemented in a compute shader or CUDA kernel
as follows: for every pixel in the bounding box, a GPU-thread is
launched. Every thread checks whether all three edge tests pass, and
if so, rasterize the pixel. This algorithm requires no synchronization
between the threads whatsoever, and thus it will be very fast. It is
also possible to implement a parallel algorithm on the CPU using
SSE or AVX. Such an implementation is provided in the [source code](https://github.com/Erkaman/sse-avx-rasterization)
accompanying this article.