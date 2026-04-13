---
title: Mesh Simplification Part III - Simplifying A Triangulation
url: http://hacksoflife.blogspot.com/2011/05/mesh-simplification-part-iii.html
author: Benjamin Supnik
published: '2011-05-26'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Consider a constrained Delaunay triangulation, where our arrangement edges have been replaced with triangulation constraints, and there are no free vertices (nor are there vertices in the triangulation that don't have at least one incident constraint).

We can now use an idea from the

[previously referenced](http://www.springerlink.com/content/f3j0667118n71567/)paper: given a pair of constraints forming a curve pqr that we want to simplify into pr, if there exist any vertices that might be on the edge or in the interior of triangle pqr, then they must be adjacent to q in the triangulation (and between pq and pr on the accute side of pqr).

This means that we can simply circulate vertex q to search for squatters. The triangulation is the index.

Why does this work? Well, consider the case where there exists a vertex X inside triangle PQR that is not adjacent to Q. You can't have free vertices in a triangulation; the act of triangulating out X is going to create at least one link between Q and X; the only way that this will not happen is if there is already some other point inside PQR that is closer to Q than X (and in that case, we fail for that other point).

The triangulation also has the nice property that when we remove a vertex X, we can reconsider its adjacent vertices to see if X was a squatter of those other vertices. This works because if X is a squatter of Q and there are no other squatters (thus removing X "unlocks" Q) then X and Q must be connected.

Implementation Notes

In my case I have one other implementation consideration besides the usual requirements: in my case, I have a many-to-many link between vertices in my original arrangement and vertices in my triangulation. Some triangulation vertices will not have original nodes because they represent subdivision of the triangulation to improve elevation data. And some original arrangement vertices will not be in the triangulation due to simplification of the triangulation's constraints.

The problem is: how do we work backward from a triangulation triangle to an original arrangement face? Given a triangle with a constraint on one side, we need to figure out what arrangement halfedge(s) it links to.

In order to keep this "back-link" unambiguous, we cannot remove all of the degree 2 vertices from a poly-line of original edge segments. We need to leave at least one "poly-line interior" vertex in place to disambiguate two paths between vertices in the arrangement. (This case happens a lot when we have closed loops.)

In practice, we could never remove the poly-line interior vertices from all paths anyway (because they would collapse to zero paths) but in practice, we don't want to remove them from any poly-line because it makes resolving the original arrangement face more difficult.

A picture would say more than 1000 words :).

ReplyDeleteThe subject sounds interesting but to lazy to try to visualize what you are saying.