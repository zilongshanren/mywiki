---
title: Balancing Dynamic Trees
url: https://box2d.org/posts/2014/08/balancing-dynamic-trees/
published: '2014-08-07'
source_blog: Box2D
source_site: https://box2d.org/
category: graphics
fetched: '2026-04-19'
---

I received this question on LinkedIn:

I’m working on a 3d dynamic aabb tree based on the concepts of Presson’s bullet contribution. I came across a bullet forum thread in which Dirk recommended looking at your box2d implementation. I noticed the major difference is that box2d is a balanced tree using a surface area heuristic while bullet’s is unbalanced with manhattan distance heuristic.

My guess is that keeping your tree balanced resulted in increased maintenance overhead but decreased tree query times. Was there any benchmark of this anywhere that measured if the tradeoff was worth it? Or if there was any other motivation for implementing it this way?

Here is my reply:

A dynamic tree must be actively balanced through rotations (like AVL trees), otherwise you can easily have the tree degenerate into a very long linked list.

For example, imagine a world with many boxes in a row. Say 100 boxes extending along the x-axis. If the boxes are added to the tree at the origin and then incrementally along the x-axis, you will end up not with a tree, but a linked list with 100 elements. You do not need to run a benchmark to know this will yield horrible query performance. Not only will the performance be bad, but you will also need a large stack to process queries (ray casts or overlap tests).

This may sound like a contrived example, but this actually happens a lot in games. Imagine a side scrolling game, as the player moves through the world, objects are added in a linear fashion.

The Bullet code attempts to keep the tree balanced through random removal and insertions. In my tests, I found situations where this would take thousands of iterations to balance the tree reasonably. So I decided to implement tree rotations like you will find in AVL trees. It is actually a little bit simpler since there is no strict right-left sorting necessary.