---
title: Rendering Performance
url: http://gameenginebook.blogspot.com/2012/01/rendering-questions.html
author: Jqgregory
published: '2012-01-05'
source_blog: Game Engine Architecture
source_site: http://gameenginebook.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Selected email conversations, errata and announcements regarding "Game Engine Architecture" by Jason Gregory

Thursday, January 5, 2012

Rendering Performance

From:Manuel Fernandez

Hello,

My name is manny, and I'm a big fan of your book. I think it's great how all the main parts of a game engine interact with each other. Most of the time you can probably find good resources online that teach you how to do one thing or the other, but bringing things together to make a game engine is a topic all on its own. I think you book does a great job at detailing all the different parts of a game engine and how they work together.

I bought your book after I read an article in gamasutra about it, i thought it would be useful. I have a Quake 3 BSP file loader which works on both Direct X and Open gl. I'm pretty proud of it because it implements Quake 3's PVS and AABB to frustum culling, and bezier patches. What surprises me is that when i get out of the BSP comfort zone, like rendering from outside the bsp, or simply rendering the whole virtual world, it's a pretty big hit in performance. I'm pretty sure game engine's like UDK, or source can handle drawing a quake 3 level without a problem. I guess my question is what makes industry strength game engines perform so much better than average? I think it's more than just smart culling, or better thread management.

Thank you for your time.

______________________________

Hi Manny, I'm sorry I didn't get back to you sooner, but your email fell thru the cracks.

I'm not a deep rendering guru, more of a generalist. But here are a few ways in which industrial strength rendering engines attain their high performance:

1. Rendering data is often packed into (relatively) small and contiguous data packets, to improve cache coherency. The real key here is to eliminate all pointer chasing during rendering. This means duplicating data, but it is worth it. We did this at Naughty Dog in order to optimize our rendering of dynamic objects (i.e. everything that is not static background geometry) and it yielded immense improvements. So as a (contrived) example, instead of a MeshInstance struct that contains a pointer to a material, which in turn contains pointers to lighting data etc. we would now have a RenderableInstance struct that contains all the data that you would have found by following down all the pointers (and ONLY the data that is actually needed for rendering). (Or maybe it would be multiple arrays of structs, each one containing one type of data... but the key is to avoid the use of pointers to refer to data that lives elsewhere in memory.) These structs aren't tiny, but at least we can iterate thru them in one linear swoop, and gain the benefits of precacheing the memory as we go. Any time you jump around in memory you're going to flush your L1/L2 cache and hurt your performance.

2. Pre-sorting to reduce render state changes is a great idea. That includes which vertex and index buffers you're rendering from (i.e. which mesh), which vertex and fragment/pixel shader programs are loaded, your render constants (transformation matrices, lighting vectors, animation matrix palette, etc.), which texture units you're rendering from, and all the other "render state" of the GPU. Most high-performance rendering engines divide the geometry up into two big categories: opaque and translucent. For opaque, you sort to minimize render state changes as I said: set up the render state for a particular "bin" and then render everything in that bin, then change state, and go again. For translucent, you typically have to sort the geometry in back-to-front order so it looks right. So you lose the benefits of sorting by render state changes. You do it after the opaque stuff, and try to limit how much translucent geometry you render.

3. Z pre-pass can be a savior, especially for GPU hardware on which fill rate (pixel shade, blend and store rate) is limited (like the PS3). I think I describe it in the book, but the basic idea is to put the GPU into a special z-write-only mode, then render the scene with the simplest possible pixel shader (since only the depth/z matters anyway). This is very fast. Then you render the scene again, this time with real pixel shaders enabled (much slower), but without writing to the z-buffer... onlyreading the depth values you deposited before. The GPU is pretty good at early-ing out on fragments whose z values are larger than what's already in the z buffer, so you don't pay the cost of shading them.

4. Eliminate the middle man. DirectX and OpenGL are actually wrappers around a lower-level "raw" GPU hardware protocol called a command list. This is basically the stream of data that the GPU actually consumes, in order to know what to render, what render state changes to make, etc. On the PS3, Sony provides a library called libgcm that allows games to build up their own GPU command lists directly, rather than going through the OpenGL layer. This is really the only way to render fast on the PS3. And actually, Naughty Dog's rendering team wrote an optimized interface, similar to libgcm, but even faster, and customized to the specific compressed data formats that we use... That's what Uncharted uses to render. So the lesson here is: if you have access to a library like libgcm (or want to reverse-engineer one!!!), that can be the best way to wring the last ounces of performance out of your rendering engine.

That said, the only way to be sure about performance is to code it and profile it. So once you have a basic mesh rendering working, you can try optimizing it by (a) keeping all the render data in one or more contiguous arrays -- i.e. eliminate pointer-chasing in your render loop, and (b) sort by render state changes for maximum thruput. Then profile it, and tweak from there.

## No comments:

## Post a Comment