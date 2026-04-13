---
title: Instancing for BrickSmith
url: http://hacksoflife.blogspot.com/2013/01/instancing-for-bricksmith.html
author: Benjamin Supnik
published: '2013-01-30'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[BrickSmith](http://bricksmith.sourceforge.net/)is a FOSS 3-d

[LDraw](http://www.ldraw.org/)-compatible editor for Mac; basically it lets you model legos on your computer. BrickSmith is a wonderful program - really a joy to use. I have submitted a few patches, mostly little features that I want for my own modeling. Recently I rewrote the low level OpenGL drawing code to improve performance and quality; hopefully we'll ship this in the next major patch.

This post describes the OpenGL techniques I picked. Since OpenGL is a cross-platform standard, it's possible that the design might be of interest (at least for reference) to other LDraw program developers. In some cases I will reference X-Plane performance numbers because I have access to that data.

#### LDraw Basics

- The file format effectively turns into something like a push-down state stack and individual line, tri, and quad primitives.
- The vast majority of drawing tends to be colored lines and polygons; while texture support was added to the format, it's not yet in wide-spread production.
- LDraw models tend to be vertex bound; the format contains no LOD for reducing vertex count, and the lego parts are modeled in full geometric detail. (Consider: even though the lego 'studs' are only broken into octagon-prisms, you still have 1024 of them on a single baseplate.)

#### Basic OpenGL Decisions

The new renderer uses shaders, not the fixed function pipeline. Because of this, I was able to program one or two LDraw-specific tricks into the shaders to avoid CPU work.The shaders understand the LDraw concept of a "current" color (which is the top of a stack of color changes induced by the inclusion of sub-parts/sub-models) vs static hard-coded colors; a given part might be a mix of "this is red" and "fill in the blank". I represent these meta-colors that come off the stack as special RGBA quadruples with A=0 and RGB having a special value; the shader can then pull off the current stack state and substitute it in. This is important because it means that I can use a single mesh (with color) for any given part regardless of color changes (the mesh doesn't have to be edited) and I don't have to draw the mesh in two batches (which would cost CPU time).

BrickSmith "flattens" parts in the standard LDraw library into a single simple representation - in other words, the 'stack' is simulated and the final output is consolidated. Thus a part is typically a single set of tris, lines, and draws, all stored in a single VBO, with no state change. Thus the library parts are "atomic". The VBO is loaded as STATIC_DRAW (because it is virtually never changed) for maximum speed.

Because LDraw models are currently flat shaded, BrickSmith does not attempt to index and share vertices; all VBOs are non-indexed, and a distinct set of GL_QUADS is maintained to avoid vertex duplication.

(I believe we would get a performance boost by indexing vertices, but only if smooth shading could be employed; with flat shading virtually all vertices have different normals and cannot be merged.)

#### Attribute Instancing

A naive way to draw part meshes would be to use glPushMatrix/glRotate/glTranslate sequences to push transforms to the GPU. The problem with this technique is that it is CPU expensive; the built-in matrix transforms are uniform state, and on modern cards this uniform state has to live in a buffer where the GPU can read itThus each time you 'touch' the matrix state, the

**entire**set of built-in uniforms including the ones you haven't messed with (your projection matrix, lighting values, etc.) get copied into a new chunk of buffer that must be sent to the card. The driver doesn't know that you're only going to touch transform, so it can't be efficient.

That uniform buffer will then either be in AGP memory (requiring the card to read over the PCIe bus at least at first to draw) or it will have to be DMAed into VRAM (requiring the card to set up, schedule, and wait for a DMA transfer). Either way, that's a lot of work to do

**per draw call**, and it's going to limit the total number of draw calls we can have.

Remember, 5000 draw calls is "a lot" of draw calls for real-time framerates. But 5000 bricks is only one or two big lego models. If you model all of the

[modular houses](http://en.wikipedia.org/wiki/Lego_Modular_Houses)and you just want to see them in realtime, that's 17,090 parts -- that's a lot of draw calls!

One trick we can do to lower the cost of matrix transforms is to store our model view matrix in

*vertex attributes*rather than in a uniform. Vertex attributes are very cheap to change (via glVertexAttrib4f) and it allows us to draw one brick many times with no uniform change (and thus all of that uniform work by the card gets skipped). If we draw one brick many times, we can avoid a VBO bind, avoid uniform change, and just alternate glVertexAttribute4fv, glDrawArrays repeat.

This technique is sometimes called "immediate mode" instancing because we're using immediate mode to jam our instancing data down the pipe quickly. For X-Plane on OS X, immediate mode instancing is about 2x faster than the built-in uniform/matrix transforms.

BrickSmith's new renderer code is built around a 24-float instance: a 4x4 matrix stored in 4 attributes, an RGBA current color, and an RGBA compliment color.

#### Hardware Instancing

One nice thing about using attributes to instance is that it makes using hardware instancing simple. With hardware instancing, we give the hardware an array of 24-float "instances" (e.g. the position/colors of a list of the same brick in many places) and the brick itself, and issue a single draw call; the hardware draws the brick mesh for each instance location.Hardware instancing is much faster than immediate mode instancing - YMMV but in X-Plane we see instancing running about 10x faster than immediate mode; X-Plane can draw over 100,000 individual "objects" when instancing is used - more than enough for our modular houses.

To use instancing we put the instance data into a VBO and use glVertexAttribDivisor to tell OpenGL that we want some attributes (the instance data) to be used once per model, while the other data is once per vertex.

For BrickSmith, the instance locations are GL_STREAM_DRAW - BrickSmith generates the list of bricks

*per frame*as the renderer traverses the model. So the bricks themselves are static but their locations are on the fly. I chose this design because it was the simplest; BrickSmith has no pre-existing way to cache sets of brick layouts. At 24 floats, even a 100,000 brick model is only about 10 MB of data per frame - well within the range of what we can push to the card.

(By comparison, X-Plane precomputes and saves sets of objects, so the instance location data is GL_STATIC_DRAW.)

#### Drawing Dispatch

- As draw calls come in, we simply accumulate information about
*what*the app wants to draw. Parts that are off screen are culled. (Since we are bound on the GPU, we can afford the CPU time to reduce vertex count.) - If a part contains translucency, it goes in a special "sorted" bucket, which is drawn last, from back to front. The sorting costs CPU time, so we only do this when we identify a part with translucency.
- Parts with "stack complexity" (e.g. texturing) that need to be drawn in multiple draw calls go in another bucket, the "just draw it" bucket - they are sorted by part so that we can avoid changing VBOs a lot - changing VBOs takes driver time!
- Parts that are simple go in the "instancing" bucket, and we accumulate a list of locations and parts (again, organized by part.)

Note that all instanced parts are written into a single giant stream buffer. This lets us avoid mapping and unmapping the buffer over and over, and it lets us avoid having a huge number of small buffers.

Generally fewer, larger VBOs are better - they're relatively expensive objects for the driver to manage; if your VBOs are less than one VM page, find a way to merge them.




#### Performance Results

The new renderer often runs about 2x faster than the existing code, while providing sorted transparency, and it typically runs at significantly lower CPU.

One case where it did not run faster was with Datsville - the Datsville model I have for testing is about 39,000 bricks, resulting in 125 million vertices. It runs on my 4870 at about 5 fps.

In the old renderer, I would see 100% CPU and about 5 fps; with the new one, maybe 30-35% CPU and 5.1 fps. Why no more speed? It turns out that the total vertex capacity of the card is only about 500 million vertices/second, so the card is vertex bound. (This is quite rare for games.) When the model is partly off-screen, framerate increases significantly.

Sorry, but this implementation is very slow:









ReplyDelete1) Reduce per instance data:

it is possible to pack all (and more) your data to 8 floats and then unpack it on shader using GLSL unpack* functions (do not store matrices directly, separate in position and XY local rotation)

2) Do not use glVertexAttribDivisor (see 3))

3) Use merged instancing: duplicate your model 100-1000 times (just do vertex buffer larger), than use complex indexing on VS, like:

int i = INSTANCE_OFFSET + gl_InstanceID*INSTANCE_BATCH_SIZE + gl_VertexID/ELEMENT_VERTEX_COUNT;

i *= PIXELS_PER_INSTANCE;

than, fetch and unpack data:

float3 inGlobalPosition = texelFetch(instanceBuffer_unit7, i ).xyz;

float3 instanceAttrib = texelFetch(instanceBuffer_unit7, i+1 ).xyz;

uint3 instanceAttribI = floatBitsToUint(instanceAttrib);

float2 inAzimuthSinCos = unpackHalf2x16(instanceAttribI.x);

float4 inInstanceAttributes = unpackUnorm4x8(instanceAttribI.y);

Yes, this way is complex, and requires a lot of instructions, BUT: it is very fast, like a speed of light.

Main problem in your engine: very low VS rate, because your main VBO is very small.

P.S. Sorry, if I misunderstood your post (:

Closed: all of your techniques are totally valid for boosting instancing speed, but in the case of BrickSmith, performance data I have already gathered indicates they won't help, because of the shape of Bricksmith's source data. Here's some of the things I measured...note that this applies to ATI Mac drivers only; BrickSmith is Mac-only software. My experience with the NV Mac driver is that it isn't competitive perf-wise. :-(








ReplyDelete(BrickSmith is also not yet ported to the 3.2 core profile on Mac, so I have not been able to test TBOs on NV Mac hardware.)

Would smaller instance data help? I don't think it would in this case because we're not bandwidth limited in pushing the relatively small number of instance objects. I do believe that if we had a larger number of simpler instances this _would_ start to matter.

Would a shorter vertex shader help? I don't think so; I tried simplifying vertex shader and fragment shader calculations and the needle didn't move.

Would changing the index sourcing from attrib-divisor to TBOs help? Would having a smaller number of bigger instances help? I don't think so; I have seen a multi-mode test program that can vary the instance count, instance object mesh size, and instance source (vertex divisor, UBO, and TBO) and max vertex throughput is flat across everything - more instances trades off perfectly with smaller instances (to a point); and you can have a surprisingly small instance mesh (e.g. 100 vertices). The bottleneck really is in triangle setup.

One other note on mesh size: a single lego stud in BrickSmith is 56 vertices -- at that number virtually every single "brick" is going to be at least 100 vertices - that is, big enough to be efficient from an instance-stream perspective.

Fortunately there just aren't _that_ many kinds of bricks in the lego world -- the test model I used has 39,690 bricks but only 548 unique bricks. That's just not a huge number of instance-batches. And if we're drawing 125M instance vertices in only 548 batches, we're well into the efficient range of the GPU -- no merging necessary. :-)

The merged instancing idea seems interesting but unnecessary - I have not seen any indication that the hardware can't re-run the mesh buffer (without duplication) efficiently. (On Windows NV hardware attribute divisors appear to operate acceptably in X-Plane, which is what makes me think the NV Mac performance is driver related and not a hardware limitation..this was on the new 650M laptops...)

cool post! not particularly familiar with bricksmith, but am with recent GPUs. they have a lot of fragment shader power you're not using. my first thought while reading your post, in trying to reduce your vertex-bound bottleneck, would be to render the lego 'bobbles' with a special bobble shader, as simple bounding geometry (either a world-space cubeoid, or, a screenspace bounding rectangle - ie either 8 or 4 vertices) and use a fragment shader that 'raytraces' against the analytic equation of a capped cylinder; that would also give you perfect round bobbles, and balance the use of your GPU better - far fewer vertices. I know there's a pool/snooker game that does this for their spheres, for example, (I can't remember the reference at the moment, but google will probably find it). the maths for ray-cylinder and ray-plane (for the caps) is really simple.

ReplyDeleteyou could of course fall-back to your existing vertex-based bobble geometry for cards that do not support fancy fragment shaders.

Alex, you are totally correct that BrickSmith is using the GPU asymmetrically - in particular, when a brick is far away (and thus rendered at low res) a shader based procedural set of studs would be better than geometry.


ReplyDeleteBrickSmith is an editor for Ldraw files, and the ldraw format is pre-specified, so substituting procedural definitions with chunks of geometry, while possible, isn't really in the application design domain.

Regarding your 39,000 bricks/125 million vertices @ 5fps case, that's around 90 vertices *per pixel* on a 2560x1440 monitor, aka massive overdraw.


ReplyDeleteBesides LOD techniques such as mentioned above to mitigate this, how about occlusion culling? Lego models should in general be very amenable to this.

Mipmap, you're right about the massive over-draw; I'd have to read the fine print of the GL spec to see how much actual overdraw is happening (because most of those triangles are going to end up sub-pixel in size). Either way, it's terribly wasteful. :-)



ReplyDeleteI think the problem with occlusion culling is that we'd need additional data of some kind to do the occlusion, and no matter which way you slice it, that data can't come from the existing LDraw data.

Is there an occlusion culling data structure you like that would be amenable to a huge number of small parts (that together may or may not cover useful areas) when offline pre-processing isn't an option?

Have you considered fully GPU-based occlusion, roughly:










ReplyDelete1. Render the parts as bounding boxes to a mip-mapped depth texture.

2. Render the parts as bounding boxes again, this time querying the depth texture for occlusion.

3. If potentially visible, geometry shader renders the actual part. Otherwise geometry shader discards the part.

I'm relaying this idea from http://rastergrid.com/blog/2010/10/hierarchical-z-map-based-occlusion-culling/ which includes a working sample.

Given the heavy instancing of Lego models, maybe this would be even more beneficial than occlusion culling:

ReplyDeletehttp://rastergrid.com/blog/2010/02/instance-culling-using-geometry-shaders/

This may sound crazy but: we don't have reliable access to hardware-accelerated geometry shaders on OS X for our supported set of operating systems.





DeleteMy general view on occlusion queries is this: I have never seen an occlusion query system simpler to write than an LOD system. And there's a lot to be said for LOD under all conditions - consider that a single baseplate can generate 180,224 vertices right now. (The odds of the entire baseplate being occluded are poor and the rendering output quality of that many vertices in a small space looks lousy.)

So my plan of action is to ignore occlusion culling temporarily - and do something like this:

1. Implement sane basic LOD.

2. Observe the new performance characteristics.

3. Implement the DUMBEST occlusion system I can, only to get metrics on the 'real' savings with real lego models.

4. Only then, examine various occlusion culling schemes if we find from (2) that we need more vertex saving and (3) that occlusion savings will deliver.

BrickSmith is an open source 'hobby program' to all of its authors, so there's no way that we can invest the time to do sane and proper occlusion culling without first determining that the payoff is there. Heck - I'd do the same pre-research for my day job work too!