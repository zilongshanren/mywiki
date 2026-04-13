---
title: 'Game Physics: Contact Generation – EPA | Ming-Lun "Allen" Chou | 周明倫'
url: https://allenchou.net/2013/12/game-physics-contact-generation-epa/
author: Allen Chou
published: '2013-12-28'
source_blog: Ming-Lun "Allen" Chou | 周明倫
source_site: https://allenchou.net
category: game programming
fetched: '2026-04-13'
---

This post is part of my [Game Physics Series](http://allenchou.net/game-physics-series/).

### Contact Data

[GJK](http://allenchou.net/2013/12/game-physics-collision-detection-gjk/) tells us whether two colliders are colliding and nothing more. In order to correctly resolve collision, we would need to generate contacts. As [mentioned earlier](http://allenchou.net/2013/12/game-physics-introduction/), contacts are approximation of the touching region of two colliding shapes, and the collection of contacts between two colliders are collectively called a contact manifold.

A typical piece of contact data contains the following information:

- Two
__contact points__in__world space__, each representing the deepest penetrating point of one collider. (positions x2) - Two
__contact points__in__local spaces__of individual colliders, each corresponding to a contact point in world space. This information is crucial for maintaining persistent contacts. (positions x2) __Contact normal__representing the “best direction” to separate the two colliding colliders. (vector x1)- Two
__contact tangents__perpendicular to each other and the contact normal. These vectors are used to resolve the frictional part of collision resolution. (vectors x2) -
__Penetration depth__, a scalar value that represents how deep the overlap of the two colliders is. (float x1)


### Contact Generation

So how do we generate the contacts? My post on [CSO & Support Function](http://allenchou.net/2013/12/game-physics-collision-detection-csos-support-functions/) showed that when two colliders are colliding, their CSO contains the origin. We can find a closest point on the CSO’s boundary that is closest to the origin. Since the closest point is on the CSO’s boundary, it must be a valid output of the CSO’s support function; the corresponding two individual support function results from the two colliders are the two __contact points__, which we will store in both world space and local spaces of individual colliders. The distance between the closest point and the origin is the __penetration depth__. Moreover, the vector normal to the CSO’s boundary at the closest point is our __contact normal__ in world space.

There are multiple ways to generate a pair of tangent vectors from a normal vector to form an orthonormal basis. The method I will show here is called the “consistent method”, because it always gives the same pair of tangent vectors for the same normal vector. The idea is very easy: we find the axis of “least significant component” of the normal vector, and then take the cross product of that axis and the normal vector to produce the first tangent vector, which can in turn let us obtain a second tangent vector by taking the cross product of the normal and the first tangent vector.

// find least axis of least significant component const float absX = std::fabs(n.x); const float absY = std::fabs(n.y); const float absZ = std::fabs(n.z); Vec3 axis(0.0f, 0.0f, 0.0f); if (absX > absY) { if (absX > absZ) axis.x = 1.0f; // X > Y > Z, X > Z > Y else axis.z = 1.0f; // Z > X > Y } else { if (absY > absZ) axis.y = 1.0f; // Y > X > Z, Y > Z > X else axis.z = 1.0f; // Z > Y > X } // compute tangents t1 = n.Cross(axis).Normalized(); t2 = n.Cross(t1).Normalized();

[Edit]

As HorridOrc has pointed out in the comment, the method above doesn’t always work. Erin Catto proposed [another method](http://box2d.org/2014/02/computing-a-basis/) that is more efficient and always works.

if (n.x >= 0.57735f) t1.Set(n.y, -n.x, 0.0f); else t1.Set(0.0f, n.z, -n.y); t1.Normalize(); t2 = n.Cross(t1);

[/Edit]

Now we have one problem left: how do we find this closest point on the CSO’s boundary? This is what the Expanding Polytope Algorithm (EPA) is for.

### EPA

As it name suggests, EPA involves expanding a polytope iteratively. EPA finds a triangle with vertices on the CSO’s boundary, and we treat the projection of the origin onto this triangle as a good enough approximation of the closest point on the CSO’s boundary to the origin (it will be the exact closest point instead of an approximation if the two colliders are convex polyhedrons with finite vertices).

Below is essentially what EPA does:


- Take over the simplex from GJK when GJK terminated, and “blow up” the simplex to a tetrahedron if it contains less than 4 vertices.
- Use the 4 faces (triangles) of the tetrahedron to construct an initial polytope.
- Pick the closest face of the polytope to the origin.
- If the closest face is no closer (by a certain threshold) to the origin than the previously picked one, go to 8.
- Remove the closest face, use the face normal (outward pointing) as the search direction to find a support point on the CSO.
- Remove all faces from the polytope that can be “seen” by this new support point, and add new faces to cover up the “hole” on the polytope, where all new faces share the new support point as a common vertex (this is the
expandingpart of the algorithm).- Go to 3.
- Project the origin onto the closest triangle. This is our closest point to the origin on the CSO’s boundary. Compute the
[barycentric coordinates]of this closest point using the vertices from this triangle. The barycentric coordinates are linear combination coefficients of vertices from the triangle. For each collider, linearly combine the support points corresponding to the vertices of the triangle, using the same barycentric coordinates as coefficients. This gives us contact points on each collider in local space. We can then convert these contact points to world space.End EPA.

If a face can be “seen” from a point, it means that the point is on the positive halfspace of the plane that contains the face triangle. This test is simple: test if the dot product between the face normal (CCW winding assumed) and the vector from any one of the triangle’s vertex to the point is greater than zero.

const Vec3 v01 = face.v1 - face.v0; const Vec3 v02 = face.v2 - face.v0; const Vec3 normal = v01.Cross(v02); const bool faceCanBeSeenByPoint = normal.Dot(point - face.v0);

### Blowing Up Simplex to Tetrahedron

It is possible that the simplex passed down from GJK contains less than 4 vertices. Here is how we add more vertices to the simplex so it forms a tetrahedron at the beginning of EPA:

// simplex declaration from GJK Vec3 simplex[4]; // global support points Vec3 simplexA[4]; // local support points for collider A Vec3 simplexB[4]; // local support points for collider B unsigned numVerts; // small floating-point margin const float k_epsilon = 0.00001f; const float k_epsilonSq = k_epsilon * k_epsilon; // constant vector representing the origin const Vec3 k_origin(0.0f, 0.0f, 0.0f); // ... GJK stuff ... // blow up simplex to tetrahedron switch (numVerts) { // intentional ommision of "break" statements // for case fall-through case 1: // 6 principal directions static const Vec3 k_searchDirs[] = { Vec3( 1.0f, 0.0f, 0.0f), Vec3(-1.0f, 0.0f, 0.0f), Vec3( 0.0f, 1.0f, 0.0f), Vec3( 0.0f, -1.0f, 0.0f), Vec3( 0.0f, 0.0f, 1.0f), Vec3( 0.0f, 0.0f, -1.0f), }; // iterate until a good search direction is used for (const Vec3 &searchDir : k_searchDirs) { CsoSupport(colliderA, colliderB, searchDir, simplex[1], simplexA[1], simplexB[1]); // good search direction used, break if ((simplex[1] - simplex[0]).LengthSQ() >= k_epsilonSq) break; } // end of case 1 case 2: // 3 principal axes static const Vec3 k_axes[3] = { Vec3(1.0f, 0.0f, 0.0f), Vec3(0.0f, 1.0f, 0.0f), Vec3(0.0f, 0.0f, 1.0f) }; // line direction vector const Vec3 lineVec = simplex[1] - simplex[0]; // find least significant axis of line direction // 0 = x, 1 = y, 2 = z const unsinged leastSignificantAxis = LeastSignificantComponent(lineVec); // initial search direction Vec3 searchDir = lineVec.Cross(k_axes[leastSignificantAxis]); // build a rotation matrix of 60 degrees about line vector Mat3 rot = Mat3()::AxisAngle(PI_3, lineVec); // find up to 6 directions perpendicular to the line vector // until a good search direction is used for (int i = 0; i < 6; ++i) { CsoSupport(colliderA, colliderB, searchDir, simplex[2], simplexA[2], simplexB[2]); // good search direction used, break if (simplex[2].LengthSQ() > k_epsilonSq) break; // rotate search direction by 60 degrees searchDir = rot * searchDir; } // end of case 2 case 3: // use triangle normal as search direction const Vec3 v01 = simplex[1] - simplex[0]; const Vec3 v02 = simplex[2] - simplex[0]; Vec3 searchDir = v01.Cross(v02); CsoSupport(colliderA, colliderB, searchDir, simplex[3], simplexA[3], simplexB[3]); // search direction not good, use its opposite direction if (simplex[3].LengthSQ &lt; k_epsilonSq) { searchDir.Negate(); CsoSupport(colliderA, colliderB, searchDir, simplex[3], simplexA[3], simplexB[3]); } // end of case 3 } // fix tetrahedron winding // so that simplex[0]-simplex[1]-simplex[2] is CCW winding const Vec3 v30 = simplex[0] - simplex[3]; const Vec3 v31 = simplex[1] - simplex[3]; const Vec3 v32 = simplex[2] - simplex[3]; const float det = v30.Dot(v31.Cross(v32)); if (det > 0.0f) { std::swap(verts [0], verts [1]); std::swap(vertsA[0], vertsA[1]); std::swap(vertsB[0], vertsB[1]); }

### Visual Example

To help you have a better grasp of what EPA is doing, here is a visual example in 2D. The 2D version of EPA removes and adds line segments instead of triangles. Nevertheless, the purpose is the same: EPA is used to find the closest point to the origin on the CSO’s boundary. On a side note, there is a unified name to call triangles in the 3D case and line segments in the 2D case; we call them “facets”.

Below is our CSO and a polytope passed down from GJK, which is a triangle (2D simplex).

![EPA-1](../../assets/9f1d604937f811fd.png)


The closest facet is the top side of the triangle, so we expand in the direction from the origin to the closest point on the facet to the origin (essentially the outward-pointing normal of the facet). We find a support point in this direction (the black dot in the figure below).

![EPA-2](../../assets/9d37fbf8dd124aa1.png)


The top side of the triangle can be “seen” by the support point, so we remove it (the red dotted line segment), and we patch up the “hole” by connecting the support point with the end points of the now-broken polytope (the green line segments).

![EPA-3](../../assets/8b34d672c88ca90a.png)


Now our polytope is a quadralateral. The closest facet to the origin is on the bottom right. We repeat the same process and find a support point in that direction (the black dot).

![EPA-4](../../assets/ce7d5b1d84418d5f.png)


Again, we remove the facet that can be seen by the new support point and patch up the polytope by connecting points with the support point.

![EPA-5](../../assets/0578dd951a6c41e0.png)


Next, we attempt to find the closest facet of the new polytope to the origin, but we find out that the support point doesn’t bring us any further outside the polytope. Actually, we have two valid support points in this case (the two black dots). It doesn’t matter which support point our support function gives us; either way we can reach the conclusion that no further expansion is possible.

![EPA-6b](../../assets/c2b0f870061528d3.png)


Project the origin onto the closest facet. The distance between the origin and the closest point (the orange line segment) is the penetration depth, and the outward-pointing normal of the facet at the closest point is the contact normal (the red arrow).

![EPA-7](../../assets/30e05ebdcaf01364.png)


With this information, we can then generate the local and global contact points and contact tangents.

### Maintaining An Expanding Polytopes in 3D

In 2D, it is not hard to come up with a way to represent and maintain the expanding polytope. All you need to do is find a way to store a dynamic polygon (2D polytope), a list of line segments perhaps. In 3D, however, it is not so trivial. Some would argue that the most complicated part of EPA is actually maintaining an expanding polyhedron (3D polytope).

The method I prefer involves storing 3 lists: one vertex list, a triangle list, and a directed edge list (edge AB and edge BA are opposite and are considered different). All lists are initially empty. (I was originally introduced to this method by Andrew Alvarez, a member of [DigiPen Institute of Technology])

When we add a triangle to the polytope, we add the vertices to the vertex list and add the triangle to the triangle list.

To find the triangles that can be seen from a support point, we perform a linear walk through the triangle list and test all triangles. If a triangle can be seen by the point and is to be removed, add its 3 edges to the edge list (CCW order). When adding an edge to the edge list, if an opposite edge already exists in the list, we don’t add the edge and we remove the opposite edge.

After removing all triangles that can be seen from a support point, the edges in the edge list are the edges that need to be used to patch up the hole on the polytope. For each edge, add a new triangle formed by the support point and the edge (be careful about the winding). Finally, clear the edge list.

### End of EPA

Now you know how to generate contact information using EPA. I will move onto the resolution phase in the following posts.

Great article, thanks. Helped me implement and understand it for myself 🙂

Hi Allen, thanks for this series! Question for you, in the example code for blowing up to a tetrahedron, you find the closest point to the origin but don’t seem to use it anywhere, lines (51 and 97). Am I missing something maybe?

Good catch. Those two lines are unused variables I forgot to clean up. Removed.

You mention as part of the “face seen from a point” section that the test involves checking if the dot product is greater than zero, but the code is not demonstrating this. Just thought I’d point that out.

That’s because I’m showing only the code for blowing up a simplex to a tetrahedron. 🙂

Hey,

I managed to create EPA however it gives only 1 contact point. When I stack two boxes there should be 4 contact points.How can I get the other 3 points?

One way to deal with collision detection algorithms that only generate one contact point is, add the newly created contact point in the current frame to a set of “persistent contact points” that is persistent across frames, and remove a point from the set if it has gotten too “different” from the state in which it was first created or if your set is full.

Simply put, generate one contact point per frame and accumulate to up to four contact points over multiple frames.

You can find out more about persistent contacts in this post.

Oh that’s awesome 🙂 Thanks

Ok I begun to stuck this contact points and think I have a problem and I don’t know if it is because of GJK or EPA.

When the two boxes (one is ground(big) and the other one(small) is falling on the ground) collide for the first time I get the first collision contact, right in the middle of the box.

After that the second and the third contact points are on the corners of the smaller box. Because I get forces back from the constraints, the box begins to jump up and I can’t make it stable. Because of this I can’t get the 4th contact point.

Do you think that first point might cause this behavior?

The boxes are not rotated around the axis.

Thanks

I think I have the same problem. The first point is right in the middle of the box and I can’t make them stable

Hmm. I’ve never run in to this problem before. Yes, I also got the same series of contact points in the same setup, but never got unstable results. The corner contact points should cause the box to rotate and make the other corners penetrate more, resulting in them getting picked up by collision detection and added to a persistent contact manifold.

Did you remember to update the penetration depth for cached contacts before constraint resolution every time step? This has caused me instability before.

Oh I didn’t update the penetration..:D

About the first point in the middle of the boxes. I took a screen capture to show you:

http://gyazo.com/6c029037e0562db88ec52583d2fe040e

I tried to debug visually to see what happens and I always get the origin from the simplex resulted by the GJK right on the edge of a face. (in the picture, the green line contains the origin (0,0,0) ). Is this right? Even if I rotate the boxes and I don’t perfectly stack the boxes, the origint is still in on the edge of the simplex

There’s nothing wrong with the origin always ending up on a simplex edge in GJK. In fact, I always get the closest point to the origin on a simplex edge due to my implementation of support function, even if the closest simplex feature to the origin is a face.

Does the EPA works by maintaining the convex hull of CSO and find the closest face?

It works like the incremental algorithm of 3D convex hull.

Yes, the logic in each EPA iteration is actually the same as the 3D quick hull algorithm. It keeps adding vertices to grow the polytope, each vertex added being the support point in the direction of the closest point on the existing polytope to the origin.

Hi!

How do you deal with the case when the original support points (from the two bodies) form a degenerate triangle? (two or more points are the same)

This can happen very easily, despite that the face on the CSO’s boundary is actually a valid triangle.

As long as the algorithm used to determine the distance between a point and a triangle can handle degenerate cases, it shouldn’t be a problem. Also, in my own implementation, I break out of EPA if the next closest face is not closer than the previous closest face by a marginal amount; this can prevent the algorithm from being stuck in an infinite loop where the closest point on the CSO lies on multiple faces, which is another degenerate case.

Great article! Thank you for sharing. I have a question though. Why do you need to remove all the triangles that can be “seen” by the new support point? Is it because otherwise the “polytope” might lose its convexity? It’s hard to picture in the head how the polytope would grow, but judging from the 2d case you illustrated above, the polytope(polygon in 2d) would always preserve the convexity because it grows inside the Mikowski Sum which itself is convex. Thanks,

Lin

Yes, you are correct. You have to remove triangles that can be “seen” by the new support point so the convexity of the polytope is preserved.

Hi, excellent series of tutorials.

Minor point: shouldn’t the comparisons be “inverted” on lines 79 and 110?

You’re right. Thanks for pointing out the typos. Fixed.

Hi

Your method of generating an orthonormal basis given a single unit vector does not always work. Consider the input =).

Erin Catto recently posted this: http://box2d.org/2014/02/computing-a-basis/ which is a pretty cool approach. I decided to add a small smudge factor since I don’t trust floating point numbers.

With that being said, thank you so much for all your blog posts, they have been and are going to be a great help 🙂

Consider the input (0, 1, 0)*. Apparantly gt and lt aren’t accepted.

You’re right. Thanks for pointing it out. I added a note.

Oh cool, thank you!

This is awesome, the best explanation of 3D EPA I’ve seen!

However, can you elaborate on what you mean by the faces the support point can ‘see’? Do you mean ones of which the support point is on the side of the plane facing OUTWARDS from the object?

You are correct. I will add a new section to elaborate on this.