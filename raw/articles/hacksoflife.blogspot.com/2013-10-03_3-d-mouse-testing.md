---
title: 3-d Mouse Testing
url: http://hacksoflife.blogspot.com/2013/10/3-d-mouse-testing.html
author: Benjamin Supnik
published: '2013-10-03'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I just finished fixing a long-running bug in

















[BrickSmith](http://bricksmith.sourceforge.net/)'s culling code; this post is a review of ways to do mouse testing of a 3-d model.### Modelview Space

The original BrickSmith code tested the mouse in the modelview-space of the entire model:

- The mouse click is treated as a ray in normalized device coordinates (that is, it goes from Z=-1 to Z=1 at an X and Y that are proportional to the click on the viewport).
- The mouse click ray is transformed by the inverse of the model-view + projection matrices to get a test ray in model-view space.
- Each test triangle is
*forward*transformed by its relative transformation before testing. - The ray and triangle are tested via something like
[Möller-Trumbore](http://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm).

- We need the depth of intersection to sort our hits, and we get that from the algorithm for free, which is nice.
- The algorithm forward transforms every triangle (sad) but it also does not have to calculate the inverse matrices of any of the sub-transforms of our model. Since LDraw sub-transforms can be pretty much anything in a 4x3 matrix, not having to run a real 'inverse' is nice.
- Because we aren't doing plane-based intersections or using matrix inverses, there is no need to cache any data to make the intersection tests faster. Since BrickSmith is an editor, not having to precompute 'helper' data for our model (that would need to be recalculated every time the user edits) is a win.
- There is no culling or early out; a hit test looks at pretty much the
*entire*model, which is not fast.

Had we stayed with a modelview-space approach, I believe the marquee selection would have been implemented by taking the intersection of all triangles on the positive side of six planes: four planes going through the camera position and the selection box, as well as the near and far clip planes. In other words, the marquee selection forms a tighter-frustum in which we want to find intersections.

Had we had such a frustum test, it would have had two other uses:

- Accelerating rendering (by discarding any rendering that was fully outside the 'big' frustum that is the viewport) and
- If the frustum test is faster than our ray-triangle hit test (above), we can accelerate single-point testing by first culling the entire scene to a frustum that 'barely' surrounds our hit ray (e.g. via a marquee selection of just a few pixels).

### Screen Space

When I looked at getting a frustum test going (to implement marquee selection), I came up with an idea that I thought at the time would be very clever: work entirely in screen space. Working in screen space creates a more fundamentally limited API (because all queries must be specified in screen space points and AABBs, whereas the old code could test any ray in any direction) but BrickSmith was only using screen-space tests, and they can potentially be done quite a bit quicker. Here's how the new code worked:

- Point queries and AABB queries are always provided in normalized device coordinates (with returned depths also in NDC from -1 to 1).
- To test triangles, we forward transform them all the way through their complete matrix (model view and projection) and then do a perspective divide.
- The resulting primitive is 2-d in its extent and can be tested very cheaply. In particular, the AABB test is dirt cheap in 2-d.

*containers*of parts first (by trnasforming the AABB from its local model space to screen space, building a new AABB around it, and testing that). This hierarchical culling of bounding boxes is what provides the real speed. Given an MPD model with most of the sub-models off screen, we pay almost nothing for them.

One more win: because the frustum surrounding a single mouse-click test is so tiny, almost everything in a model is rejected early when testing for the mouse, so mouse-over-the-model is fast even when a huge model is entirely on screen.

### Clip-Space

At this point I was feeling pretty clever and smug (because for a really big model, the hierarchical culling could give you a 10x or 50x speedup) and happy (that my models were usable again). But of course if you have been working with 3-d graphics for a while, you're probably face-palming yourself at the big leak in the abstraction of working in clip space.

Here's the thing: BrickSmith normally keeps your entire model behind the near clip plane. It's like your model is sitting on a table and you are hovering over it; you never actually jam your face

*into*the model. So the fact that I was working in screen space was not a problem because the entire model always had a sane representation in clip space.
Until it didn't. I implemented a "walk-through" camera that would let the user get

*inside*their model and look around. For users making modular buildings, this leads to some pretty cool screen-shots. But it also led to low framerate and (even weirder) whole parts of the model just disappearing randomly! I looked at the math over and over and there just wasn't something broken.
Of course what was broken was not a math mistake, it was a lack of

*clipping*. The problem is that in screen space, geometry in front of the near clip plane is eliminated by the GPU; therefore we don't have to worry about the strange things that happen in front of the near clip plane. But in my hit-testing code, those vertices were being processed as is.
After a standard glFrustum transformation, vertices in clip space (homogeneous coordinates) have their -Z in their W coordinate which will become a divisor to the final device-space coordinate. X and Y have been multiplied by the near clip plane. So:

- At the near clip plane, geometry does not change size. In other words, you have a simple 2-d coordinate system.
- Behind the near clip plane, things get smaller as they get farther away - this is not astonishing.
- In front of the near clip plane, things get really big, really fast as we divide by a fractional Z.
- At Z = 0 (parallel to the camera) we get a divide-by-zero, which is exciting.
- Behind the camera, the divisor is negative (Z is positive, but the W coordinate has been negated already to get the rest of rendering to be not insane), so everything is mirrored in X and Y!

The disappearing models happen when we have a model-view-space AABB that is to the left side of the screen in front of the camera and to the right behind the camera (because it is at a 45 degree angle to the eye-space Z axis, for example); in this case the "behind us" part of the AABB flips, and the whole AABB is to the left side of the screen in screen space and gets culled.

(This case happens a lot when we have long, thin models that we are in the middle of, viewed at a 45 degree angle to their long axis. In other words, walk around a modular city and the city is going to disappear on a regular basis as you pan the camera.)

The fix I found and implemented is stupid but effective: clip all transformed triangles in clip space before the perspective divide.

- The AABB is treated as a cube and each of its 12 edges are clipped to produce a new point set. Since the AABB was going to have a new AABB built around its 12 points, doing this with a clipped point set isn't much different.
- Triangles are clipped, sometimes resulting in zero or two triangles, before the perspective divide.

### Other Options

There were a few other options I considered but haven't had time to code.

One option would be to do what X-Plane does (for culling) and work in eye-space, using side-of-plane tests for our frustum culling. The test (for points) is cheap and would work without clipping.

(X-Plane does its ray-triangle mouse-testing in the coordinate system of the model itself; because all of the local transforms are simple rotations or translations, applying the inverse to the test ray is really cheap, and it avoids having to transform the entire model.)

Another option would be to work in homogeneous coordinates. I am still not sure if this is mathematically possible, but the idea would be to do the ray-point intersection in clip space, and then check whether the clip-space intersection is behind the near clip plane. This would let us do a single ray-triangle intersection without special-casing out the clipping logic, then reject a single point later.

## No comments:

## Post a Comment