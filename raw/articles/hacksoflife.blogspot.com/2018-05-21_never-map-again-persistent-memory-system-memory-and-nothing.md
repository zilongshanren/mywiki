---
title: 'Never Map Again: Persistent Memory, System Memory, and Nothing In Between'
url: http://hacksoflife.blogspot.com/2018/05/never-map-again-persistent-memory.html
author: Benjamin Supnik
published: '2018-05-21'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I have, over the years,


It's 2018 and we've been rebuilding our internal engine around abstractions that can work on a modern GL driver, Vulkan and Metal. When it comes to streaming geometry, here's what I have found.



That persistent memory is a win is unsurprising - you can't get any faster than not doing any work at all, and persistent memory simply removes the driver from the equation by giving you a direct memory-centric way to talk to the GPU.



This second result surprised me, but in every test I've run, client arrays in system memory have out-performed VBOs for small-to-medium sized batches. We were already using system memory for small-batch vertex drawing, but it's even faster for larger buffers.


Now before you go and delete all your VBO code, a few caveats:




Unlike VBOs, in the case of client arrays, the driver knows


When the draw call happens, the driver knows:








[written](http://hacksoflife.blogspot.com/2006/10/vbos-pbos-and-fbos.html)[more](http://hacksoflife.blogspot.com/2008/09/so-where-is-that-fast-path.html)[posts](http://hacksoflife.blogspot.com/2010/02/double-buffering-vbos.html)on[VBOs](http://hacksoflife.blogspot.com/2010/02/double-buffering-part-2-why-agp-might.html)and[vertex](http://hacksoflife.blogspot.com/2010/02/one-more-on-vbos-glbuffersubdata.html)[performance](http://hacksoflife.blogspot.com/2010/08/when-is-your-vbo-double-buffered.html)in[OpenGL](http://hacksoflife.blogspot.com/2012/04/beyond-glmapbuffer.html)than I'd like to admit. At this point, I can't even find them all. Vertex performance is often critical in X-Plane because we draw a lot of*stuff*in the world; at altitude you can see a lot of little things, and it's useful to be able to just blast all of the geometry through, if we can find a high performance vertex path.It's 2018 and we've been rebuilding our internal engine around abstractions that can work on a modern GL driver, Vulkan and Metal. When it comes to streaming geometry, here's what I have found.

### Be Persistent!

First, use persistent memory if you have it. On modern GL 4.x drivers on Windows/Linux, the driver can permanently map buffers for streaming via[GL_ARB_buffer_storage](https://www.khronos.org/registry/OpenGL/extensions/ARB/ARB_buffer_storage.txt). This is plan A! This will be the fastest path you can find because you pay no overhead for streaming geometry - you just write the data. (It's also multi-core friendly because you can grab a region of mapped memory without having to talk to the driver at all, avoiding multi-context hell.)That persistent memory is a win is unsurprising - you can't get any faster than not doing any work at all, and persistent memory simply removes the driver from the equation by giving you a direct memory-centric way to talk to the GPU.

### Don't Be Uncool

Second, if you don't have persistent memory (e.g. you are on OS X), use system memory via client arrays, rather than[trying to jam your data into a VBO with glMapBuffer](http://hacksoflife.blogspot.com/2015/06/glmapbuffer-no-longer-cool.html)or glBufferSubData.This second result surprised me, but in every test I've run, client arrays in system memory have out-performed VBOs for small-to-medium sized batches. We were already using system memory for small-batch vertex drawing, but it's even faster for larger buffers.

Now before you go and delete all your VBO code, a few caveats:

- We are mostly testing small-batch draw performance - this is UI, some effects code, but not million-VBO terrain chunks.
- The largest streaming data I have tried is a 128K index buffer. That's not tiny - that's perhaps 32 VM pages, but it's not a 2 MB static mesh.
- It wouldn't shock me if index buffers are more friendly to system memory streaming than vertex buffers - the 128K index buffer indexes a static VBO.

### Why Would Client Arrays Be Fast?

I'd speculate, they're easier to optimize.Unlike VBOs, in the case of client arrays, the driver knows

*everything*about the data transfer at one time. Everything up until an actual draw call is just stashing pointers for later use - the app is required to make sure the pointers remain valid until the draw call happens.When the draw call happens, the driver knows:

- How big the data is.
- What format the data is in.
- Which part of the data is actually consumed by the shader.
- Where the data is located (system memory, duh).
- That this is a streaming case - since the API provides no mechanism for efficient reuse, the driver might as well assume no reuse.

There's not really any validation to be done - if your client pointers point to junk memory, the driver can just segfault.

Because the driver knows how big the draw call is at the time it manages the vertex data, it can select the optimal vertex transfer mode for the particular hardware and draw call size. Large draws can be scheduled via a DMA (worth it if enough data is being transferred), medium draws can be sourced right from AGP memory, and tiny draws could even be stored directly in the command buffer.

### You Are Out of Order

There's one last thing we know for client arrays that we don't know for map/unmap, and I think this might be the most important one of all: in the case of client arrays, vertex transfer is strictly FIFO - within a single context (and client arrays data is not shared) submission order from the client is draw/retirement order.

That means the driver can use a simple ring buffer to allocate memory for these draw calls. That's really cheap unless the total size of the ring buffer has to grow.

By comparison, the driver can assume nothing about orphaning and renaming of VBOs. Rename/map/unmap/draw sequences show up as ad hoc calls to the driver, so the driver has to allocate new backing storage for VBOs out of a free store/heap. Even if the driver has a magazine front-end, the cost of heap allocations in the driver is going to be more expensive than bumping ring buffer pointers.

### What Can We Do With This Knowledge?

Once we recognize that we're going to draw only with client arrays and persistent memory (and not with non-persistent mapped and unmapped VBOs), we can recognize a simplifying assumption: our unmap/flushing overhead is

*zero*in every case, and we can simplify client code around this.
In a previous post, I suggested two ways around the

[cost of ensuring that your data is GPU-visible](http://hacksoflife.blogspot.com/2018/01/flush-less-often.html): persistent memory and deferring all command encoding until later.
If we're not going to have to unmap, we can just go with option 1 all of the time. If we don't have persistent coherent memory, we treat system memory as our persistent coherent memory and draw with client arrays. This means we can drop the cost of buffering up and replaying our command encoding and just render directly.

## No comments:

## Post a Comment