---
title: Mesh Simplification Part II - Arrangement Simplification
url: http://hacksoflife.blogspot.com/2011/05/mesh-simplification-part-i-arrangement.html
author: Benjamin Supnik
published: '2011-05-26'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

To simplify an arrangement, therefore, what we really need is a good spatial index to make searching for squatters fast.

Previously I had used a quadtree-like structure, but I seem to be getting better results using a Delaunay triangulation. (This idea is based on the CGAL point_set_2 class).

- We insert every vertex of our arrangement into a Delaunay triangulation.
- When we want to check for squatters, we find the minimum circle enclosing the triangle pqr (where pqr is the curve pair we want to simplify to pr) and search the triangulation for nodes inside the circle.

Implementation Details

For my implementation using arrangements, there are a few quirks:

- I use my own point set; CGAL's point set uses a stack-based depth-first search that tends to flood the stack for large data sets.
- I do not re-queue previously "blocked" points as squatters are removed. This would be a nice feature to add at some point (but is not easily added with a mere index).
- I abuse CGAL's "merge_edge" routine to do the simplification. Edge merge was meant for collinear curves; in my case I pre-ensure that it is a safe operation. The advantage of using merge_edge vs. actually inserting the new edges and removing the old ones is speed and stability: no faces are created or removed, thus face data stays stable, and no geometry tests are needed to determine what holes go in what face, etc.
- Because I am edge-merging, I can't merge two edges that have opposite x-monotone "direction" - thus some details won't get simplified. This is a limitation of CGAL's arrangement interface.

Since the method recycles two of the four half-edges in the merge, if the first half of the curve points in the opposite direction of the merged curve, the merge is changing the half-edge's direction.

Could this case happen if the merged edge had the same path as the original two edges? No. In order for the direction to change, the two underlying curves cannot be summed to a single curve that is still x-monotone, which is a requirement for CGAL's arrangement.

## No comments:

## Post a Comment