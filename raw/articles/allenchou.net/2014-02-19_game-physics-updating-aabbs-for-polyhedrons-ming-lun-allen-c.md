---
title: 'Game Physics: Updating AABBs for Polyhedrons | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2014/02/game-physics-updating-aabbs-for-polyhedrons/
author: Allen Chou
published: '2014-02-19'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

In order for most broadphases to work, it is important to update AABBs of colliders after their position and orientation have changed. This post will present 3 methods to update AABBs for, in particular, colliders of __arbitrary polyhedron__ shapes: the brute-force approach, approximation by local AABB, and the support function approach.

### The Brute-Force Approach

This is probably the most straightforward approach of updating a polyhedron’s AABB. You simply loop through all vertices in global coordinates and extract the extrema in all principle axes.

aabb.minPoint.Set( FLT_MAX, FLT_MAX, FLT_MAX); aabb.maxPoint.Set(-FLT_MAX, -FLT_MAX, -FLT_MAX); for (auto Vec3 &vert : mesh.verts) { const Vec3 globalPos = body.LocalToGlobal(vert); aabb.minPoint.x = Min(aabb.minPoint.x, globalPos.x); aabb.minPoint.y = Min(aabb.minPoint.y, globalPos.y); aabb.minPoint.z = Min(aabb.minPoint.z, globalPos.z); aabb.maxPoint.x = Max(aabb.maxPoint.x, globalPos.x); aabb.maxPoint.y = Max(aabb.maxPoint.y, globalPos.y); aabb.maxPoint.z = Max(aabb.maxPoint.z, globalPos.z); }

It’s fast to implement and easy to understand. However, this approach does not scale very well with numbers of vertices.


### Approximation by Local AABB

Another common approach to update a polyhedron’s AABB is to approximate the AABB using the local AABB that is computed only once at the start of physics simulation, or even loaded from pre-computed data. Then, we use the AABB of the transformed local AABB as an approximation in global coordinates.

This approach is fast and constant-time. However, it is an approximation and would generate an AABB that is typically larger than the exact AABB, possibly producing more false positives during broadphase.

Note that this approach can be applied to any types of colliders, not just polyhedrons.

### The Support Function Approach

Last but not least, the support function approach.

We convert the principle axes (both positive and negative directions) from global coordinates into local coordinates of the collider. Next, we use these directions to find 6 support points. Finally, we convert these support points back to global coordinates. Each support point in global coordinates corresponds to one side of the AABB.

Of course, to gain any advantage in performance, the support function should be implemented using an approach better than the trivial brute-force method; for example, the hill-climbing method using half edges as mentioned in [this post](http://allenchou.net/2014/02/game-physics-implementing-support-function-for-polyhedrons-using-half-edges/).

const Vec3 xNeg(-1.0f, 0.0f, 0.0f); const Vec3 yNeg( 0.0f, -1.0f, 0.0f); const Vec3 zNeg( 0.0f, 0.0f, -1.0f); const Vec3 xPos( 1.0f, 0.0f, 0.0f); const Vec3 yPos( 0.0f, 1.0f, 0.0f); const Vec3 zPos( 0.0f, 0.0f, 1.0f); const Vec3 xNegLocal = body.GlobalToLocalVec(xNeg); const Vec3 yNegLocal = body.GlobalToLocalVec(yNeg); const Vec3 zNegLocal = body.GlobalToLocalVec(zNeg); const Vec3 xPosLocal = body.GlobalToLocalVec(xPos); const Vec3 yPosLocal = body.GlobalToLocalVec(yPos); const Vec3 zPosLocal = body.GlobalToLocalVec(zPos); aabb.minPoint.x = body.LocalToGlobal(Support(xNegLocal)).x; aabb.minPoint.y = body.LocalToGlobal(Support(yNegLocal)).y; aabb.minPoint.z = body.LocalToGlobal(Support(zNegLocal)).z; aabb.maxPoint.x = body.LocalToGlobal(Support(xPosLocal)).x; aabb.maxPoint.y = body.LocalToGlobal(Support(yPosLocal)).y; aabb.maxPoint.z = body.LocalToGlobal(Support(zPosLocal)).z;

For polyhedrons of reasonably many vertices, the computation time of this approach should lie between the brute-force approach and approximation by local AABB.

For polyhedrons with just a few vertices, this approach could be slower than the brute-force approach. But if your polyhedron has that few verticies, you shouldn’t be worrying about the performance of updating its AABB anyway.

### End of Updating AABBs for Polyhedrons

There is no correct or the best approach to update AABBs of polyhedrons. It all depends on the scenarios of your physics simulation. You may profile your simulation with all of these approaches and decide which one works the best for you.