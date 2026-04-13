---
title: Fixing Camera Shake on Single Precision GPUs
url: http://hacksoflife.blogspot.com/2018/01/fixing-camera-shake-on-single-precision.html
author: Benjamin Supnik
published: '2018-01-13'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I've tried to write this post twice now, and I keep getting bogged down in the background information. In X-Plane 11.10 we fixed our long-standing problem of camera shake, caused by 32-bit floating point transforms in a very large world.


I did a literature search on this a few months ago and didn't find anything that met our requirements, namely:



I didn't find anything that met both of those requirements (the 32-bit-friendly solutions I found required major changes to how the engine deals with mesh chunks), so I want to write up what we did.



























I did a literature search on this a few months ago and didn't find anything that met our requirements, namely:

- Support GPUs without 64-bit floating point (e.g. mobile GPUs).
- Keep our large (100 km x 100 km) mesh chunks.

I didn't find anything that met both of those requirements (the 32-bit-friendly solutions I found required major changes to how the engine deals with mesh chunks), so I want to write up what we did.

### Background: Why We Jitter

X-Plane's world is large - scenery tiles are about 100 km x 100 km, so you can be up to 50 km from the origin before we "scroll" (e.g. change the relationship between the Earth and the primary rendering coordinate system so the user's aircraft is closer to the origin). At these distances, we have about 1 cm of precision in our 32-bit coordinates, so any time we are close enough to the ground that 1 cm is larger than 1 pixel, meshes will "jump" by more than 1 pixel during camera movement due to rounding in the floating point transform stack.

It's not hard to have 1 pixel be larger than 1 cm. If you are looking at the ground on a 1920p monitor, you might have 1920 pixels covering 2 meters, for about 1 mm per pixel. The ground is going to jitter like hell.

Engines that don't have huge offsets don't have these problems - if we were within 1 km of the origin, we'd have almost 100x more precision and the jitter might not be noticeable. Engines can solve this by having small worlds, or by scrolling the origin a lot more often.

Note that it's

**not**good enough to just keep the main OpenGL origin near the user. If we have a large mesh (e.g. a mesh whose vertices get up into the 50 km magnitude) we're going to jitter, because*at the time that we draw them*our effective transform matrix is going to need an offset to bring the 50 km offset back to the camera. (In other words, even if our main transform matrix doesn't have huge offsets that cause us to lose precision, we'll have to do a big translation to draw our big object.)### Fixing Instances With Large Offsets

The first thing we do is make our transform stack double precision on the CPU (but

*not*the GPU). To be clear, we need double precision:- In the internal transform matrices we keep on the CPU as we "accumulate" rotates, translates, etc.
- In the calculations where we modify this matrix (e.g. if we are going to transform, we have to up-res the incoming matrix, do the calculation in double, and save the results in double).
- We do
**not**have to send the final transforms to the GPU in double - we can truncate the final model-view, etc. - We can accept input transforms from client code in single or double precision.

We do eat the cost of double precision in our CPU-side transforms - I don't have numbers yet for how much of a penalty on old mobile phones this is, but on desktop this is not a problem. (If you are beating the transform stack so badly that this matters, it's time to use hardware instancing.)

This hasn't fixed most of our jitter - large meshes and hardware instances are still jittering like crazy, but this is a necessary pre-requisite.

### Fixing Large Meshes

The trick to fixing jitter on meshes with large vertex coordinates is understanding

*why*we have precision problems. The fundamental problem is this: transform matrices apply rotations first and translations second. Therefore in any model-view matrix that positions the world, the translations in the matrix have been*mutated*by the rotation basis vectors. (That's why your camera location is not just items 12,13, and 14 of your MV matrix.)
If the camera's location in the world is a very big number (necessary to get you "near" those huge-coordinate vertices so you can see them) then the precision at which they are transformed by the basis vectors is...not very good.

That's not actually the total problem. (If it was, preparing the camera transform matrix in double on the CPU would have gotten us out of jail.)

The problem is that we are counting on these calculations to

*cancel each other out*:
vertex location * camera rotation + (camera rotation * camera location) = eye space vertex

The camera rotated location was calculated on the CPU ahead of time and baked into the translation component of your MV matrix ,but the vertex location is huge and is rotated by the camera rotation on the GPU in 32-bits. So we have two huge offsets multiplied by very finicky rotations - we add them together and we are hoping that the result is pixel accurate, so that tiny movements of the camera are smooth.

They are not - it's the rounding error of the cancelation of these calculations that

*is*our jitter.
The solution is to

**change the order of operations of our transform**stack. We need to introduce a*second*translation step that (unlike a normal 4x4 matrix operation), happens*before*rotation, in world coordinates and not camera coordinates. In other words, we want to do this:
(vertex location - offset) * camera rotation + (camera rotation * (camera location - offset)) = ...

Heres' why this can actually work: "offset" is going to be a number that brings our mesh

*roughly*near the camera. Since it doesn't have to bring us to the camera, it can change*infrequently*and have very few low-place bits to get lost by rounding. Since our vertex location and offset are not changing, this number is going to be stable across frames.
Our camera location minus this offset can be done on the CPU side in double precision, so the results of this will be both small (in magnitude) and high precision.

So now we have two small locations multiplied by the camera rotation that have to cancel out - this is what we would have had if our engine used only small meshes.

In other words, by applying a rounded, infrequently changing static offset first, we can reduce the problem to what we would have had in a small-world engine, "just in time".

You might wonder what happens if the mesh vertex is no-where near our offset - my claim that the result will be really small is wrong. But that's okay - since the offset is near the camera, mesh vertices that don't cancel well are far from the camera and too small/far away to jitter. Jitter is a problem for close stuff.

The CPU-side math goes like this: given an affine model-view matrix in the form of R, T (where R is the 3x3 rotation and T is the translation vector), we do this:

// Calculate C, the camera's position, by reverse-

// rotating the translation

C = transpose(R) * T

// Grid-snap the camera position in world coordinates - I used

// a 4 km grid. smaller grids mean more frequent jumps but

// better precision.

C_snap = grid_round(C)

// Offset the matrix's translation by this snap (moved back

// to post-rotation coordinates), to compensate for the pre-offset.

T -= R * C_snap

// Pre-offset is the opposite of the snap.

O = -C_snap

In our shader code, we transform like this:

v_eye = (v_world - O) * modelview_matrix

There's no reason why the sign has to be this way - O could have been C_snap and we could have added in the shader; I found it was easier to debug having the offset be actual locations in the world.

### Fixing Hardware Instancing

There's one more case to fix. If your engine has hardware instancing, you may have code that takes the (small) model mesh vertices and applies an instancing transform first, then the main transform. In this case, the large vertex is the result of the instancing matrix, not the mesh itself.

This case is easily solved - we simply subtract our camera offset from the translation part of the hardware instance. This ensures that the instance, when transformed into our world, will be near the camera - no jitter.

One last note: on some drivers I found the driver was very finicky about order of operations - if the calculation is not done by applying the offset before the transform, the de-jitter totally fails. The precise and invariant qualifiers didn't seem to help, only getting the code "just right" did.

## No comments:

## Post a Comment