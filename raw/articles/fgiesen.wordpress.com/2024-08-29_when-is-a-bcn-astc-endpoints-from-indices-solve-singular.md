---
title: When is a BCn/ASTC endpoints-from-indices solve singular?
url: https://fgiesen.wordpress.com/2024/08/29/when-is-a-bcn-astc-endpoints-from-indices-solve-singular/
published: '2024-08-29'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# When is a BCn/ASTC endpoints-from-indices solve singular?

This is a result I must have re-derived at least 4 times by now in various ways, but this time I’m writing it down so I just have a link next time. All right. If you’re encoding a BCn or ASTC block and are trying to find optimal endpoints (in a least-squares sense) for a given set of weights, you are led to the linear least-squares problem

where A is a n-by-2 matrix of weights, X is a 2-by-c matrix of endpoints we’re solving for where c is the number of color channels (most commonly 3 or 4), B is a n-by-c matrix of desired pixel values, and A looks like

Solving this leads us to the Normal Equations

which is ultimately a regular linear system with multiple right-hand sides. is just a 2×2 matrix, so solving this is very easy (Cramer’s rule is the most popular approach). The only problem being, of course, that this matrix can end up being singular. There’s one obvious case where

ends up singular: when all weights are the same (making the two columns of A linearly dependent). The question is, are there any other cases where we end up with a singular system?


In short: no. Write (because it’s symmetric), then its determinant is


which per [Lagrange’s Identity](https://en.wikipedia.org/wiki/Lagrange%27s_identity) equals

That’s a sum of squares, therefore non-negative terms, and the determinant can only be 0 if all the summands are 0. However, we can simplify

and therefore the determinant is 0 (and our system singular) if and only if all the weights are the same, since we’re summing over all possible pairs of weights and a single pair with a non-zero difference is sufficient to make our sum positive.