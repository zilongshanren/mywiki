---
title: There Must Be 50 Ways to Draw Your Streaming Quads
url: http://hacksoflife.blogspot.com/2013/04/there-must-be-50-ways-to-draw-your.html
author: Benjamin Supnik
published: '2013-04-20'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

So you want to draw a series of streaming 2-d quads. (By streaming I mean: their position or orientation is changing per frame.) Maybe it's your UI, maybe it is text, maybe it is some kind of 2-d game or particle system. What is the fastest way to draw them?


For a desktop, one legitimate response might be "who cares"? Desktops are so fast now that it would be worth profiling naive code first to make sure optimization is warranted. For the iPhone, you probably still care.





Note that if we were using naive transforms, we'd still have to "push" a 16-float uniform matrix to the card (plus a ton of overhead that goes with it), so 16 floats of 2-d coordinates plus texture is a wash. As a general rule I would say that if you are using uniforms to transform single primitives, try using the CPU instead.For a desktop, one legitimate response might be "who cares"? Desktops are so fast now that it would be worth profiling naive code first to make sure optimization is warranted. For the iPhone, you probably still care.

### Batch It Up

The first thing you'll need to do is to put all of your geometry in a single VBO, and reference only a single texture (e.g. a texture atlas). This is mandatory for any kind of good performance. The cost of changing the source buffer or texture (in terms of CPU time spent in the driver) is quite a bit larger than the time it takes to actually draw a single quad. If you can't draw in bulk, stop now - there's no point in optimizing anything else.

(As a side note: you'll eat the cost of changing VBOs even if you simply change the base address pointer within the same VBO. Every time you muck around with the vertex pointers or vertex formats, the driver has to re-validate that what you are doing isn't going to blow up the GPU. It's incredible how many cases the driver has to check to make sure that a subsequent draw call is reasonable. glVertexPointer is way more expensive than it looks!)

#### The Naive Approach

The naive approach is to use the OpenGL transform stack (e.g. glRotate, glTranslate, etc.) to position each quad, then draw it. Under the hood, the OpenGL transform stack translates into "uniform" state change - that is, changing state that is considered invariant during a draw call but changes between draw calls. (If you are using the GL 2.0 core profile, you would code glRotate/glTranslate yourself by maintaining a current matrix and changing a uniform.)

When drawing a lot of stuff, uniforms are your friend; because they are known to be uniform for a single draw call, the driver can put them in memory on the GPU where they are quick to access over a huge number of triangles or quads. But when drawing a very small amount of geometry, the cost of changing the uniforms (more driver calls, more CPU time) begins to outweigh the benefit of having the GPU "do the math".

In particular, if each quad has its own matrix stack in 2-d, you are saving 24 MADs per quad by requiring the driver to rebuild the current uniform state. (How much does that cost? A lot more than 24 MADs.) Even ignoring the uniforms, the fact that a uniform changed means each draw call can only draw 1 quad. Not fast.

#### Stream the Geomery

One simple option is to throw out hardware transform on the GPU and simply transform the vertices on the CPU before "pushing" them to the GPU. Since the geometry of the quads are changing per frame, you were going to have to send them to the GPU anyway. This technique has a few advantages and disadvantages.

- Win: You get all of your drawing in a single OpenGL draw call with a single VBO. So your driver time is going to be low and you're talking to the hardware efficiency.
- Win: This requires no newer GL 3.x/4.x kung fu. That's good if you're using OpenGL 2.0 ES on an iPhone, for example.
- Fail: You have to push every vertex every frame. That costs CPU and (on desktops) bus bandwidth.
- Not-total-fail: Once you commit to pushing everything every frame, the cost of varying UV maps in real-time has no penalty; and there isn't a bus to jam up on a mobile device.

#### Stupid OpenGL Tricks

If you are on a desktop with a modern driver, you can in theory leverage the compute power of the GPU, cut down your bandwidth, and still avoid uniform-CPU-misery.

*Disclaimer: while we use instancing heavily in X-Plane, I have not tried this technique for 2-d quads. Per the first section, in X-Plane desktop we don't have any cases where we care enough. The streaming case was important for iPhone.*

To cut down the amount of streamed data:

- Set the GPU up for vertex-array-divisor-style instancing.
- In your instance array, push the transform data. You might have an opportunity for compression here; for example, if all of your transforms are translate+2-d rotate (no scaling ever), you can pass a pair of 2-d offsets and the sin/cos of the rotation and let the shader apply the math ad-hoc, rather than using a full 4x4 matrix. If your UV coordinates change per quad, you'll need to pass some mix of UV translations/scales. (Again, if there is a regularity to your data you can save instance space.)
- The mesh itself is a simple 4-vertex quad in a static VBO.

There are a few other ways to cut this up that might not be as good as hw instancing:

- There are other ways to instance using the primitive ID and UBOs or TBOs - YMMV.
- If you have no instancing, you can use immediate mode to push the transforms and make individual draw calls. This case will probably outperform uniforms, but probably not outperform streaming and CPU transform.
- You could use geometry shaders, but um, don't.

Wow, what a nice article!









ReplyDeleteYou are right, the streaming method is the best for rendering dynamic 2D geometry under iOS (OpenGL ES 2.0). The thing is how to do it the most efficiently - I mean how to send data to GPU… and also what data.

You touched the latter part by mentioning "instancing" and "compressing". When I say "instancing under OpenGL ES 2.0" I mean that you send object's transformation matrix (compressed if possible) as a part of the vertex data, extract/recreate the matrix in vertex shader and then do to transform on GPU. This is the method which I use in our game for rendering many dynamic 2D objects (which have relatively few vertices on their own) in one draw call. Btw I use "linked" triangle strips which seemed as a better solution than options like indexed triangle list. I didn't perform any relevant comparison test to prove that, though.

But I wonder if doing the transform on GPU is faster that doing it on CPU (using NEON instructions if possible). PowerVR GPUs' SIMD architecture should be quite a good match for that task but considering differences in frequencies (1Ghz CPU vs 200Mhz GPU) I am not sure if GPU is really that faster doing 2D transform. Also there are many different SoCs in iOS devices - starting with A4 in iPhone4 (Cortex-A8/SGX535) and ending with the newest A6x in iPad4 (?Cortex-A9 Custom?/SGX554) so GPU/CPU performance may vary from device to device. There is no recommended method. We are not vertex bound so I don't plan to investigate further… for now :)

Now about the problem how to send data to GPU (update your VBO) This always translates to questions like: "Single-buffered, double-buffered or even triple-buffered? Use a ring buffer? Discard an old buffer? Use glMapBuffer(Range), glBufferData or glBufferSubdata?", and more similar ones to which only the GPU driver engineers know the answer :) There are just too many ways how to do it, which means you can easily do it wrong. But do I actually care? Nope, because in most iOS games the differences are really not so huge and again vary from one iDevice to another… I tested some variants long time ago on my old iPhone4 and iPad2 and decided to stick with the best one after that. So right now I use tripe-buffered approach with glMapBuffer while discarding an old buffer. I haven't done any comparison tests since then so maybe another method is better on newer devices but I think I don't care enough becuase the game still runs 60 frames per seconds and it has other problems :)

So in the end I am streaming my dynamic geometry using my preferred method and all seems pretty fast in that part of the pipeline because I am fill-rate bound anyway :)

#end_of_rant

PS.: Btw I really like your older articles about double-buffered VBOs :)

Totally true - on IOS with GLES 2.0 you do have the option to write a shader to 'decompress' some kind of packed up transformation. But you also bring up the other issue: the GPUs aren't super-beefy. I think it's a question of what the game is bound up on...if the game is dying for CPU, an offload is a win. If the CPU is idle and you've maxed out the poor GPU, then trying to use GPU-based transform is not a win.


ReplyDeleteI think in our latest code we use indexed triangles and orphaning and it works pretty well. You can tell pretty easily when you've won with instruments - when you're doing something the driver doesn't like a ton of CPU stuff with ominous names will show up in the stack trace under the glDrawXXX call. :-)

You are right, "Test, compare and analyze using Instruments" is what I recommend to everyone too :D



ReplyDeleteBtw do you have all vertex data in one VBO and stream everything or do you split them into multiple so you can update (or not) them separately? I mean in the iOS version. I prefer the interleaved method but in our case it doesn't really matter... I think :)

Hi Vladimir,




ReplyDeleteWe always keep all vertex attributes interleaved in a single VBO for both IOS and desktop - only the indices are in a separate VBO.

We do this to maintain locality - whatever hw fetches a vertex, we want the vertex to sit in a cache line, etc.

Cheers

Ben

I'm curious, I've only this week started playing around properly with OpenGL so please excuse my ignorance here..










ReplyDeleteWhen you say your vertex attributes for all mesh data is interleaved in a single VBO...

Is that to say that the vertices and the attributes themselves are interleaved? e.g.:

{pos_0,colour_0,pos_1,colour_1,...,pos_n,colour_n}

Or is each individual object encoded such that the vertices are all sequential, followed by a sequential block of attributes?

{pos_0,pos_1,...,pos_n,colour_0,colour_1,...,colour_n}

I suspect the latter, such the vertices for an object are sequential, followed by a sequential block of attributes for that object, and then repeat for each object...

Is there any measurable benefit of either approach?

95% of the time you want to go pos0, color0, normal0, pos1, color1, normal1. The GPU is going to fetch data from memory in relatively big chunks (it has a wide memory system) - if all of the data in a single vertex is nearby, then all of the data it fetches is useful immediately, and cache utilization is good.


ReplyDeleteThe only exception is if you need some data to change per frame and some is static - in that case, keep the data separate AND use separate VBOs. That way you can set the unchanged data to STATIC_DRAW and the changing data to STREAM_DRAW.

From my experience developing a voxel engine: for small vertex strides and small "instance" sizes, using a geometry shader to blow up each instance is MUCH faster than instancing. As the vertex stride increases, however, the geometry shader becomes inferior to simply filling a VBO with a pair of triangles for each quad. As for instancing in that case, common wisdom amongst the voxel gurus is that instancing is intended for *large* vertex-per-instance counts, and small ones won't perform well at all. At the end of the day, though, this only matters if you're not already fill-rate bound... a likely scenario if your voxels are better looking than Minecraft's :)

ReplyDelete