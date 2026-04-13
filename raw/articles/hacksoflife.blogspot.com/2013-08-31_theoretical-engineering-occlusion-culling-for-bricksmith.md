---
title: 'Theoretical Engineering: Occlusion Culling for BrickSmith'
url: http://hacksoflife.blogspot.com/2013/08/theoretical-engineering-occlusion.html
author: Benjamin Supnik
published: '2013-08-31'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I have been pushing for a formal level-of-detail scheme for LDraw; the performance problem is that LDraw bricks contain a fairly high vertex count; at low zoom a large model might be entirely on screen, resulting in frame-rate limited by pure vertex count. (The vertices are on the GPU, the batches are drawn with array-attribute-divisor instancing, and the destination viewport is small with simple shaders, so the limiting factor is trying to cram 125M vertices through the GPU.)


During the discussion, some developers brought up the question of occlusion culling. In many of these wide views, a fair amount of the geometry is going to have no contribution in the final image due to occlusion by other, closer bricks.


Occlusion culling is tricky stuff. Occlusion queries on the GPU are not available to the CPU until drawing completes; recent GPUs are finally gaining the ability to use the occlusion query result directly, eliminating back-to-the-CPU latency. CPU-side occlusion queries are usually facilitated by heavy pre-processing of the source data, but that isn't an easy option in BrickSmith because it is an editor, not a viewer (and therefore the source data is continually changing).


What follows is speculative engineering, e.g. how


When looking at the algorithm that follows, please keep one thing in mind: the limiting factor here is vertex count - that's what we are trying to optimize. This is a very unusual situation in 3-d graphics; most systems are designed to not have this problem. In particular, we are not fill rate bound, so we can expect GPU commands involving small numbers of vertices to complete reasonably quickly, because the GPU isn't drowning in last-frames pixel-fill operations.


Here's the basic idea:












During the discussion, some developers brought up the question of occlusion culling. In many of these wide views, a fair amount of the geometry is going to have no contribution in the final image due to occlusion by other, closer bricks.

Occlusion culling is tricky stuff. Occlusion queries on the GPU are not available to the CPU until drawing completes; recent GPUs are finally gaining the ability to use the occlusion query result directly, eliminating back-to-the-CPU latency. CPU-side occlusion queries are usually facilitated by heavy pre-processing of the source data, but that isn't an easy option in BrickSmith because it is an editor, not a viewer (and therefore the source data is continually changing).

What follows is speculative engineering, e.g. how

*could*occlusion culling work on a modern GPU. Looking at the requirements for the design we can then infer as to whether such a scheme is feasible. (Spoiler alert: it is not.)When looking at the algorithm that follows, please keep one thing in mind: the limiting factor here is vertex count - that's what we are trying to optimize. This is a very unusual situation in 3-d graphics; most systems are designed to not have this problem. In particular, we are not fill rate bound, so we can expect GPU commands involving small numbers of vertices to complete reasonably quickly, because the GPU isn't drowning in last-frames pixel-fill operations.

Here's the basic idea:

- Every part that we draw is divided into two sets of geometry: the crude occluders and the rest of the part. The crude occluders are the non-transparent triangles and quads (no lines) that are big enough to be worth drawing early to start filling space. The goal is to keep fill rate high while lowering vertex count, so that we can fill a lot of the screen quickly and then see what is left. (For example, for a 2x4 brick, the outer 5 quads of the brick top and sides would be the crude occluders; the entire interior, edging, studs and tubes and line work would be the rest.)
- Each brick is pre-'normalized' so that it exists within a unit cube; when we draw our brick instances, the transform matrix will include scaling factors to reconstitute the brick, not just the translation and rotation we have now. (This means that we can know from the instance data where a brick will be.)
- We set up an off-screen render target so that we can get direct access to the depth buffer; we'll blit the whole thing down to screen later, and it'll be cheap (one single-pass screen-sized blit with no processing).
- We start drawing the way the engine works now: we traverse the data model and dynamically build instancing lists for all opaque parts. (Translucent parts get dumped in a holding bay for later, slower, sorted processing; they won't participate in occlusion.) This step exists in the current BrickSmith source code and is fast enough that CPU is not the bottleneck even on my older 2008 Mac Pro.
- We draw the instance list with the crude occluder meshes. This should, in theory, complete quickly, because the vertex count is low, early Z can take effect, there is no blending, and our shaders are not complicated.

Our next step is to grab the depth buffer and use render-to-texture to ping-pong it, forming a hierarchy of depth buffers. For each depth buffer we will use a "farthest" policy, so that a low-res depth texel contains the farthest depth of the four high-res depth texels that it covers.

Now we can run

[GPU culling](http://rastergrid.com/blog/2010/02/instance-culling-using-geometry-shaders/). For each instance list VBO, we run it through a geometry shader, treating one instance as one vertex. (In BrickSmith, instances are a 4x3 affine transform plus two RGBA colors, so our 20 floats can be five attributes in the vertex stream.) The geometry shader calculates the screen space AABB of the instance, fetches depth from the appropriate level of the Z buffer, and determines whether the brick's bounding box is clearly behind every single pixel already drawn into the AABB's location. The geometry shader then outputs zero or one vertices depending on the cull.
The geometry shader must be fed into a transform feedback stage so that we can (1) capture the vertices back rather than render them and (2) so the GPU will retain the number of vertices for later use in a glDrawTransformFeedbackStreamInstanced call.

(We could implement frustum culling here too, but I think we need to keep the original CPU frustum cull from the initial draw in order to not draw the entire model off-screen when we are setting up our early-Z buffer.)

Note that BrickSmith currently uses one giant VBO for its instance list - the

[individual bricks know which part of the instance list they own](http://http.developer.nvidia.com/GPUGems2/gpugems2_chapter04.html), so we save on VBO count. However, if we want to reduce the instance count we have a serious problem: our segment buffering will be borked. One way to solve this is to transform each primitive into its own transform feedback VBO, so that we can know how many primitives to draw and where they start. This would probably be bad for total draw performance.
(There might be a better way to organize this, perhaps with multi-draw-indirect or compute, or atomic writes to a memory buffer. I have not dug into this because, as you will see from later in the post, this scheme is not actually shippable.)

Finally, with the instance lists culled, we can go and draw 'the rest' of the model; since the instance lists have been trimmed, we skip

*most*of the geometry for every occluded brick. Thus we will get a large vertex savings on every occluded brick. (For example, a 2x4 brick will save better than 97% of its vertices, even*after*excluding lines, when occlusion culled.)
There are a few reasons why we can't actually ship this.

- The biggest single problem that I see is that the part library would have to be pre-tagged into rough occluder geometry and the rest. Given the size of the part library and its structure as a series of "subroutine"-style partial primitives, such a partitioning would both be a huge manual undertaking (that could in theory be automated) and it would result in a transformation of the parts that could not be fed back into the LDraw system.
- The code above assumes the most modern GPU features. Instanced transform feedback is an OpenGL 4.2 feature, so it would require a DX11-class GPU. Apple has not yet shipped OpenGL 4.0, so at best we'd be dropping support for Lion and Mountain Lion.
- Using separate VBOs for each brick (to get the cull list) would be a serious performance problem. It might be possible to overcome this with other new OpenGL techniques, but the requirement on a new driver would remain. GPU-culling could also be performed only on parts for which there was a large part count, applying an 80-20 rule to culling.
- Finally, the technique above is very complicated - it is probably more implementation work than the entire renderer-rewrite was, and BrickSmith is not a commercial project; those of us who poke at it do so in our very, very limited spare time. I don't thin anyone involved in the project has time for such serious GPU work.

**Edit:**reading Daniel Rákos' article more carefully, I see he uses an asynchronous query to get the amount of feedback delivered. In theory this would let us source our instances out of a single VBO even after culling, which would be a performance win. However, I am not sure that this would be completely free. The algorithm without this modification can run entirely asynchronously - that is, the entire frame can be "late" and still render. Pulling back the instance count to the CPU therefore might introduce the first sync point and hurt performance. (E.g. if the previous frame hasn't completed, the next frame's query for culling count will block because the GPU wans't available.)**The conclusion is, of course, just to use crude reduced-LOD models for far viewing and go home happy. But having spent the time considering what it would take to do GPU culling, I figured I should at least write it down.**

## No comments:

## Post a Comment