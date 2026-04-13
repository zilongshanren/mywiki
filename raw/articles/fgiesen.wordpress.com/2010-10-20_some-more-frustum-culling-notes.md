---
title: Some more frustum culling notes
url: https://fgiesen.wordpress.com/2010/10/20/some-more-frustum-culling-notes/
published: '2010-10-20'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Some more frustum culling notes

More link-chasing! [Charles](http://cbloomrants.blogspot.com/2010/10/10-18-10-frustum-and-radiusindirection.html) has some more notes on the general “get center along axis” / “get radius along axis” primitives that are used in these tests. This is also at the heart of separating axis tests and the GJK algorithm for collision detection, so it’s definitely worth getting comfortable with. He also notes that:

Frustum culling is actually a bit subtle, in that how much work you should do on it depends on how expensive the object you are culling is to render. If the object will take 0.0001 ms to just render, you shouldn’t spend much time culling it. In that case you should use a simpler approximate test – for example a Cone vs. Sphere test. Or maybe no test at all – combine it into a group of objects and test the whole group of culling. If an object is very expensive to render (like maybe it’s a skinned human with very complex shaders), it takes 1 ms to render, then you want to cull it very accurately indeed – in fact you may want to test against an OBB or a convex hull of the object instead of just an AABB.


I agree with the second part, but I’m not sure about the cone vs. sphere test. Three reasons: First, the cone around the view frustum is really a pretty coarse approximation. For a 4:3 viewport, the area of the cone cross-section along the near plane is about 64% larger than the area of the bounding rectangle. For the 16:9 viewports we now commonly have it’s about 84% larger than the rect. That’s a *very* conservative test, even if you have tight-fitting bounding spheres. Second, even when an object is cheap to render, it still goes through a lot of pipeline stages before it ever gets submitted to the GPU. You don’t draw things immediately; you normally [build a job list first that is then sorted](http://realtimecollisiondetection.net/blog/?p=86). You may also do some sort of occlusion culling. For all survivors, you then need to set the state for that batch (shaders, constants, textures, various rendering states), do some state filtering while you’re at it (to avoid wasting GPU cycles with redundant state changes), and then finally issue the actual draw call. Even with optimized code, that’s usually a few thousand clock cycles start to finish. For posterity, let’s assume that the box-frustum test costs 50 cycles more than a sphere-cone test (which is generous), and each non-culled batch costs an average of 1000 cycles start to finish. If your coarse test has a false positive rate of only 5%, it’s no win; at 10%, it’s a 50 cycles/batch net cost. Third, even if it is a win on the CPU side, you end up generating GPU work for some false positives. Wasted GPU cycles are more expensive than wasted CPU cycles, because there’s less of them (lower clock rate, and usually just one GPU vs. more than one CPU core nowadays).

Grouping is a good point though. If there’s a natural grouping for your dynamic objects, exploit it. For your scenery, you should build a static hierarchy. Large cache lines, high mispredicted branch penalties and SIMD-optimized processors mean that any kind of binary tree is a bad choice (doubly so when you don’t have fast random access to memory as on SPUs). Use a larger fan-out, aim for a fairly flat hierarchy (again, doubly so for SPUs). Don’t build just any tree; use a simple cost function and choose your subdivisions to minimize it (no need for exhaustive search, it’s enough to test 5-8 different options at each level and pick the best one). If in doubt, build a binary hierarchy first (it’s easier to code) then merge nodes later to get the larger fan-out.

Culling tests inside a hierarchy have different trade-offs than the per-batch culling tests you do at the leaf nodes, so consider using different code (or a different type of bounding volume) for it.

If your tests work with clipspace geometry, it’s fairly easy to build a 2D screen-space bounding box around your BV while you’re at it. The cheap version just returns the whole screen when the BV crosses the near plane; Blinn describes a more accurate (but slower) variant in “Calculating Screen Coverage” (Chapter 6 of “Jim Blinn’s Corner: Notation, Notation, Notation”, another book you should consider buying). Either way, this bbox is useful: you can use it to estimate the screen size of objects (useful for LOD selection and to reject objects entirely once they’re smaller than a few pixels) and as input to a coarse occlusion test.

The bbox screen size test is more generally useful than a far-plane test; if you use it, consider skipping the far-plane test entirely during your per-batch culling. That brings your plane count down to 5; depending on your geometry, there might be another plane that’s not really helpful for culling (usually the top or bottom plane). Throwing another plane out gets you down to 4, which may or may not make your culling code nicer (4-way SIMD and all). Debatable whether it helps nowadays, but it used to be nifty on PS2 :)

Yeah you’re probably right about the sphere-cone test making no sense. The only time I’ve actually used it was a pre-test before doing the more expensive OBB-frustum test.

BTW I think that spheres get a bad rap. It’s a myth that they are on average way larger that aabb’s, people have looked at too many characters in “jesus pose”. They are slightly larger on average, but the big advantage is you can store them with only 1 float (assuming you already have a position for your object near its center; if your position is a “floor” position then you probably need two floats, one for a Z offset and one for a radius).

And not needing to do any ModelToWorld transform at all to cull is a massive massive win.

As I mentioned, there’s an inherent imbalance between leafs and inner nodes in any kind of hierarchy. The cost of a false positive for an “inner node” test is some unnecessary testing at lower levels (which hopefully all get rejected). But a false positive on leaf levels usually causes a lot of extra work, so you want to make your leaf tests more precise. Cheaper tests are very useful at the top levels where you want to rapidly throw out everything that’s definitely irrelevant.

“I think that spheres get a bad rap. It’s a myth that they are on average way larger that aabb’s, people have looked at too many characters in “jesus pose”.”

Well, characters in general get a pretty bad fit with spheres, as do columns, flagpoles, trees, planks, rifles, swords, spears, bows, arrows, axes, staffs and wands, skis and cars – anything that has a dominant major axis really. To get a good fit for such objects in a general setting you need OBBs, since AABBs quickly get very bad once you start rotating. But if you work with object-space bounds, it’s a non-issue since items with a “dominant direction” usually get authored with that direction aligned with the coordinate system.

“And not needing to do any ModelToWorld transform at all to cull is a massive massive win.”

Yep, very useful especially at the top levels of a hierarchy.

Spheres are great for a quick, coarse cull, but I’d stay with sphere-frustum instead of sphere-cone. It’s still a fairly cheap test (with SIMD and fast FMA, a few dot products are nothing to worry about), and you don’t want to over-approximate your frustum too much; your bounding volumes get a better fit as you get closer to leaf level, but your frustum approximation stays the same.